import mysql.connector
import pandas as pd

def merr_te_dhenat():
    db = mysql.connector.connect(
        host="localhost",
        user="përdoruesi_juaj",
        password="fjalëkalimi_juaj",
        database="emri_databazes"
    )
    
    # Përdorni pandas për të lexuar të dhënat direkt nga MySQL
    query = "SELECT * FROM te_dhenat"
    df = pd.read_sql(query, db)
    
    db.close()
    return df

# Përdorimi
te_dhenat = merr_te_dhenat() 