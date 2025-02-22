import pandas as pd
from sqlalchemy import text, Table, Column, String, MetaData, create_engine
from bs4 import BeautifulSoup
import requests
from datetime import datetime
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

def fetch_product_details(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }
    
    try:
        response = requests.get(product_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return {
                "image_url": DEFAULT_IMAGE_URL,
                "title": None,
                "price": 0.0
            }
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        image_url = DEFAULT_IMAGE_URL
        
        image_selectors = [
            {"id": "landingImage"},
            {"id": "imgBlkFront"},
            {"class": "a-dynamic-image"},
            {"class": "s-image"},
            {"id": "main-image"},
            {"id": "product-image"},
            {"class": "image-block"},
            {"class": "product-image-container"}
        ]
        
        for selector in image_selectors:
            image_tags = soup.find_all("img", selector)
            
            for image_tag in image_tags:
                for attr in ['src', 'data-src', 'data-a-dynamic-image', 'data-old-hires', 'data-zoom-hires']:
                    img_url = image_tag.get(attr)
                    
                    if img_url:
                        if attr == 'data-a-dynamic-image':
                            try:
                                import json
                                urls = json.loads(img_url)
                                if urls:
                                    image_url = list(urls.keys())[0]
                                    break
                            except Exception as e:
                                continue
                        else:
                            image_url = img_url
                            break
                
                if image_url != DEFAULT_IMAGE_URL:
                    break
            
            if image_url != DEFAULT_IMAGE_URL:
                break
        
        if image_url and image_url != DEFAULT_IMAGE_URL:
            if '._' in image_url:
                base_url = image_url.split('._')[0]
                image_url = f"{base_url}._V1_FMjpg_UX1000_.jpg"
            elif '_SL' in image_url:
                base_url = image_url.split('_SL')[0]
                image_url = f"{base_url}_SL1500_.jpg"
                
            print(f"Final image URL: {image_url}")
        else:
            print("No image found, using default image")
        
        title_tag = soup.find("span", {"id": "productTitle"})
        title = title_tag.text.strip() if title_tag else None
        print(f"Found title: {title}")
        
        price = 0.0
        price_tag = soup.find("span", {"class": "a-price-whole"})
        if price_tag:
            try:
                price_text = price_tag.text.strip().rstrip('.').replace(',', '')
                price_inr = float(price_text)
                price = round(price_inr / 90, 2)
                print(f"Found price: {price}")
            except (ValueError, AttributeError) as e:
                print(f"Error parsing price: {e}")
                price = 0.0
        else:
            print("No price found")
        
        return {
            "image_url": image_url,
            "title": title,
            "price": round(float(price), 2)
        }
        
    except Exception as e:
        print(f"Error fetching product details: {str(e)}")
        return {
            "image_url": DEFAULT_IMAGE_URL,
            "title": None,
            "price": 0.00
        }

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
                COALESCE(AVG(ab.Rating), 0) as avg_rating,
                COUNT(ab.Rating) as review_count
            FROM products prod
            LEFT JOIN amazon_beauty ab ON prod.ProductId = ab.ProductId
            WHERE ({conditions})
                AND prod.ProductId IS NOT NULL
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
