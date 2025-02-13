import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import Image, display

# Create a database connection
def get_db():
    try:
        engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
        return engine
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise e

# Function to fetch all products from the database
def fetch_all_products():
    engine = get_db()
    with engine.connect() as conn:
        query = text("SELECT ProductId, ProductType, Rating, URL FROM amazon_beauty")
        result = conn.execute(query).fetchall()
    return [dict(row) for row in result]

# Function to get recommendations based on product ID
def get_recommendations(product_id, num_recommendations=4):
    """Fetch recommendations based on product ID from the database."""
    try:
        print(f"Starting recommendation fetch for product: {product_id}")
        engine = get_db()
        with engine.connect() as conn:
            # Së pari kontrollojmë nëse produkti ekziston
            check_query = text("""
                SELECT ProductId, ProductType 
                FROM amazon_beauty 
                WHERE ProductId = :product_id
            """)
            product = conn.execute(check_query, {"product_id": product_id}).fetchone()
            
            if not product:
                print(f"Product {product_id} not found in database")
                return []
                
            print(f"Found product {product_id} of type: {product.ProductType}")
            
            # Marrim rekomandimet
            query = text("""
                SELECT DISTINCT ProductId, ProductType, Rating, URL
                FROM amazon_beauty
                WHERE ProductId != :product_id
                    AND (
                        ProductType = :product_type
                        OR ProductType LIKE :product_type_pattern
                    )
                    AND Rating >= 4
                ORDER BY Rating DESC, RAND()
                LIMIT :num_recommendations
            """)
            
            recommendations = conn.execute(query, {
                "product_id": product_id,
                "product_type": product.ProductType,
                "product_type_pattern": f"%{product.ProductType}%",
                "num_recommendations": num_recommendations
            }).fetchall()
            
            print(f"Found {len(recommendations)} initial recommendations")
            
            # Nëse nuk kemi mjaftueshëm rekomandime, marrim produkte të ngjashme
            if len(recommendations) < num_recommendations:
                print("Not enough recommendations, fetching similar products")
                fallback_query = text("""
                    SELECT DISTINCT ProductId, ProductType, Rating, URL
                    FROM amazon_beauty
                    WHERE ProductId != :product_id
                        AND Rating >= 4
                    ORDER BY Rating DESC, RAND()
                    LIMIT :limit
                """)
                
                remaining = num_recommendations - len(recommendations)
                fallback_results = conn.execute(fallback_query, {
                    "product_id": product_id,
                    "limit": remaining
                }).fetchall()
                
                recommendations.extend(fallback_results)
                print(f"Added {len(fallback_results)} fallback recommendations")
            
            # Konvertojmë në listë të fjalorëve
            recommendations_list = [{
                "ProductId": row[0],
                "ProductType": row[1],
                "Rating": float(row[2]),
                "URL": row[3]
            } for row in recommendations]
            
            print(f"Returning {len(recommendations_list)} total recommendations")
            return recommendations_list
            
    except Exception as e:
        print(f"Error in get_recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

# Example function to fetch product details
def get_product_details(product_id):
    """Fetch product details from the database."""
    try:
        engine = get_db()
        with engine.connect() as conn:
            query = text("""
                SELECT ProductId, ProductType, Rating, URL
                FROM amazon_beauty
                WHERE ProductId = :product_id
            """)
            result = conn.execute(query, {"product_id": product_id}).fetchone()
            return dict(result) if result else None
    except Exception as e:
        print(f"Error fetching product details: {str(e)}")
        return None

# Function to fetch image from product URL
def fetch_image(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.find("img", {"id": "landingImage"})  # Adjust the ID if needed
        if image_tag:
            return image_tag.get("src")
    except Exception as e:
        print(f"Error fetching image for URL {product_url}: {e}")
    return "https://via.placeholder.com/150"  # Fallback image

# Function to get recommendations with images
def get_recommendations_with_images(product_id):
    try:
        print(f"Fetching recommendations for product: {product_id}")
        recommendations = get_recommendations(product_id)
        
        if not recommendations:
            print(f"No recommendations found for product: {product_id}")
            return []
            
        print(f"Found {len(recommendations)} recommendations")
        
        # Add images to recommendations
        for rec in recommendations:
            try:
                rec['ImageURL'] = fetch_image(rec['URL'])
            except Exception as e:
                print(f"Error fetching image for product {rec['ProductId']}: {e}")
                rec['ImageURL'] = "https://via.placeholder.com/150"
                
        return recommendations
        
    except Exception as e:
        print(f"Error in get_recommendations_with_images: {str(e)}")
        raise e

# Test the function
test_product_id = 'B00LLPT4HI'
recommended_products = get_recommendations_with_images(test_product_id)

# Display recommendations with images
for product in recommended_products:
    print(f"Product ID: {product['ProductId']}")
    print(f"Product Type: {product['ProductType']}")
    print(f"Rating: {product['Rating']}")
    display(Image(url=product['ImageURL']))
