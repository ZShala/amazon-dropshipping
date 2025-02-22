import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, text
import numpy as np

df = pd.read_csv('../data/amazon-beauty-recommendation.csv')

def preprocess_dataset(df):
    print("Cleaning data...")
    
    print("\nColumns in dataset:")
    print(df.columns.tolist())
    
    df = df.dropna()
    
    df = df.drop_duplicates()
    
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_numeric(df['Timestamp'], errors='coerce')
    
    if 'URL' in df.columns:
        df['URL'] = df['URL'].astype(str).str.strip()
    
    print("\nCleaned dataset information:")
    print(f"Total rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")
    print("\nRating value distribution:")
    print(df['Rating'].value_counts().sort_index())
    
    return df

def create_mysql_connection():
    engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
    return engine

def main():
    try:
        chunk_size = 100000
        chunks = []
        
        print("Reading dataset in chunks...")
        for chunk in pd.read_csv('../data/amazon-beauty-recommendation.csv', 
                               chunksize=chunk_size):
            chunks.append(chunk)
        
        df = pd.concat(chunks)
        print(f"Read {len(df)} rows in total")
        
        cleaned_df = preprocess_dataset(df)
        
        print("\nConnecting to database...")
        engine = create_mysql_connection()
        
        print("Loading data into MySQL...")
        cleaned_df.to_sql('amazon_beauty', 
                         engine, 
                         if_exists='replace',
                         index=False,
                         chunksize=10000)
        
        with engine.connect() as conn:
            print("\nCreating indexes...")
            conn.execute(text("ALTER TABLE amazon_beauty ADD INDEX idx_product_id (ProductId(255))"))
            conn.execute(text("ALTER TABLE amazon_beauty ADD INDEX idx_user_id (UserId(255))"))
            conn.execute(text("ALTER TABLE amazon_beauty ADD INDEX idx_rating (Rating)"))
        
        print("\nProcess completed successfully!")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

def check_data():
    try:
        engine = create_mysql_connection()
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM amazon_beauty"))
            count = result.scalar()
            print(f"\nTotal rows in database: {count}")
            
            print("\nColumn statistics:")
            result = conn.execute(text("""
                SELECT 
                    COUNT(DISTINCT UserId) as unique_users,
                    COUNT(DISTINCT ProductId) as unique_products,
                    MIN(Rating) as min_rating,
                    MAX(Rating) as max_rating,
                    AVG(Rating) as avg_rating
                FROM amazon_beauty
            """))
            stats = result.fetchone()
            print(f"Unique users: {stats[0]}")
            print(f"Unique products: {stats[1]}")
            print(f"Minimum rating: {stats[2]}")
            print(f"Maximum rating: {stats[3]}")
            print(f"Average rating: {round(stats[4], 2)}")
            
            result = conn.execute(text("""
                SELECT 
                    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
                FROM information_schema.tables
                WHERE table_schema = 'dataset_db' 
                AND table_name = 'amazon_beauty'
            """))
            size = result.scalar()
            print(f"\nTable size: {size} MB")
            
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
    check_data() 