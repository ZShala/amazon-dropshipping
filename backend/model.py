import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from bs4 import BeautifulSoup
import requests

url = "https://www.amazon.in/Maybelline-Colossal-Kajal-Black-0-35g/dp/B06WGZP21B/ref=lp_27061952031_1_1?sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the image URL (This depends on Amazon's page structure)
    image_tag = soup.find("img", {"id": "landingImage"})  # Replace 'landingImage' with the correct ID
    if image_tag:
        image_url = image_tag.get("src")
        print(f"Image URL: {image_url}")
        display(Image(url=image_url))
    else:
        print("Could not find the image on the page.")
except Exception as e:
    print(f"Error fetching image: {e}")


df = pd.read_csv('amazon-beauty-recommendation.csv')

print("First 5 rows of the dataset:")
print(df.head())

df_clean = df.dropna(subset=['ProductId', 'ProductType', 'Rating', 'Timestamp', 'URL'])

df_clean = df_clean.drop_duplicates(subset=['ProductId'])

print("Cleaned dataset:")
print(df_clean.head())

tfidf = TfidfVectorizer(stop_words='english', max_features=1000)

tfidf_matrix = tfidf.fit_transform(df_clean['ProductType'])

print("TF-IDF matrix shape:", tfidf_matrix.shape)

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(product_id, cosine_sim=cosine_sim):
  
    idx = df_clean.index[df_clean['ProductId'] == product_id].tolist()[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:11]
    product_indices = [i[0] for i in sim_scores]
    
    recommended_products = df_clean['ProductId'].iloc[product_indices].tolist()
    
    return recommended_products

test_product_id = 'B00LLPT4HI' 
recommended_products = get_recommendations(test_product_id, cosine_sim)

print(f"\nRecommended products for product ID '{test_product_id}':")
for product in recommended_products:
    print(f"- {product}")

sns.histplot(df_clean['Rating'], bins=20, kde=True)
plt.title('Distribution of Product Ratings')
plt.show()

rating_distribution = df_clean.groupby('ProductType')['Rating'].mean().sort_values()
rating_distribution.plot(kind='barh', figsize=(10, 6))
plt.title('Average Ratings per Product Type')
plt.xlabel('Average Rating')
plt.ylabel('Product Type')
plt.show()

