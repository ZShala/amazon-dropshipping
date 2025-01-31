import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from database_operations import get_data_from_db, get_product_recommendations
from sqlalchemy import create_engine
from functools import lru_cache
import time

# Cache për 1 orë
CACHE_TIMEOUT = 3600

class RecommendationCache:
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key):
        if key in self.cache:
            if time.time() - self.timestamps[key] < CACHE_TIMEOUT:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        return None
    
    def set(self, key, value):
        self.cache[key] = value
        self.timestamps[key] = time.time()

recommendation_cache = RecommendationCache()

@lru_cache(maxsize=1000)
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

@lru_cache(maxsize=100)
def get_recommendations_with_images(product_id, engine, top_n=10):
    try:
        # Kontrollojmë cache-in
        cached_recommendations = recommendation_cache.get(product_id)
        if cached_recommendations:
            print("Duke përdorur rekomandimet nga cache")
            return cached_recommendations

        # Nëse nuk janë në cache, i gjenerojmë
        df_clean = get_data_from_db(engine)
        if df_clean is None or df_clean.empty:
            return []
        
        if product_id not in df_clean['ProductId'].values:
            print(f"ProductId {product_id} nuk ekziston në dataset!")
            return []

        # Krijojmë TF-IDF matrix për ProductType
        tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = tfidf.fit_transform(df_clean['ProductType'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        try:
            idx = df_clean.index[df_clean['ProductId'] == product_id].tolist()[0]
        except IndexError:
            print(f"ProductId {product_id} nuk u gjet!")
            return []

        # Llogarisim similaritetin dhe marrim top N produktet
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]

        product_indices = [i[0] for i in sim_scores]

        # Krijojmë listën e rekomandimeve
        recommendations = []
        for i in product_indices:
            if i < len(df_clean):
                try:
                    product_row = df_clean.iloc[i]
                    combined_score = sim_scores[product_indices.index(i)][1] * product_row['Rating']
                    image_url = fetch_image(product_row['URL'])
                    recommendations.append({
                        "ProductId": product_row['ProductId'],
                        "ProductType": product_row['ProductType'],
                        "Rating": float(product_row['Rating']),
                        "CombinedScore": float(combined_score),
                        "ImageURL": image_url
                    })
                except IndexError:
                    continue

        # Rendisim sipas combined score
        recommendations = sorted(recommendations, key=lambda x: x['CombinedScore'], reverse=True)

        # Ruajmë në cache para se t'i kthejmë
        recommendation_cache.set(product_id, recommendations)
        return recommendations

    except Exception as e:
        print(f"Ndodhi një gabim: {str(e)}")
        return []

def main():
    # Krijojmë engine për testim
    engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
    
    # Test the recommendation system
    test_product_id = 'B00LLPT4HI'
    print(f"\nDuke testuar rekomandimet për produktin: {test_product_id}")
    
    recommended_products = get_recommendations_with_images(test_product_id, engine)
    
    if recommended_products:
        print("\nRekomandimet:")
        for i, product in enumerate(recommended_products, 1):
            print(f"\n{i}. Produkti:")
            print(f"   ID: {product['ProductId']}")
            print(f"   Tipi: {product['ProductType']}")
            print(f"   Rating: {product['Rating']}")
            print(f"   Score: {product['CombinedScore']:.2f}")
    else:
        print("Nuk u gjetën rekomandime")

if __name__ == "__main__":
    main()
