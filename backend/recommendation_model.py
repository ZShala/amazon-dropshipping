import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
from functools import lru_cache
from sklearn.preprocessing import MinMaxScaler
from collections import defaultdict
from datetime import datetime, timedelta

def get_db():
    try:
        engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
        return engine
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise e

def get_recommendations(product_id, num_recommendations=4):
    """Funksioni kryesor për rekomandimet"""
    try:
        print(f"Starting recommendations for product: {product_id}")
        engine = get_db()
        recommender = AdvancedRecommendationEngine(engine)
        recommendations = recommender.get_similar_products(product_id, num_recommendations)
        print(f"Found {len(recommendations)} recommendations")
        return recommendations
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def fetch_image(product_url):
    if not product_url:
        return None
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        image_tag = (
            soup.find("img", {"id": "landingImage"}) or
            soup.find("img", {"id": "main-image"}) or
            soup.find("img", {"class": "product-image"})
        )
        
        if image_tag and image_tag.get("src"):
            image_url = image_tag.get("src")
            
            if image_url.startswith('http') and any(ext in image_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                return image_url
                
    except Exception as e:
        print(f"Error fetching image for URL {product_url}: {e}")
    return None

def get_recommendations_with_images(product_id):
    """Funksioni për rekomandimet me imazhe"""
    try:
        print(f"Getting recommendations with images for product: {product_id}")
        recommendations = get_recommendations(product_id)
        
        if not recommendations:
            print("No recommendations found")
            return []
            
        print(f"Processing images for {len(recommendations)} recommendations")
        
        for rec in recommendations:
            try:
                if not rec.get('ImageURL') or 'placeholder' in rec['ImageURL']:
                    query = text("""
                        SELECT ImageURL, URL 
                        FROM products 
                        WHERE ProductId = :product_id
                    """)
                    
                    with get_db().connect() as conn:
                        result = conn.execute(query, {"product_id": rec['ProductId']}).fetchone()
                        
                        if result and result.ImageURL:
                            rec['ImageURL'] = result.ImageURL
                        else:
                            rec['ImageURL'] = "http://localhost:5001/static/images/product-placeholder.jpg"
                            
            except Exception as e:
                print(f"Error processing image for product {rec['ProductId']}: {str(e)}")
                rec['ImageURL'] = "http://localhost:5001/static/images/product-placeholder.jpg"
                
        return recommendations
        
    except Exception as e:
        print(f"Error in get_recommendations_with_images: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

class AdvancedRecommendationEngine:
    def __init__(self, engine):
        self.engine = engine
        self.tfidf = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 2),
            min_df=0.01,
            max_features=1000,
            stop_words='english'
        )
        self.memory_cache = {}

    def get_similar_products(self, product_id, num_recommendations=4):
        """Metoda kryesore për gjetjen e produkteve të ngjashme"""
        try:
            print(f"Finding similar products for: {product_id}")
            
            # Query për të marrë produktin aktual dhe produktet e ngjashme
            query = text("""
                WITH product_info AS (
                    SELECT 
                        p.ProductId,
                        p.ProductType,
                        p.price,
                        COALESCE(AVG(ab.Rating), 0) as avg_rating
                    FROM products p
                    LEFT JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
                    WHERE p.ProductId = :product_id
                    GROUP BY p.ProductId, p.ProductType, p.price
                )
                SELECT DISTINCT
                    p.ProductId,
                    p.ProductType,
                    p.ProductTitle,
                    p.ImageURL,
                    p.price,
                    COALESCE(AVG(ab.Rating), 0) as avg_rating,
                    COUNT(DISTINCT ab.UserId) as review_count,
                    pi.ProductType as original_type,
                    pi.price as original_price
                FROM products p
                LEFT JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
                CROSS JOIN product_info pi
                WHERE p.ProductId != :product_id
                AND p.ProductType LIKE CONCAT('%', pi.ProductType, '%')
                AND p.price BETWEEN (pi.price * 0.5) AND (pi.price * 1.5)
                GROUP BY 
                    p.ProductId, 
                    p.ProductType,
                    p.ProductTitle,
                    p.ImageURL,
                    p.price,
                    pi.ProductType,
                    pi.price
                HAVING avg_rating >= 4.0
                ORDER BY avg_rating DESC, review_count DESC
                LIMIT :limit
            """)

            print("Executing query...")
            with self.engine.connect() as conn:
                results = conn.execute(query, {
                    "product_id": product_id,
                    "limit": num_recommendations * 2
                }).fetchall()
                
                print(f"Found {len(results)} initial results")

                recommended_products = []
                for row in results:
                    try:
                        product = {
                            "ProductId": row.ProductId,
                            "ProductType": row.ProductType,
                            "ProductTitle": row.ProductTitle,
                            "ImageURL": row.ImageURL or "http://localhost:5001/static/images/product-placeholder.jpg",
                            "price": float(row.price) if row.price else 0.0,
                            "Rating": float(row.avg_rating),
                            "ReviewCount": row.review_count,
                            "similarity_score": 1.0
                        }
                        recommended_products.append(product)
                    except Exception as e:
                        print(f"Error processing product {row.ProductId}: {str(e)}")
                        continue

                print(f"Processed {len(recommended_products)} recommendations")
                return recommended_products[:num_recommendations]

        except Exception as e:
            print(f"Error in get_similar_products: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    def get_collaborative_recommendations(self, product_id, num_recommendations=4):
        """Rekomandimet bazuar në sjelljen e përdoruesve"""
        try:
            query = text("""
                WITH user_preferences AS (
                    SELECT 
                        ab1.UserId,
                        ab1.ProductId,
                        ab1.Rating
                    FROM amazon_beauty ab1
                    WHERE ab1.Rating >= 4.0
                ),
                similar_users AS (
                    SELECT DISTINCT 
                        up1.UserId
                    FROM user_preferences up1
                    WHERE up1.ProductId = :product_id
                ),
                recommended_products AS (
                    SELECT 
                        up2.ProductId,
                        COUNT(DISTINCT up2.UserId) as user_count,
                        AVG(up2.Rating) as avg_rating
                    FROM user_preferences up2
                    JOIN similar_users su ON up2.UserId = su.UserId
                    WHERE up2.ProductId != :product_id
                    GROUP BY up2.ProductId
                    HAVING avg_rating >= 4.0
                    ORDER BY user_count DESC, avg_rating DESC
                    LIMIT :limit
                )
                SELECT 
                    p.*,
                    rp.user_count,
                    rp.avg_rating
                FROM recommended_products rp
                JOIN products p ON rp.ProductId = p.ProductId
            """)

            with self.engine.connect() as conn:
                results = conn.execute(query, {
                    "product_id": product_id,
                    "limit": num_recommendations
                }).fetchall()

                return [{
                    "ProductId": row.ProductId,
                    "ProductType": row.ProductType,
                    "ProductTitle": row.ProductTitle,
                    "ImageURL": row.ImageURL or "http://localhost:5001/static/images/product-placeholder.jpg",
                    "price": float(row.price) if row.price else 0.0,
                    "Rating": float(row.avg_rating),
                    "UserCount": row.user_count,
                    "similarity_score": 0.8  # Peshë për collaborative filtering
                } for row in results]

        except Exception as e:
            print(f"Error in collaborative recommendations: {str(e)}")
            return []

    def get_trending_recommendations(self, product_id, num_recommendations=4):
        """Rekomandimet bazuar në trendet aktuale"""
        try:
            query = text("""
                WITH product_category AS (
                    SELECT ProductType 
                    FROM products 
                    WHERE ProductId = :product_id
                ),
                trending_products AS (
                    SELECT 
                        p.ProductId,
                        p.ProductType,
                        p.ProductTitle,
                        p.ImageURL,
                        p.price,
                        COUNT(DISTINCT ab.UserId) as recent_purchases,
                        AVG(ab.Rating) as avg_rating
                    FROM products p
                    JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
                    JOIN product_category pc ON p.ProductType LIKE CONCAT('%', pc.ProductType, '%')
                    WHERE p.ProductId != :product_id
                    AND ab.Timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                    GROUP BY p.ProductId, p.ProductType, p.ProductTitle, p.ImageURL, p.price
                    HAVING avg_rating >= 4.0
                    ORDER BY recent_purchases DESC, avg_rating DESC
                    LIMIT :limit
                )
                SELECT * FROM trending_products
            """)

            with self.engine.connect() as conn:
                results = conn.execute(query, {
                    "product_id": product_id,
                    "limit": num_recommendations
                }).fetchall()

                return [{
                    "ProductId": row.ProductId,
                    "ProductType": row.ProductType,
                    "ProductTitle": row.ProductTitle,
                    "ImageURL": row.ImageURL or "http://localhost:5001/static/images/product-placeholder.jpg",
                    "price": float(row.price) if row.price else 0.0,
                    "Rating": float(row.avg_rating),
                    "RecentPurchases": row.recent_purchases,
                    "similarity_score": 0.6  # Peshë për trending products
                } for row in results]

        except Exception as e:
            print(f"Error in trending recommendations: {str(e)}")
            return []

    def get_hybrid_recommendations(self, product_id, num_recommendations=4):
        """Kombinon të gjitha metodat e rekomandimit"""
        try:
            # Merr rekomandimet nga secila metodë
            similar_products = self.get_similar_products(product_id, num_recommendations)
            collaborative_recs = self.get_collaborative_recommendations(product_id, num_recommendations)
            trending_recs = self.get_trending_recommendations(product_id, num_recommendations)

            # Kombinon rezultatet me pesha
            product_scores = defaultdict(float)
            
            # Shton pikët për produktet e ngjashme (40%)
            for prod in similar_products:
                product_scores[prod['ProductId']] += 0.4 * prod['similarity_score']

            # Shton pikët për collaborative filtering (35%)
            for prod in collaborative_recs:
                product_scores[prod['ProductId']] += 0.35 * prod['similarity_score']

            # Shton pikët për trending products (25%)
            for prod in trending_recs:
                product_scores[prod['ProductId']] += 0.25 * prod['similarity_score']

            # Merr top N produktet
            top_products = sorted(
                product_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:num_recommendations]

            # Merr detajet e produkteve
            final_recommendations = []
            for prod_id, score in top_products:
                query = text("""
                    SELECT 
                        p.*,
                        COALESCE(AVG(ab.Rating), 0) as avg_rating,
                        COUNT(DISTINCT ab.UserId) as review_count
                    FROM products p
                    LEFT JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
                    WHERE p.ProductId = :product_id
                    GROUP BY p.ProductId
                """)

                with self.engine.connect() as conn:
                    result = conn.execute(query, {"product_id": prod_id}).fetchone()
                    if result:
                        final_recommendations.append({
                            "ProductId": result.ProductId,
                            "ProductType": result.ProductType,
                            "ProductTitle": result.ProductTitle,
                            "ImageURL": result.ImageURL or "http://localhost:5001/static/images/product-placeholder.jpg",
                            "price": float(result.price) if result.price else 0.0,
                            "Rating": float(result.avg_rating),
                            "ReviewCount": result.review_count,
                            "similarity_score": score
                        })

            return final_recommendations

        except Exception as e:
            print(f"Error in hybrid recommendations: {str(e)}")
            return self.get_similar_products(product_id, num_recommendations)  # Fallback në metodën bazë
