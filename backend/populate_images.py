from sqlalchemy import create_engine, text
import requests
import time

def populate_image_cache(limit=10):
    """Mbush tabelën product_images me imazhe nga produktet ekzistuese"""
    try:
        engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
        
        with engine.begin() as conn:
            # Verifiko nëse tabela ekziston
            table_check = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'dataset_db' 
                AND table_name = 'product_images'
            """)).scalar()
            
            if not table_check:
                print("Tabela product_images nuk ekziston!")
                return
                
            print("Tabela product_images ekziston.")
            
            # Merr produktet
            products = conn.execute(text("""
                SELECT DISTINCT URL 
                FROM amazon_beauty 
                WHERE URL IS NOT NULL 
                AND URL != ''
                AND URL LIKE '%amazon%'
                LIMIT :limit
            """), {"limit": limit}).fetchall()
            
            print(f"U gjetën {len(products)} produkte.")
            
            for i, row in enumerate(products, 1):
                url = row[0]
                print(f"\nPërpunimi {i}: {url}")
                
                try:
                    # Ekstrakto ASIN
                    asin = next((part for part in url.split('/') 
                               if part.startswith(('B0', 'A0'))), None)
                    
                    if not asin:
                        print(f"Nuk u gjet ASIN për {url}")
                        continue
                        
                    print(f"ASIN: {asin}")
                    
                    # Krijo URL-në e imazhit
                    image_url = f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg"
                    print(f"Image URL: {image_url}")
                    
                    # Ruaj në databazë
                    conn.execute(text("""
                        INSERT INTO product_images (asin, image_url, last_updated)
                        VALUES (:asin, :image_url, NOW())
                        ON DUPLICATE KEY UPDATE 
                            image_url = :image_url,
                            last_updated = NOW()
                    """), {
                        "asin": asin,
                        "image_url": image_url
                    })
                    
                    # Verifiko nëse u ruajt
                    verify = conn.execute(text("""
                        SELECT * FROM product_images WHERE asin = :asin
                    """), {"asin": asin}).fetchone()
                    
                    if verify:
                        print(f"U ruajt me sukses: {verify.asin} -> {verify.image_url}")
                    else:
                        print("Nuk u ruajt!")
                    
                except Exception as e:
                    print(f"Gabim për {url}: {str(e)}")
                
            # Shfaq përmbajtjen e tabelës
            results = conn.execute(text("SELECT * FROM product_images")).fetchall()
            print("\nPërmbajtja e tabelës:")
            for row in results:
                print(f"ASIN: {row.asin}, URL: {row.image_url}")
            
    except Exception as e:
        print(f"Gabim i përgjithshëm: {str(e)}")

if __name__ == "__main__":
    print("Duke filluar populimin e imazheve...")
    populate_image_cache(limit=3)
    print("Përfundoi!") 