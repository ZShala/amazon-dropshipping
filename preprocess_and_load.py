import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, text
import numpy as np

# Lexojmë datasetin
df = pd.read_csv('./backend/amazon-beauty-recommendation.csv')

# Pastrimi i të dhënave
def preprocess_dataset(df):
    print("Duke pastruar të dhënat...")
    
    # Shfaqim kolonat që kemi në dataset
    print("\nKolonat në dataset:")
    print(df.columns.tolist())
    
    # Heqim rreshtat me vlera që mungojnë
    df = df.dropna()
    
    # Heqim duplikatet
    df = df.drop_duplicates()
    
    # Konvertojmë kolonat në tipin e duhur të të dhënave
    # Përdorim 'Rating' në vend të 'rating' pasi është emri i saktë i kolonës
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    
    # Nëse ka kolona të tjera numerike
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_numeric(df['Timestamp'], errors='coerce')
    
    # Pastrojmë tekstin në URL nëse ekziston
    if 'URL' in df.columns:
        df['URL'] = df['URL'].astype(str).str.strip()
    
    print("\nInformacion për datasetin e pastruar:")
    print(f"Numri total i rreshtave: {len(df)}")
    print(f"Numri i kolonave: {len(df.columns)}")
    print("\nShpërndarja e vlerave të Rating:")
    print(df['Rating'].value_counts().sort_index())
    
    return df

# Konfigurimi i lidhjes me MySQL
def create_mysql_connection():
    engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
    return engine

# Funksioni kryesor
def main():
    try:
        # Lexojmë datasetin në chunks për performancë më të mirë
        chunk_size = 100000
        chunks = []
        
        print("Duke lexuar datasetin në chunks...")
        for chunk in pd.read_csv('./backend/amazon-beauty-recommendation.csv', 
                               chunksize=chunk_size):
            chunks.append(chunk)
        
        df = pd.concat(chunks)
        print(f"U lexuan {len(df)} rreshta në total")
        
        # Preprocessimi i dataset
        cleaned_df = preprocess_dataset(df)
        
        # Krijojmë lidhjen me MySQL
        print("\nDuke u lidhur me databasën...")
        engine = create_mysql_connection()
        
        # Ngarkojmë të dhënat në MySQL me chunks
        print("Duke ngarkuar të dhënat në MySQL...")
        cleaned_df.to_sql('amazon_beauty', 
                         engine, 
                         if_exists='replace',
                         index=False,
                         chunksize=10000)
        
        # Krijojmë indekset për performancë më të mirë
        with engine.connect() as conn:
            print("\nDuke krijuar indekset...")
            # Shtojmë gjatësinë maksimale për kolonat tekst (p.sh. 255 karaktere)
            conn.execute(text("ALTER TABLE amazon_beauty ADD INDEX idx_product_id (ProductId(255))"))
            conn.execute(text("ALTER TABLE amazon_beauty ADD INDEX idx_user_id (UserId(255))"))
            conn.execute(text("ALTER TABLE amazon_beauty ADD INDEX idx_rating (Rating)"))
        
        print("\nProcesi përfundoi me sukses!")
        
    except Exception as e:
        print(f"\nNdodhi një gabim: {str(e)}")

def check_data():
    try:
        engine = create_mysql_connection()
        
        with engine.connect() as conn:
            # Numri total i rreshtave
            result = conn.execute(text("SELECT COUNT(*) FROM amazon_beauty"))
            count = result.scalar()
            print(f"\nNumri total i rreshtave në databazë: {count}")
            
            # Statistika për secilën kolonë
            print("\nStatistikat për kolonat:")
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
            print(f"Përdorues unikë: {stats[0]}")
            print(f"Produkte unike: {stats[1]}")
            print(f"Rating minimal: {stats[2]}")
            print(f"Rating maksimal: {stats[3]}")
            print(f"Rating mesatar: {round(stats[4], 2)}")
            
            # Madhësia e tabelës në MB
            result = conn.execute(text("""
                SELECT 
                    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
                FROM information_schema.tables
                WHERE table_schema = 'dataset_db' 
                AND table_name = 'amazon_beauty'
            """))
            size = result.scalar()
            print(f"\nMadhësia e tabelës: {size} MB")
            
    except Exception as e:
        print(f"\nNdodhi një gabim: {str(e)}")

# Thirre funksionin në fund të main()
if __name__ == "__main__":
    main()
    check_data() 