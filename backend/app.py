import pandas as pd
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

df = pd.read_csv('amazon-beauty-recommendation.csv')
df_clean = df.dropna(subset=['ProductId', 'ProductType', 'Rating', 'Timestamp', 'URL'])
df_clean = df_clean.drop_duplicates(subset=['ProductId'])

tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = tfidf.fit_transform(df_clean['ProductType'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to fetch image URL from product page
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
    return "https://via.placeholder.com/150"  # Fallback image

# Function to get recommendations along with product details
def get_recommendations(product_id, cosine_sim=cosine_sim):
    try:
        idx = df_clean.index[df_clean['ProductId'] == product_id].tolist()[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Get top 10 recommendations
        product_indices = [i[0] for i in sim_scores]

        recommendations = []
        for i in product_indices:
            product_row = df_clean.iloc[i]
            image_url = fetch_image(product_row['URL'])
            recommendations.append({
                "ProductId": product_row['ProductId'],
                "ProductType": product_row['ProductType'],
                "Rating": float(product_row['Rating']),  # Convert Rating to float
                "ImageURL": image_url
            })
        return recommendations
    except IndexError:
        return []

@app.route('/recommendations', methods=['GET'])
def recommendations():
    product_id = request.args.get('product_id')
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    recommendations = get_recommendations(product_id)
    return jsonify({'product_id': product_id, 'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)
