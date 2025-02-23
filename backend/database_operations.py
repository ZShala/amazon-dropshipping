import pandas as pd
from sqlalchemy import text, Table, Column, String, MetaData, create_engine
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from functools import lru_cache
import json

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

# Cache për produktet
product_cache = {}
cache_duration = timedelta(hours=1)

# Shtojmë cache për kategoritë
category_cache = {}
category_cache_duration = timedelta(minutes=30)  # Cache për 30 minuta

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

def get_cached_category(category_type, page):
    """Merr produktet e kategorisë nga cache"""
    cache_key = f"{category_type}_{page}"
    if cache_key in category_cache:
        cached_data, timestamp = category_cache[cache_key]
        if datetime.now() - timestamp < category_cache_duration:
            return cached_data
        del category_cache[cache_key]
    return None

def set_cached_category(category_type, page, data):
    """Ruan produktet e kategorisë në cache"""
    cache_key = f"{category_type}_{page}"
    category_cache[cache_key] = (data, datetime.now())

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
                ProductId, 
                ProductType, 
                Rating, 
                URL,
                COUNT(*) OVER (PARTITION BY ProductId) as review_count,
                AVG(Rating) OVER (PARTITION BY ProductId) as avg_rating
            FROM amazon_beauty 
            WHERE ProductId IS NOT NULL 
                AND ProductType IS NOT NULL 
                AND Rating >= 4.0
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

def fetch_image(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.find("img", {"id": "landingImage"})
        if image_tag:
            return image_tag.get("src")
    except Exception as e:
        print(f"Error fetching image for URL {product_url}: {e}")
    return "http://localhost:5001/static/images/product-placeholder.jpg"

@lru_cache(maxsize=1000)
def get_product_details(engine, product_id):
    """Merr detajet e produktit nga databaza me caching"""
    try:
        # Kontrollo cache-in
        cached_product = get_cached_product(product_id)
        if cached_product:
            return cached_product

        # Query e optimizuar që merr të gjitha të dhënat në një kërkesë
        query = text("""
            SELECT 
                p.ProductId,
                p.ProductType,
                p.ProductTitle,
                p.URL,
                p.ImageURL,
                p.price,
                COALESCE(AVG(ab.Rating), 0) as avg_rating,
                COUNT(DISTINCT ab.UserId) as review_count,
                GROUP_CONCAT(DISTINCT ab.ProductType) as categories,
                MIN(p.price) as min_price,
                MAX(p.price) as max_price
            FROM products p
            LEFT JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
            WHERE p.ProductId = :product_id
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

def get_category_products(engine, category_type, page=1, per_page=20):
    try:
        # Kontrollo cache-in
        cached_result = get_cached_category(category_type, page)
        if cached_result:
            return cached_result

        search_terms = CATEGORY_MAPPING.get(category_type.lower(), [])
        
        if not search_terms:
            return {"products": [], "total": 0, "page": page, "per_page": per_page}

        # Query e optimizuar
        query = text("""
            WITH RankedProducts AS (
                SELECT DISTINCT 
                    prod.ProductId,
                    prod.ProductType,
                    prod.ProductTitle,
                    prod.ImageURL,
                    prod.price,
                    COALESCE(AVG(ab.Rating), 0) as avg_rating,
                    COUNT(DISTINCT ab.UserId) as review_count,
                    ROW_NUMBER() OVER (
                        ORDER BY 
                            COALESCE(AVG(ab.Rating), 0) DESC,
                            COUNT(DISTINCT ab.UserId) DESC
                    ) as row_num
                FROM products prod
                LEFT JOIN amazon_beauty ab ON prod.ProductId = ab.ProductId
                WHERE prod.ProductType REGEXP :search_pattern
                    AND prod.ProductId IS NOT NULL
                GROUP BY 
                    prod.ProductId, 
                    prod.ProductType,
                    prod.ProductTitle,
                    prod.ImageURL,
                    prod.price
                HAVING review_count > 0
            )
            SELECT *
            FROM RankedProducts
            WHERE row_num BETWEEN :start_row AND :end_row
        """)

        # Përgatit pattern për kërkim
        search_pattern = '|'.join(term.replace('%', '') for term in search_terms)
        start_row = (page - 1) * per_page + 1
        end_row = start_row + per_page - 1

        with engine.connect() as conn:
            # Merr totalin e produkteve
            count_query = text("""
                SELECT COUNT(*) as total
                FROM (
                    SELECT DISTINCT prod.ProductId
                    FROM products prod
                    LEFT JOIN amazon_beauty ab ON prod.ProductId = ab.ProductId
                    WHERE prod.ProductType REGEXP :search_pattern
                    GROUP BY prod.ProductId
                    HAVING COUNT(DISTINCT ab.UserId) > 0
                ) as counted
            """)
            
            total = conn.execute(count_query, {
                "search_pattern": search_pattern
            }).scalar()

            # Merr produktet për faqen aktuale
            results = conn.execute(query, {
                "search_pattern": search_pattern,
                "start_row": start_row,
                "end_row": end_row
            }).fetchall()

            products = []
            for row in results:
                try:
                    image_url = row.ImageURL or DEFAULT_IMAGE_URL
                    if not image_url.startswith(('http://', 'https://')):
                        image_url = f"http://localhost:5001/static/images/{image_url}"

                    product = {
                        "ProductId": row.ProductId,
                        "ProductType": row.ProductType,
                        "ProductTitle": row.ProductTitle or row.ProductType,
                        "Rating": float(row.avg_rating),
                        "ReviewCount": row.review_count,
                        "ImageURL": image_url,
                        "price": float(row.price) if row.price else 0.0,
                        "currency": "EUR"
                    }
                    products.append(product)
                except Exception as e:
                    print(f"Error processing product {row.ProductId}: {str(e)}")
                    continue

            result = {
                "products": products,
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page
            }

            # Ruaj në cache
            set_cached_category(category_type, page, result)
            return result

    except Exception as e:
        print(f"Error in get_category_products: {str(e)}")
        return {
            "products": [],
            "total": 0,
            "page": page,
            "per_page": per_page,
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
