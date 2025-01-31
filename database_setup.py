import mysql.connector
import pandas as pd
from mysql.connector import Error

try:
    # Krijoni lidhjen me MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysqlZ97*",
        database="dataset_db",
        # Shtojmë parametra shtesë për kompatibilitet
        auth_plugin='mysql_native_password'
    )
    
    if db.is_connected():
        print("Lidhja me databazën u krye me sukses!")
        print(f"Versioni i MySQL: {db.get_server_info()}")
        
        # Krijoni një cursor për të ekzekutuar queries
        cursor = db.cursor()
        
        # Krijoni tabelën me kolonat që përputhen me CSV-në tuaj
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS te_dhenat (
                id INT AUTO_INCREMENT PRIMARY KEY,
                # Këtu duhet të listoni kolonat që keni në CSV
                # Për shembull:
                emri VARCHAR(255),
                mosha INT,
                paga FLOAT
                # ... shtoni kolonat e tjera
            )
        """)
        
        # Lexoni dataset-in
        df = pd.read_csv('dataset_juaj.csv')
        
        # Konvertoni të dhënat
        values = df.values.tolist()
        
        # Query për insert
        insert_query = """
            INSERT INTO te_dhenat (kolona1, kolona2, kolona3) 
            VALUES (%s, %s, %s)
        """
        
        # Insertoni të dhënat
        cursor.executemany(insert_query, values)
        db.commit()
        print("Të dhënat u insertuan me sukses!")

except Error as e:
    print(f"Gabim gjatë lidhjes me MySQL: {e}")
    
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
        print("Lidhja me MySQL u mbyll") 