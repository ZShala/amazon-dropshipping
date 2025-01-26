import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import Image, display

df = pd.read_csv('amazon-beauty-recommendation.csv')
df_clean = df.dropna(subset=['ProductId', 'ProductType', 'Rating', 'Timestamp', 'URL'])
df_clean = df_clean.drop_duplicates(subset=['ProductId'])

tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = tfidf.fit_transform(df_clean['ProductType'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def fetch_image(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.find("img", {"id": "landingImage"})
        if image_tag:
            return image_tag.get("src")
    except Exception as e:
        print(f"Error fetching image for URL {product_url}: {e}")
    return "https://via.placeholder.com/150"

def get_recommendations_with_images(product_id, cosine_sim=cosine_sim):
    idx = df_clean.index[df_clean['ProductId'] == product_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    product_indices = [i[0] for i in sim_scores]

    recommendations = []
    for i in product_indices:
        product_row = df_clean.iloc[i]
        image_url = fetch_image(product_row['URL'])
        recommendations.append({
            "ProductId": product_row['ProductId'],
            "ProductType": product_row['ProductType'],
            "Rating": product_row['Rating'],
            "ImageURL": image_url
        })
    return recommendations

test_product_id = 'B00LLPT4HI'
recommended_products = get_recommendations_with_images(test_product_id)

for product in recommended_products:
    print(f"Product ID: {product['ProductId']}")
    print(f"Product Type: {product['ProductType']}")
    print(f"Rating: {product['Rating']}")
    display(Image(url=product['ImageURL']))
