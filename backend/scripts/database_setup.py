from sqlalchemy import create_engine, text

DB_CONFIG = {
    'user': 'root',
    'password': 'mysqlZ97*',
    'host': 'localhost',
    'database': 'dataset_db'
}

def create_connection():
    try:
        engine = create_engine(f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")
        return engine
    except Exception as e:
        print(f"Error creating database connection: {e}")
        raise

def setup_database():
    engine = create_connection()
    
    try:
        with engine.connect() as conn:
            with conn.begin():
                conn.execute(text("DROP TABLE IF EXISTS amazon_beauty"))
                conn.execute(text("DROP TABLE IF EXISTS product_images"))
                conn.execute(text("DROP TABLE IF EXISTS products"))
                
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
                        INDEX idx_rating (Rating)
                    )
                """))
                
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        ProductId VARCHAR(255) UNIQUE,
                        ProductTitle TEXT,
                        ImageURL TEXT,
                        price DECIMAL(10,2)
                    )
                """))
                
                result = conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'dataset_db'
                """))
                
                print("\nCreated tables:")
                for row in result:
                    print(f"- {row[0]}")
                
        print("\nDatabase setup completed successfully!")
        
    except Exception as e:
        print(f"Error during database setup: {e}")
        raise

if __name__ == "__main__":
    setup_database() 