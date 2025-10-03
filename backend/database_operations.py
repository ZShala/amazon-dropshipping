import pandas as pd
from sqlalchemy import text, Table, Column, String, MetaData, create_engine
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from functools import lru_cache, wraps
import json
import time

CATEGORY_MAPPING = {
    'makeup': [
        '%Eyeliner%', '%Kajal%', '%Lipstick%', '%Foundation%',
        '%Mascara%', '%Eye Shadow%', '%Concealer%', '%Blush%',
        '%Compact%', '%Powder%', '%Nail%', '%Makeup%'
    ],
    'skincare': [
        '%Face%', '%Skin%', '%Cream%', '%Moisturizer%',
        '%Serum%', '%Mask%', '%Facial%', '%Cleanser%',
        '%Toner%', '%Lotion%'
    ],
    'haircare': [
        '%Hair%', '%Shampoo%', '%Conditioner%', '%Scalp%'
    ],
    'fragrance': [
        '%Perfume%', '%Fragrance%', '%Body Spray%',
        '%Deodorant%', '%Scent%'
    ],
    'miscellaneous': [
        '%Tool%', '%Kit%', '%Accessory%', '%Accessories%',
        '%Brush%', '%Applicator%', '%Beauty Tool%', '%Makeup Tool%'
    ]
}

DEFAULT_IMAGE_URL = "http://localhost:5001/static/images/product-placeholder.jpg"

SCRAPING_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

product_cache = {}
cache_duration = timedelta(hours=1)

def get_cached_product(product_id):
    """Merr produktin nga cache"""
    if product_id in product_cache:
        cached_data, timestamp = product_cache[product_id]
        if datetime.now() - timestamp < cache_duration:
            return cached_data
        del product_cache[product_id]
    return None

def set_cached_product(product_id, data):
    """Ruan produktin në cache"""
    product_cache[product_id] = (data, datetime.now())

def setup_database(engine):
    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS amazon_beauty (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ProductId VARCHAR(255),
                        ProductType VARCHAR(255),
                        Rating FLOAT,
                        URL TEXT,
                        Timestamp BIGINT,
                        UserId VARCHAR(255),
                        INDEX idx_product_id (ProductId(255)),
                        INDEX idx_rating (Rating),
                        INDEX idx_product_type (ProductType(255))
                    )
                """))
                
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS product_images (
                        asin VARCHAR(20) PRIMARY KEY,
                        image_url VARCHAR(500) NOT NULL,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_last_updated (last_updated)
                    ) ENGINE=InnoDB
                """))
                
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ProductId VARCHAR(255) UNIQUE,
                        ProductTitle TEXT,
                        ImageURL TEXT,
                        price DECIMAL(10,2),
                        INDEX idx_product_id (ProductId(255))
                    )
                """))
                
                try:
                    conn.execute(text("""
                        ALTER TABLE products 
                        ADD COLUMN price DECIMAL(10,2) AFTER ImageURL
                    """))
                except Exception as e:
                    if "Duplicate column name" not in str(e):
                        raise e
            
            tables = conn.execute(text("""
                SELECT TABLE_NAME 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE()
            """)).fetchall()
            
            for row in tables:
                print(f"- {row[0]}")
            
            products_table = conn.execute(text("""
                SELECT TABLE_NAME 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND TABLE_NAME = 'products'
            """)).fetchone()
            
            if products_table:
                print("\nProducts table created successfully!")
            else:
                raise Exception("Products table was not created!")
            
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        raise

def get_data_from_db(engine):
    try:
        query = text("""
            SELECT DISTINCT 
                p.ProductId, 
                p.ProductType, 
                ab.Rating, 
                p.URL,
                COUNT(*) OVER (PARTITION BY p.ProductId) as review_count,
                AVG(ab.Rating) OVER (PARTITION BY p.ProductId) as avg_rating
            FROM products p
            JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
            WHERE p.ProductId IS NOT NULL 
                AND p.ProductType IS NOT NULL 
                AND ab.Rating >= 4.0
                AND p.price > 0
            HAVING review_count >= 3
            ORDER BY avg_rating DESC, review_count DESC
            LIMIT 1000
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query)
            df = pd.DataFrame(result.fetchall(), 
                            columns=['ProductId', 'ProductType', 'Rating', 'URL', 'ReviewCount', 'AvgRating'])
            return df
    
    except Exception as e:
        print(f"Error reading data: {str(e)}")
        return None

def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_decorator(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = seconds
        func.expiration = time.time() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.time() >= func.expiration:
                func.cache_clear()
                func.expiration = time.time() + func.lifetime
            return func(*args, **kwargs)

        return wrapped_func
    return wrapper_decorator

@timed_lru_cache(seconds=3600, maxsize=1000)  # Cache zgjat 1 orë
def get_product_details(engine, product_id):
    """Merr detajet e produktit nga databaza me caching"""
    try:
        cached_product = get_cached_product(product_id)
        if cached_product:
            return cached_product

        query = text("""
            SELECT 
                p.ProductId,
                p.ProductType,
                p.ProductTitle,
                p.URL,
                p.ImageURL,
                p.price,
                ROUND(COALESCE(AVG(ab.Rating), 0), 1) as avg_rating,
                COUNT(DISTINCT ab.UserId) as review_count,
                GROUP_CONCAT(DISTINCT ab.ProductType) as categories,
                MIN(p.price) as min_price,
                MAX(p.price) as max_price
            FROM products p
            LEFT JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
            WHERE p.ProductId = :product_id
                AND p.price > 0
            GROUP BY p.ProductId, p.ProductType, p.ProductTitle, p.URL, p.ImageURL, p.price
        """)

        with engine.connect() as conn:
            result = conn.execute(query, {"product_id": product_id}).fetchone()
            
            if result:
                product = {
                    "ProductId": result.ProductId,
                    "ProductType": result.ProductTitle or result.ProductType,
                    "Rating": float(result.avg_rating),
                    "URL": result.URL,
                    "ReviewCount": result.review_count,
                    "ImageURL": result.ImageURL or "http://localhost:5001/static/images/product-placeholder.jpg",
                    "price": float(result.price) if result.price else 0.0,
                    "categories": result.categories.split(',') if result.categories else [],
                    "price_range": {
                        "min": float(result.min_price) if result.min_price else 0.0,
                        "max": float(result.max_price) if result.max_price else 0.0
                    },
                    "currency": "EUR"
                }

                # Ruaj në cache
                set_cached_product(product_id, product)
                return product

        return None

    except Exception as e:
        print(f"Error in get_product_details: {str(e)}")
        return None

def get_category_products(engine, category_type, page=1, per_page=None):
    try:
        search_terms = CATEGORY_MAPPING.get(category_type.lower(), [])
        
        if not search_terms:
            print(f"Nuk u gjetën terma kërkimi për kategorinë: {category_type}")
            return {"products": [], "total": 0, "page": page, "per_page": per_page, "total_pages": 0}

        conditions = " OR ".join([
            f"LOWER(prod.ProductType) LIKE LOWER(:term{i})"
            for i in range(len(search_terms))
        ])

        query = text(f"""
            SELECT DISTINCT 
                prod.ProductId,
                prod.ProductType,
                prod.ProductTitle,
                prod.ImageURL,
                prod.price,
                prod.URL,
                ROUND(COALESCE(AVG(ab.Rating), 0), 1) as avg_rating,
                COUNT(ab.Rating) as review_count
            FROM products prod
            LEFT JOIN amazon_beauty ab ON prod.ProductId = ab.ProductId
            WHERE ({conditions})
                AND prod.ProductId IS NOT NULL
                AND prod.price > 0
            GROUP BY 
                prod.ProductId, 
                prod.ProductType,
                prod.ProductTitle,
                prod.ImageURL,
                prod.price,
                prod.URL
            HAVING review_count > 0
            ORDER BY avg_rating DESC, review_count DESC
        """)

        print(f"Executing query for category: {category_type}")
        print(f"Search terms: {search_terms}")

        with engine.connect() as conn:
            params = {f"term{i}": term for i, term in enumerate(search_terms)}
            print(f"Query parameters: {params}")
            
            result = conn.execute(query, params)
            products = []
            
            for row in result:
                try:
                    image_url = row.ImageURL
                    if not image_url or image_url.isspace():
                        image_url = DEFAULT_IMAGE_URL
                    elif not image_url.startswith(('http://', 'https://')):
                        image_url = f"http://localhost:5001/static/images/{image_url}"

                    product_details = {
                        "ProductId": row.ProductId,
                        "ProductType": row.ProductType,
                        "ProductTitle": row.ProductTitle or row.ProductType,
                        "Rating": float(row.avg_rating),
                        "URL": row.URL,
                        "ReviewCount": row.review_count,
                        "ImageURL": image_url,
                        "price": float(row.price) if row.price else 0.0,
                        "currency": "EUR"
                    }
                    products.append(product_details)
                except Exception as e:
                    print(f"Error processing product {row.ProductId}: {str(e)}")
                    continue

            print(f"Found {len(products)} products for category {category_type}")
            
            return {
                "products": products,
                "total": len(products),
                "page": page,
                "per_page": len(products),
                "total_pages": 1
            }

    except Exception as e:
        print(f"Error in get_category_products: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "products": [],
            "total": 0,
            "page": page,
            "per_page": 0,
            "total_pages": 1
        }

def check_and_insert_product(engine, product_data):
    try:
        with engine.connect() as conn:
            with conn.begin():
                check_query = text("""
                    SELECT ProductId, price
                    FROM products 
                    WHERE ProductId = :product_id
                """)
                
                result = conn.execute(check_query, {"product_id": product_data["ProductId"]})
                existing_product = result.fetchone()
                
                if not existing_product:
                    insert_query = text("""
                        INSERT INTO products 
                        (ProductId, ProductType, ProductTitle, URL, ImageURL, price)
                        VALUES 
                        (:product_id, :product_type, :product_title, :url, :image_url, :price)
                    """)
                    
                    params = {
                        "product_id": product_data["ProductId"],
                        "product_type": product_data["ProductType"],
                        "product_title": product_data.get("ProductTitle", ""),
                        "url": product_data["URL"],
                        "image_url": product_data.get("ImageURL", DEFAULT_IMAGE_URL),
                        "price": product_data.get("price")
                    }
                    
                    print(f"Inserting product with data: {params}")
                    conn.execute(insert_query, params)
                    print(f"Successfully inserted product {product_data['ProductId']}")
                    return True
                else:
                    if product_data.get("price") is not None:
                        update_query = text("""
                            UPDATE products 
                            SET price = :price
                            WHERE ProductId = :product_id
                        """)
                        conn.execute(update_query, {
                            "product_id": product_data["ProductId"],
                            "price": product_data["price"]
                        })
                        print(f"Updated price for product {product_data['ProductId']}")
                    
                    return False
            
    except Exception as e:
        print(f"Detailed error in check_and_insert_product for ProductId {product_data.get('ProductId', 'unknown')}: {str(e)}")
        print(f"Product data: {product_data}")
        return False

if __name__ == "__main__":
    engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
    setup_database(engine)  
    test_product_insertion(engine) 
