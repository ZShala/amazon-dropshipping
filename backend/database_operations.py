import pandas as pd
from sqlalchemy import text, Table, Column, String, MetaData, create_engine
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time

# Konfigurimet që ishin në config.py
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
    """Krijon tabelat dhe indekset e nevojshme në databazë"""
    try:
        with engine.connect() as conn:
            with conn.begin():
                # Create amazon_beauty table
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
                        INDEX idx_product_type (ProductType(255)),
                        INDEX idx_composite (ProductType(255), Rating),
                        FULLTEXT INDEX idx_product_type_fulltext (ProductType)
                    ) ENGINE=InnoDB
                """))
                
                # Create product_images table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS product_images (
                        asin VARCHAR(20) PRIMARY KEY,
                        image_url VARCHAR(500) NOT NULL,
                        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_last_updated (last_updated)
                    ) ENGINE=InnoDB
                """))
                
                # Create products table without last_price_update
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ProductId VARCHAR(255) UNIQUE,
                        ProductType VARCHAR(255),
                        ProductTitle VARCHAR(500),
                        URL TEXT,
                        ImageURL TEXT,
                        price DECIMAL(10,2),
                        INDEX idx_product_id (ProductId(255))
                    ) ENGINE=InnoDB
                """))
                
                # Add price column if it doesn't exist (for existing tables)
                try:
                    conn.execute(text("""
                        ALTER TABLE products 
                        ADD COLUMN price DECIMAL(10,2) AFTER ImageURL
                    """))
                except Exception as e:
                    if "Duplicate column name" not in str(e):
                        raise e
            
            # Verify tables exist
            tables = conn.execute(text("""
                SELECT TABLE_NAME 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE()
            """)).fetchall()
            
            print("\nTabelat e krijuara:")
            for row in tables:
                print(f"- {row[0]}")
            
            # Verify products table specifically
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
        print(f"Ndodhi një gabim gjatë setup të databazës: {str(e)}")
        raise  # Re-raise the exception to ensure we know if setup failed

def get_data_from_db(engine):
    """Merr të dhënat nga databaza"""
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
        print(f"Ndodhi një gabim gjatë leximit të të dhënave: {str(e)}")
        return None

def get_product_recommendations(engine, product_id):
    try:
        query = text("""
            WITH target_product AS (
                -- Marrim produktin target dhe statistikat e tij
                SELECT 
                    p.ProductId,
                    p.ProductType,
                    p.Rating,
                    COUNT(DISTINCT u.UserId) as user_count,
                    AVG(u.Rating) as avg_user_rating
                FROM amazon_beauty p
                LEFT JOIN amazon_beauty u ON p.ProductType = u.ProductType
                WHERE p.ProductId = :product_id
                GROUP BY p.ProductId, p.ProductType, p.Rating
            ),
            user_preferences AS (
                -- Gjejmë përdoruesit që kanë vlerësuar këtë produkt
                SELECT DISTINCT 
                    u.UserId,
                    u.Rating as given_rating
                FROM amazon_beauty u
                WHERE u.ProductId = :product_id
            ),
            collaborative_recommendations AS (
                -- Produktet që përdoruesit e ngjashëm kanë vlerësuar mirë
                SELECT 
                    p.ProductId,
                    p.ProductType,
                    p.Rating,
                    p.URL,
                    COUNT(DISTINCT p.UserId) as review_count,
                    AVG(p.Rating) as avg_rating,
                    COUNT(DISTINCT up.UserId) as similar_users
                FROM amazon_beauty p
                JOIN user_preferences up ON p.UserId = up.UserId
                WHERE p.ProductId != :product_id
                GROUP BY p.ProductId, p.ProductType, p.Rating, p.URL
            ),
            content_similarity AS (
                -- Produktet e ngjashme bazuar në tip dhe karakteristika
                SELECT 
                    p.ProductId,
                    p.ProductType,
                    p.Rating,
                    p.URL,
                    COUNT(*) as review_count,
                    AVG(p.Rating) as avg_rating,
                    CASE 
                        WHEN p.ProductType = tp.ProductType THEN 3
                        WHEN SUBSTRING_INDEX(p.ProductType, ' ', 2) = 
                             SUBSTRING_INDEX(tp.ProductType, ' ', 2) THEN 2
                        WHEN p.ProductType LIKE CONCAT('%', SUBSTRING_INDEX(tp.ProductType, ' ', 1), '%') THEN 1
                        ELSE 0
                    END as type_similarity
                FROM amazon_beauty p
                CROSS JOIN target_product tp
                WHERE p.ProductId != tp.ProductId
                GROUP BY p.ProductId, p.ProductType, p.Rating, p.URL
            )
            SELECT 
                cr.ProductId,
                cr.ProductType,
                cr.URL,
                cr.avg_rating as Rating,
                cr.review_count,
                -- Llogarisim një score të kombinuar
                (
                    (IFNULL(cr.similar_users, 0) * 0.4) + 
                    (cs.type_similarity * 0.3) +
                    (cr.avg_rating * 0.2) +
                    (LOG(cr.review_count + 1) * 0.1)
                ) as recommendation_score
            FROM collaborative_recommendations cr
            JOIN content_similarity cs ON cr.ProductId = cs.ProductId
            WHERE cr.avg_rating >= 4.0
                AND cr.review_count >= 5
            ORDER BY recommendation_score DESC, cr.avg_rating DESC
            LIMIT 10
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query, {"product_id": product_id})
            recommendations = [{
                "ProductId": row.ProductId,
                "ProductType": row.ProductType,
                "Rating": float(row.Rating),
                "URL": row.URL,
                "ReviewCount": row.review_count,
                "Score": float(row.recommendation_score)
            } for row in result]
            
            if not recommendations:
                backup_query = text("""
                    WITH product_category AS (
                        SELECT SUBSTRING_INDEX(ProductType, ' ', 1) as category
                        FROM amazon_beauty 
                        WHERE ProductId = :product_id
                        LIMIT 1
                    )
                    SELECT 
                        p.ProductId,
                        p.ProductType,
                        AVG(p.Rating) as Rating,
                        COUNT(*) as review_count,
                        MAX(p.URL) as URL,
                        (AVG(p.Rating) * LOG(COUNT(*) + 1)) as popularity_score
                    FROM amazon_beauty p
                    CROSS JOIN product_category pc
                    WHERE p.ProductId != :product_id
                        AND p.ProductType LIKE CONCAT(pc.category, '%')
                        AND p.Rating >= 4.0
                    GROUP BY p.ProductId, p.ProductType
                    HAVING review_count >= 5
                    ORDER BY popularity_score DESC
                    LIMIT 10
                """)
                
                result = conn.execute(backup_query, {"product_id": product_id})
                recommendations = [{
                    "ProductId": row.ProductId,
                    "ProductType": row.ProductType,
                    "Rating": float(row.Rating),
                    "URL": row.URL,
                    "ReviewCount": row.review_count,
                    "Score": float(row.popularity_score)
                } for row in result]
            
            return recommendations
            
    except Exception as e:
        print(f"Ndodhi një gabim gjatë marrjes së rekomandimeve: {str(e)}")
        return []

def get_product_details(engine, product_id):
    """Merr detajet e një produkti specifik"""
    try:
        query = text("""
            SELECT ProductId, ProductType, Rating, URL
            FROM amazon_beauty
            WHERE ProductId = :product_id
            LIMIT 1
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query, {"product_id": product_id}).fetchone()
            if result:
                image_url = fetch_image(result.URL)
                
                return {
                    "ProductId": result.ProductId,
                    "ProductType": result.ProductType,
                    "Rating": float(result.Rating),
                    "URL": result.URL,
                    "ImageURL": image_url 
                }
            return None
            
    except Exception as e:
        print(f"Ndodhi një gabim gjatë marrjes së detajeve të produktit: {str(e)}")
        return None

def get_cart_recommendations(engine, product_ids):
    """Merr rekomandimet për produktet në cart"""
    try:
        cross_sell_query = text("""
            WITH cart_products AS (
                SELECT ProductType, Rating
                FROM amazon_beauty
                WHERE ProductId IN :product_ids
            ),
            complementary_products AS (
                -- Gjej produkte që blihen shpesh së bashku
                SELECT DISTINCT 
                    a.ProductId,
                    a.ProductType,
                    a.Rating,
                    a.URL,
                    COUNT(*) as purchase_frequency,
                    AVG(a.Rating) as avg_rating,
                    -- Llogarit një zbritje bazuar në frekuencën e blerjeve së bashku
                    CASE 
                        WHEN COUNT(*) > 100 THEN 15
                        WHEN COUNT(*) > 50 THEN 10
                        ELSE 5
                    END as suggested_discount
                FROM amazon_beauty a
                JOIN cart_products cp 
                WHERE a.ProductId NOT IN :product_ids
                    AND a.Rating >= 4.0
                GROUP BY a.ProductId, a.ProductType, a.Rating, a.URL
                HAVING purchase_frequency >= 10
                ORDER BY purchase_frequency DESC
                LIMIT 5
            )
            SELECT * FROM complementary_products
        """)

        up_sell_query = text("""
            WITH cart_products AS (
                SELECT 
                    ProductType,
                    AVG(Rating) as avg_rating
                FROM amazon_beauty
                WHERE ProductId IN :product_ids
                GROUP BY ProductType
            )
            SELECT DISTINCT
                a.ProductId,
                a.ProductType,
                a.Rating,
                a.URL,
                COUNT(*) as review_count,
                AVG(a.Rating) as avg_rating,
                -- Arsyet pse ky produkt është më i mirë
                CASE 
                    WHEN a.Rating > cp.avg_rating THEN 'Higher rated product'
                    WHEN a.Rating = cp.avg_rating THEN 'Premium alternative'
                    ELSE 'Popular choice'
                END as upgrade_reason
            FROM amazon_beauty a
            JOIN cart_products cp ON a.ProductType = cp.ProductType
            WHERE a.ProductId NOT IN :product_ids
                AND a.Rating >= cp.avg_rating
            GROUP BY a.ProductId, a.ProductType, a.Rating, a.URL, cp.avg_rating
            HAVING review_count >= 20
            ORDER BY avg_rating DESC, review_count DESC
            LIMIT 3
        """)

        with engine.connect() as conn:
            cross_sell_result = conn.execute(
                cross_sell_query, 
                {"product_ids": tuple(product_ids)}
            )
            up_sell_result = conn.execute(
                up_sell_query, 
                {"product_ids": tuple(product_ids)}
            )
            
            recommendations = {
                "crossSell": [{
                    "ProductId": row.ProductId,
                    "ProductType": row.ProductType,
                    "Rating": float(row.avg_rating),
                    "URL": row.URL,
                    "bundleDiscount": row.suggested_discount,
                    "purchaseFrequency": row.purchase_frequency
                } for row in cross_sell_result],
                
                "upSell": [{
                    "ProductId": row.ProductId,
                    "ProductType": row.ProductType,
                    "Rating": float(row.avg_rating),
                    "URL": row.URL,
                    "upgradeReason": row.upgrade_reason,
                    "reviewCount": row.review_count
                } for row in up_sell_result]
            }

            return recommendations
            
    except Exception as e:
        print(f"Ndodhi një gabim gjatë marrjes së rekomandimeve për cart: {str(e)}")
        return {"crossSell": [], "upSell": []}

def fetch_image(product_url):
    """Merr URL-në e imazhit nga faqja e produktit në Amazon"""
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
        print(f"Gabim gjatë marrjes së imazhit për URL {product_url}: {e}")
    return "http://localhost:5001/static/images/product-placeholder.jpg"

def fetch_product_details(product_url):
    """Merr imazhin, titullin dhe çmimin e produktit nga faqja e Amazon"""
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
        print(f"\nTrying to fetch details for URL: {product_url}")
        response = requests.get(product_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Failed to fetch URL. Status code: {response.status_code}")
            return {
                "image_url": DEFAULT_IMAGE_URL,
                "title": None,
                "price": 0.0
            }
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Improved image scraping with multiple selectors
        image_url = DEFAULT_IMAGE_URL
        
        # Try different image selectors in order of preference
        image_selectors = [
            {"id": "landingImage"},  # Main product image
            {"id": "imgBlkFront"},   # Alternative main image
            {"class": "a-dynamic-image"},  # Dynamic images
            {"class": "s-image"},    # Search results image
            {"id": "main-image"},    # Another possible main image
            {"id": "product-image"}, # Another possible image ID
            {"class": "image-block"}, # Another possible class
            {"class": "product-image-container"} # Another possible container
        ]
        
        print("Trying to find image with selectors:")
        for selector in image_selectors:
            print(f"Trying selector: {selector}")
            image_tags = soup.find_all("img", selector)
            
            for image_tag in image_tags:
                print(f"Found image tag: {image_tag}")
                # Try different image URL attributes
                for attr in ['src', 'data-src', 'data-a-dynamic-image', 'data-old-hires', 'data-zoom-hires']:
                    img_url = image_tag.get(attr)
                    print(f"Checking attribute {attr}: {img_url}")
                    
                    if img_url:
                        if attr == 'data-a-dynamic-image':
                            try:
                                import json
                                urls = json.loads(img_url)
                                if urls:
                                    image_url = list(urls.keys())[0]
                                    print(f"Found dynamic image URL: {image_url}")
                                    break
                            except Exception as e:
                                print(f"Error parsing dynamic image: {e}")
                                continue
                        else:
                            image_url = img_url
                            print(f"Found image URL: {image_url}")
                            break
                
                if image_url != DEFAULT_IMAGE_URL:
                    break
            
            if image_url != DEFAULT_IMAGE_URL:
                break
        
        # Clean up the image URL
        if image_url and image_url != DEFAULT_IMAGE_URL:
            # Handle different URL patterns
            if '._' in image_url:
                # Remove any size constraints in the URL to get the full-size image
                base_url = image_url.split('._')[0]
                image_url = f"{base_url}._V1_FMjpg_UX1000_.jpg"
            elif '_SL' in image_url:
                # Handle another common Amazon image URL pattern
                base_url = image_url.split('_SL')[0]
                image_url = f"{base_url}_SL1500_.jpg"
                
            print(f"Final image URL: {image_url}")
        else:
            print("No image found, using default image")
        
        # Get title and price
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
    """Merr produktet për një kategori specifike"""
    try:
        search_terms = CATEGORY_MAPPING.get(category_type.lower(), [])
        
        if not search_terms:
            print(f"Nuk u gjetën terma kërkimi për kategorinë: {category_type}")
            return {"products": [], "total": 0, "page": page, "per_page": per_page, "total_pages": 0}

        conditions = " OR ".join([
            "LOWER(p.ProductType) LIKE LOWER(:term" + str(i) + ")"
            for i in range(len(search_terms))
        ])

        query = text(f"""
            SELECT DISTINCT 
                p.ProductId,
                p.ProductType,
                p.Rating,
                p.URL,
                COUNT(*) as review_count,
                AVG(p.Rating) as avg_rating
            FROM amazon_beauty p
            WHERE ({conditions})
                AND p.ProductId IS NOT NULL
                AND p.URL IS NOT NULL
            GROUP BY p.ProductId, p.ProductType, p.Rating, p.URL
            ORDER BY p.Rating DESC
        """)

        with engine.connect() as conn:
            params = {f"term{i}": term for i, term in enumerate(search_terms)}
            result = conn.execute(query, params)
            
            products = []
            for row in result:
                try:
                    # Add delay between requests
                    # time.sleep(1)  # Wait 2 seconds between requests
                    
                    # First check if product exists in products table
                    check_query = text("""
                        SELECT ProductId, ProductType, ProductTitle, URL, ImageURL, price
                        FROM products 
                        WHERE ProductId = :product_id
                    """)
                    
                    product_result = conn.execute(check_query, {"product_id": row.ProductId}).fetchone()
                    
                    if product_result:
                        print(f"Found product {row.ProductId} in database, skipping scraping")
                        product_details = {
                            "image_url": product_result.ImageURL,
                            "title": product_result.ProductTitle,
                            "price": float(product_result.price if product_result.price is not None else 0)
                        }
                    else:
                        print(f"Product {row.ProductId} not found in database, scraping details")
                        product_details = fetch_product_details(row.URL)
                        
                        product_data = {
                            "ProductId": row.ProductId,
                            "ProductType": row.ProductType,
                            "ProductTitle": product_details["title"] or "",
                            "URL": row.URL,
                            "ImageURL": product_details["image_url"],
                            "price": float(product_details["price"] if product_details["price"] is not None else 0)
                        }
                        
                        # Insert the new product
                        check_and_insert_product(engine, product_data)
                    
                    products.append({
                        "ProductId": row.ProductId,
                        "ProductType": row.ProductType,
                        "ProductTitle": product_details["title"],
                        "Rating": float(row.avg_rating),
                        "URL": row.URL,
                        "ReviewCount": row.review_count,
                        "ImageURL": product_details["image_url"],
                        "price": round(float(product_details["price"] if product_details["price"] is not None else 0), 2),
                        "currency": "EUR"
                    })
                    
                except Exception as e:
                    print(f"Gabim gjatë krijimit të produktit: {str(e)}")
                    continue
            
            return {
                "products": products,
                "total": len(products),
                "page": 1,
                "per_page": len(products),
                "total_pages": 1
            }

    except Exception as e:
        print(f"Error in get_category_products: {str(e)}")
        return {
            "products": [],
            "total": 0,
            "page": 1,
            "per_page": 0,
            "total_pages": 1
        }

def get_all_product_types(engine):
    """Merr të gjitha ProductType-t unike nga databaza"""
    try:
        query = text("""
            SELECT DISTINCT 
                ProductType,
                COUNT(*) as count,
                AVG(Rating) as avg_rating
            FROM amazon_beauty
            WHERE ProductType IS NOT NULL
            GROUP BY ProductType
            ORDER BY count DESC, avg_rating DESC;
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query)
            product_types = [{
                "type": row.ProductType,
                "count": row.count,
                "avg_rating": float(row.avg_rating)
            } for row in result]
            
            print("\nTë gjitha ProductType-t në databazë:")
            for pt in product_types:
                print(f"- {pt['type']}: {pt['count']} produkte, Rating mesatar: {pt['avg_rating']:.2f}")
            
            return product_types
            
    except Exception as e:
        print(f"Ndodhi një gabim gjatë marrjes së product types: {str(e)}")
        return []

def check_and_insert_product(engine, product_data):
    """Check if product exists and insert if it doesn't"""
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
                    # Insert new product
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
                    # Update price if provided
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

def test_product_insertion(engine):
    """Test function to verify product insertion"""
    test_product = {
        "ProductId": "TEST123",
        "ProductType": "Test Product",
        "ProductTitle": "Test Title",
        "URL": "http://test.com",
        "ImageURL": "http://test.com/image.jpg",
        "price": 0.0
    }
    
    print("\nTesting product insertion...")
    success = check_and_insert_product(engine, test_product)
    
    if success:
        print("Test insertion successful!")
        # Verify the product exists
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM products WHERE ProductId = :pid"),
                {"pid": "TEST123"}
            ).fetchone()
            if result:
                # Convert row to dict properly
                row_dict = {key: value for key, value in zip(result.keys(), result)}
                print(f"Found test product in database: {row_dict}")
            else:
                print("Warning: Product was supposedly inserted but not found!")
    else:
        print("Test insertion failed!")

def reset_table_auto_increment(engine, table_name):
    """Reset auto-increment counter for a table"""
    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1"))
                print(f"Reset auto-increment counter for table {table_name}")
    except Exception as e:
        print(f"Error resetting auto-increment for {table_name}: {str(e)}")

def delete_category_products(engine, category_type):
    """Delete products from a specific category"""
    try:
        # Get the search terms for the category
        search_terms = CATEGORY_MAPPING.get(category_type.lower(), [])
        
        if not search_terms:
            print(f"No search terms found for category: {category_type}")
            return False
            
        # Build the conditions for the category
        conditions = " OR ".join([
            f"ProductType LIKE '{term.replace('%', '')}'"
            for term in search_terms
        ])
        
        with engine.connect() as conn:
            with conn.begin():
                # First, get count of products to be deleted
                count_query = text(f"""
                    SELECT COUNT(*) as count
                    FROM products
                    WHERE {conditions}
                """)
                count = conn.execute(count_query).scalar()
                
                # Delete the products
                delete_query = text(f"""
                    DELETE FROM products
                    WHERE {conditions}
                """)
                conn.execute(delete_query)
                
                # Reset auto-increment after deletion
                conn.execute(text("ALTER TABLE products AUTO_INCREMENT = 1"))
                
                print(f"Deleted {count} products from category {category_type} and reset ID counter")
                return True
                
    except Exception as e:
        print(f"Error deleting products from category {category_type}: {str(e)}")
        return False

def delete_products_after_id(engine, start_id):
    """Delete products from amazon_beauty table starting from a specific ID"""
    try:
        with engine.connect() as conn:
            with conn.begin():
                # First, get count of products to be deleted
                count_query = text("""
                    SELECT COUNT(*) as count
                    FROM amazon_beauty
                    WHERE id >= :start_id
                """)
                count = conn.execute(count_query, {"start_id": start_id}).scalar()
                
                # Delete the products
                delete_query = text("""
                    DELETE FROM amazon_beauty
                    WHERE id >= :start_id
                """)
                conn.execute(delete_query, {"start_id": start_id})
                
                print(f"Deleted {count} products with ID >= {start_id} from amazon_beauty table")
                return True
                
    except Exception as e:
        print(f"Error deleting products after ID {start_id}: {str(e)}")
        return False

if __name__ == "__main__":
    engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
    setup_database(engine)  # This must complete successfully
    test_product_insertion(engine)  # Test the insertion
    
    # Delete products from specific categories
    categories_to_clear = ['haircare', 'fragrance']
    for category in categories_to_clear:
        delete_category_products(engine, category)
    # Delete products after a specific ID
    delete_products_after_id(engine, 605)  # Delete products with ID >= 605
