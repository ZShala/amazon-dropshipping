from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sqlalchemy import text
import pandas as pd
from datetime import datetime

class AdvancedRecommender:
    def __init__(self, engine):
        self.engine = engine
        self.tfidf = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )

    def get_product_features(self, product_id):
        """Get detailed product features for similarity calculation"""
        query = text("""
            SELECT 
                p.ProductId,
                p.ProductType,
                pr.ProductTitle,
                pr.price,
                AVG(p.Rating) as avg_rating,
                COUNT(*) as review_count
            FROM amazon_beauty p
            JOIN products pr ON p.ProductId = pr.ProductId
            WHERE p.ProductId = :product_id
            GROUP BY p.ProductId, p.ProductType, pr.ProductTitle, pr.price
        """)
        
        with self.engine.connect() as conn:
            result = conn.execute(query, {"product_id": product_id}).fetchone()
            return result if result else None

    def get_similar_products(self, product_id, n_recommendations=10):
        """Get similar products using multiple similarity metrics"""
        try:
            # Get base product features
            base_product = self.get_product_features(product_id)
            if not base_product:
                return []

            # Get candidate products
            query = text("""
                SELECT DISTINCT
                    p.ProductId,
                    p.ProductType,
                    pr.ProductTitle,
                    pr.ImageURL,
                    pr.price,
                    AVG(p.Rating) as avg_rating,
                    COUNT(*) as review_count
                FROM amazon_beauty p
                JOIN products pr ON p.ProductId = pr.ProductId
                WHERE p.ProductId != :product_id
                    AND p.ProductType IS NOT NULL
                    AND pr.ProductTitle IS NOT NULL
                GROUP BY 
                    p.ProductId, 
                    p.ProductType,
                    pr.ProductTitle,
                    pr.ImageURL,
                    pr.price
                HAVING 
                    avg_rating >= 3.5
                    AND review_count >= 3
            """)

            with self.engine.connect() as conn:
                df = pd.read_sql(query, conn, params={"product_id": product_id})
                
                if df.empty:
                    return []

                # 1. Content-based similarity
                df['features'] = df['ProductType'] + ' ' + df['ProductTitle']
                base_features = base_product.ProductType + ' ' + base_product.ProductTitle
                
                # Calculate TF-IDF similarity
                all_features = list(df['features']) + [base_features]
                tfidf_matrix = self.tfidf.fit_transform(all_features)
                cosine_sim = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1])[0]
                
                # 2. Price similarity (normalized)
                price_diff = 1 - np.abs(df['price'] - base_product.price) / max(base_product.price, 1)
                
                # 3. Rating similarity
                rating_sim = 1 - np.abs(df['avg_rating'] - base_product.avg_rating) / 5.0
                
                # 4. Category bonus
                category_bonus = np.where(df['ProductType'] == base_product.ProductType, 0.2, 0)
                
                # Combine similarities with weights
                final_scores = (
                    0.4 * cosine_sim +      # Content similarity
                    0.2 * price_diff +      # Price similarity
                    0.2 * rating_sim +      # Rating similarity
                    0.2 * category_bonus    # Category bonus
                )
                
                # Get top recommendations
                top_indices = final_scores.argsort()[-n_recommendations:][::-1]
                
                recommendations = []
                for idx in top_indices:
                    recommendations.append({
                        'ProductId': df.iloc[idx]['ProductId'],
                        'ProductType': df.iloc[idx]['ProductType'],
                        'ProductTitle': df.iloc[idx]['ProductTitle'],
                        'ImageURL': df.iloc[idx]['ImageURL'],
                        'price': float(df.iloc[idx]['price']),
                        'Rating': float(df.iloc[idx]['avg_rating']),
                        'ReviewCount': int(df.iloc[idx]['review_count']),
                        'similarity_score': float(final_scores[idx]),
                        'recommendation_type': 'hybrid'
                    })

                return recommendations

        except Exception as e:
            print(f"Error in get_similar_products: {str(e)}")
            return []

    def get_recommendations(self, product_id, n_recommendations=10):
        """Main recommendation method with fallback strategies"""
        try:
            # Try getting hybrid recommendations first
            recommendations = self.get_similar_products(product_id, n_recommendations)
            
            # If we don't have enough recommendations, add category-based recommendations
            if len(recommendations) < n_recommendations:
                category_recs = self.get_category_recommendations(product_id, 
                                                               n_recommendations - len(recommendations))
                recommendations.extend(category_recs)
            
            return recommendations

        except Exception as e:
            print(f"Error in get_recommendations: {str(e)}")
            return []

    def get_category_recommendations(self, product_id, n_recommendations=5):
        """Get recommendations from the same category as fallback"""
        query = text("""
            WITH product_category AS (
                SELECT DISTINCT ProductType 
                FROM amazon_beauty 
                WHERE ProductId = :product_id
            )
            SELECT DISTINCT
                p.ProductId,
                p.ProductType,
                pr.ProductTitle,
                pr.ImageURL,
                pr.price,
                AVG(p.Rating) as avg_rating,
                COUNT(*) as review_count
            FROM amazon_beauty p
            JOIN products pr ON p.ProductId = pr.ProductId
            JOIN product_category pc ON p.ProductType = pc.ProductType
            WHERE p.ProductId != :product_id
            GROUP BY 
                p.ProductId, 
                p.ProductType,
                pr.ProductTitle,
                pr.ImageURL,
                pr.price
            HAVING 
                avg_rating >= 4.0
                AND review_count >= 5
            ORDER BY avg_rating DESC, review_count DESC
            LIMIT :limit
        """)

        try:
            with self.engine.connect() as conn:
                result = conn.execute(query, {
                    "product_id": product_id,
                    "limit": n_recommendations
                })

                recommendations = []
                for row in result:
                    recommendations.append({
                        'ProductId': row.ProductId,
                        'ProductType': row.ProductType,
                        'ProductTitle': row.ProductTitle,
                        'ImageURL': row.ImageURL,
                        'price': float(row.price),
                        'Rating': float(row.avg_rating),
                        'ReviewCount': int(row.review_count),
                        'recommendation_type': 'category'
                    })

                return recommendations

        except Exception as e:
            print(f"Error in get_category_recommendations: {str(e)}")
            return [] 