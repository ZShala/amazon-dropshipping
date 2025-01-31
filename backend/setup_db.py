from sqlalchemy import create_engine, text

def create_images_table():
    try:
        engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
        
        with engine.begin() as conn:
            # Drop table nëse ekziston
            conn.execute(text("DROP TABLE IF EXISTS product_images"))
            
            # Krijo tabelën
            conn.execute(text("""
                CREATE TABLE product_images (
                    asin VARCHAR(20) PRIMARY KEY,
                    image_url VARCHAR(500) NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_last_updated (last_updated)
                ) ENGINE=InnoDB
            """))
            
            # Verifiko nëse tabela u krijua
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'dataset_db' 
                AND table_name = 'product_images'
            """))
            
            if result.scalar():
                print("Tabela u krijua me sukses!")
                
                # Shfaq strukturën
                desc = conn.execute(text("DESCRIBE product_images"))
                print("\nStruktura e tabelës:")
                for row in desc:
                    print(row)
            else:
                print("Gabim: Tabela nuk u krijua!")
                
    except Exception as e:
        print(f"Gabim: {str(e)}")

if __name__ == "__main__":
    create_images_table() 