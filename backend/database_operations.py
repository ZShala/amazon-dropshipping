import pandas as pd
from sqlalchemy import text, Table, Column, String, MetaData, create_engine
from bs4 import BeautifulSoup
import requests

def setup_database(engine):
    """Krijon tabelat dhe indekset e nevojshme në databazë"""
    try:
        with engine.connect() as conn:
            # Krijojmë tabelën amazon_beauty
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
            
            # Krijojmë tabelën product_images
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS product_images (
                    asin VARCHAR(20) PRIMARY KEY,
                    image_url VARCHAR(500) NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_last_updated (last_updated)
                ) ENGINE=InnoDB
            """))
            
            print("Tabelat dhe indekset u krijuan me sukses!")
            
            # Kontrollo nëse tabelat u krijuan
            tables = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'dataset_db'
            """))
            print("\nTabelat e krijuara:")
            for table in tables:
                print(f"- {table.table_name}")
            
    except Exception as e:
        print(f"Ndodhi një gabim gjatë setup të databazës: {str(e)}")

def get_data_from_db(engine):
    """Merr të dhënat nga databaza duke përdorur engine-in e dhënë"""
    try:
        # Optimizojmë query-n duke marrë vetëm produktet më të mira
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
                AND Rating >= 4.0  -- Vetëm produktet me rating të lartë
            HAVING review_count >= 3  -- Vetëm produktet me mjaftueshëm reviews
            ORDER BY avg_rating DESC, review_count DESC
            LIMIT 1000  -- Limitojmë numrin total të produkteve për performancë
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
                # Backup: Produktet më popullore nga e njëjta kategori
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
                return {
                    "ProductId": result.ProductId,
                    "ProductType": result.ProductType,
                    "Rating": float(result.Rating),
                    "URL": result.URL
                }
            return None
            
    except Exception as e:
        print(f"Ndodhi një gabim gjatë marrjes së detajeve të produktit: {str(e)}")
        return None

def get_cart_recommendations(engine, product_ids):
    """Merr rekomandimet për produktet në cart"""
    try:
        # Query për cross-sell (produkte komplementare)
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

        # Query për up-sell (produkte premium)
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
            # Ekzekuto queries
            cross_sell_result = conn.execute(
                cross_sell_query, 
                {"product_ids": tuple(product_ids)}
            )
            up_sell_result = conn.execute(
                up_sell_query, 
                {"product_ids": tuple(product_ids)}
            )

            # Formato rezultatet
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

def get_and_save_image_url(conn, url, asin):
    try:
        # Kontrollo nëse tabela ekziston
        check_table = text("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'dataset_db' 
            AND table_name = 'product_images'
        """)
        table_exists = conn.execute(check_table).scalar()
        print(f"Table exists: {table_exists}")

        if not table_exists:
            print("Creating product_images table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS product_images (
                    asin VARCHAR(20) PRIMARY KEY,
                    image_url VARCHAR(500) NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_last_updated (last_updated)
                ) ENGINE=InnoDB
            """))

        # Kontrollo nëse imazhi ekziston në databazë
        query = text("SELECT image_url, last_updated FROM product_images WHERE asin = :asin")
        result = conn.execute(query, {"asin": asin}).fetchone()
        
        if result:
            print(f"Found cached image for ASIN {asin} from {result.last_updated}")
            return result.image_url

        print(f"Trying to find image for ASIN: {asin}")
        
        # Lista e formateve të mundshme të imazheve Amazon
        image_formats = [
            f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg",
            f"https://m.media-amazon.com/images/I/{asin}._AC_SX466_.jpg",
            f"https://m.media-amazon.com/images/I/{asin}._AC_SX425_.jpg",
            f"https://m.media-amazon.com/images/I/{asin}._AC_SX522_.jpg",
            f"https://m.media-amazon.com/images/I/{asin}._AC_SL1500_.jpg",
            f"https://m.media-amazon.com/images/I/{asin}._AC_SY300_.jpg",
            f"https://m.media-amazon.com/images/I/{asin}.jpg"
        ]

        # Testo secilin format
        for image_url in image_formats:
            try:
                print(f"Trying URL: {image_url}")
                response = requests.head(image_url, timeout=2)
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"Found working image URL: {image_url}")
                    
                    # Ruaj URL-në që funksionon në databazë
                    insert_query = text("""
                        INSERT INTO product_images (asin, image_url, last_updated)
                        VALUES (:asin, :image_url, NOW())
                        ON DUPLICATE KEY UPDATE 
                            image_url = :image_url,
                            last_updated = NOW()
                    """)
                    
                    try:
                        conn.execute(insert_query, {
                            "asin": asin,
                            "image_url": image_url
                        })
                        print(f"Successfully saved image URL to database for ASIN {asin}")
                    except Exception as e:
                        print(f"Error saving to database: {str(e)}")
                    
                    return image_url
                    
            except Exception as e:
                print(f"Error checking URL {image_url}: {str(e)}")
                continue

        # Default URL nëse asnjë format nuk funksionon
        default_url = f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg"
        print(f"Using default URL: {default_url}")
        
        try:
            insert_query = text("""
                INSERT INTO product_images (asin, image_url, last_updated)
                VALUES (:asin, :image_url, NOW())
                ON DUPLICATE KEY UPDATE 
                    image_url = :image_url,
                    last_updated = NOW()
            """)
            
            conn.execute(insert_query, {
                "asin": asin,
                "image_url": default_url
            })
            print(f"Saved default URL to database for ASIN {asin}")
        except Exception as e:
            print(f"Error saving default URL: {str(e)}")
        
        return default_url
        
    except Exception as e:
        print(f"Major error in get_and_save_image_url: {str(e)}")
        return f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg"

def get_image_url_with_scraping(url, asin):
    """Merr URL-në e imazhit duke përdorur BeautifulSoup"""
    try:
        print(f"\nDuke bërë scrape URL: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            print("Duke përdorur URL default për shkak të status kodit")
            return f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg"
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Lista e të gjitha metodave për të gjetur imazhin
        image_selectors = [
            # Metoda 1: data-old-hires
            lambda: soup.find('img', {'data-old-hires': True})['data-old-hires'],
            
            # Metoda 2: landingImage
            lambda: soup.find('img', {'id': 'landingImage'})['src'],
            
            # Metoda 3: imgBlkFront
            lambda: soup.find('img', {'id': 'imgBlkFront'})['src'],
            
            # Metoda 4: main-image-container
            lambda: soup.find('div', {'id': 'main-image-container'}).find('img')['src'],
            
            # Metoda 5: image në main
            lambda: soup.find('main').find('img')['src'],
            
            # Metoda 6: të gjitha imazhet që përmbajnë ASIN
            lambda: next(img['src'] for img in soup.find_all('img') 
                        if img.get('src') and asin in img['src']),
            
            # Metoda 7: imazhi i parë në faqe
            lambda: soup.find('img')['src']
        ]
        
        # Provo çdo metodë
        for i, selector in enumerate(image_selectors, 1):
            try:
                image_url = selector()
                if image_url:
                    print(f"U gjet imazhi me metodën {i}: {image_url}")
                    
                    # Kontrollo nëse URL është relative
                    if image_url.startswith('//'):
                        image_url = 'https:' + image_url
                    
                    # Kontrollo nëse është imazh valid
                    if any(ext in image_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                        return image_url
            except Exception as e:
                print(f"Metoda {i} dështoi: {str(e)}")
                continue
        
        # Nëse asnjë metodë nuk funksionon, përdor formatin default
        print("Duke përdorur URL default pasi asnjë metodë nuk funksionoi")
        return f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg"
        
    except Exception as e:
        print(f"Error kryesor në scraping: {str(e)}")
        return f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg"

def get_category_products(engine, category_type, page=1, per_page=None):
    """Merr produktet për një kategori specifike"""
    try:
        # Mapping i kategorive me termat e kërkimit
        category_mapping = {
            'makeup': [
                '%Eyeliner%',
                '%Kajal%',
                '%Lipstick%',
                '%Foundation%',
                '%Mascara%',
                '%Eye Shadow%',
                '%Concealer%',
                '%Blush%',
                '%Compact%',
                '%Powder%',
                '%Nail%',
                '%Makeup%'
            ],
            'skincare': [
                '%Face%',
                '%Skin%',
                '%Cream%',
                '%Moisturizer%',
                '%Serum%',
                '%Mask%',
                '%Facial%',
                '%Cleanser%',
                '%Toner%',
                '%Lotion%'
            ],
            'haircare': [
                '%Hair%',
                '%Shampoo%',
                '%Conditioner%',
                '%Scalp%'
            ],
            'fragrance': [
                '%Perfume%',
                '%Fragrance%',
                '%Body Spray%',
                '%Deodorant%',
                '%Scent%'
            ],
            'miscellaneous': [
                '%Tool%',
                '%Kit%',
                '%Accessory%',
                '%Accessories%',
                '%Brush%',
                '%Applicator%',
                '%Beauty Tool%',
                '%Makeup Tool%'
            ]
        }

        search_terms = category_mapping.get(category_type.lower(), [])
        
        if not search_terms:
            print(f"Nuk u gjetën terma kërkimi për kategorinë: {category_type}")
            return {"products": [], "total": 0, "page": page, "per_page": per_page, "total_pages": 0}

        conditions = " OR ".join([
            "LOWER(p.ProductType) LIKE LOWER(:term" + str(i) + ")"
            for i in range(len(search_terms))
        ])

        # Query për të marrë totalin e produkteve
        count_query = text(f"""
            SELECT COUNT(DISTINCT p.ProductId) as total
            FROM amazon_beauty p
            WHERE ({conditions})
                AND p.ProductId IS NOT NULL
                AND p.URL IS NOT NULL
        """)

        # Query kryesore pa pagination
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
                    url = row.URL
                    url_parts = url.split('/')
                    asin = next((part for part in url_parts 
                               if part.startswith('B0') or part.startswith('A0')), None)
                    
                    # Krijo URL-në e imazhit
                    image_url = f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg"
                    
                    print(f"Processing product: {asin} -> {image_url}")  # Shto logging
                    
                    products.append({
                        "ProductId": row.ProductId,
                        "ProductType": row.ProductType,
                        "Rating": float(row.avg_rating),
                        "URL": row.URL,
                        "ReviewCount": row.review_count,
                        "ImageURL": image_url,
                        "ASIN": asin  # Shto ASIN në response
                    })
                    
                except Exception as e:
                    print(f"Error creating product: {str(e)}")
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

def check_image_cache(engine):
    """Kontrollon përmbajtjen e cache-it të imazheve"""
    try:
        query = text("""
            SELECT asin, image_url, last_updated 
            FROM product_images 
            ORDER BY last_updated DESC 
            LIMIT 10
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query)
            print("\nMost recent cached images:")
            for row in result:
                print(f"ASIN: {row.asin}")
                print(f"Image URL: {row.image_url}")
                print(f"Last Updated: {row.last_updated}")
                print("-" * 50)
            
            # Numri total i imazheve të ruajtura
            count_query = text("SELECT COUNT(*) as total FROM product_images")
            total = conn.execute(count_query).scalar()
            print(f"\nTotal cached images: {total}")
            
    except Exception as e:
        print(f"Error checking image cache: {str(e)}")

if __name__ == "__main__":
    engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
    setup_database(engine)
    check_image_cache(engine) 