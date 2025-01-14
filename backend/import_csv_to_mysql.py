# import pandas as pd
# import mysql.connector
# from datetime import datetime

# df = pd.read_csv('amazon-beauty-recommendation.csv')

# def convert_unix_to_datetime(timestamp):
#     try:
#         return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
#     except Exception as e:
#         print(f"Error converting timestamp {timestamp}: {e}")
#         return None

# db_config = {
#     'host': 'localhost', 
#     'user': 'root', 
#     'password': '',  
#     'database': 'product_recommendation'
# }

# def get_db_connection():
#     return mysql.connector.connect(
#         host=db_config['host'],
#         user=db_config['user'],
#         password=db_config['password'],
#         database=db_config['database']
#     )

# def insert_data_to_db(df):
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     insert_query = """
#     INSERT INTO products (ProductId, ProductType, Rating, Timestamp, URL)
#     VALUES (%s, %s, %s, %s, %s)
#     """
    
#     for index, row in df.iterrows():
#         timestamp = convert_unix_to_datetime(row['Timestamp']) 
#         if timestamp:
#             cursor.execute(insert_query, (row['ProductId'], row['ProductType'], row['Rating'], timestamp, row['URL']))
    
#     connection.commit() 
#     cursor.close()
#     connection.close()

# insert_data_to_db(df)
# print("Data inserted successfully.")
