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
    try:
        print(f"Starting recommendation fetch for product: {product_id}")
        engine = get_db()
        with engine.connect() as conn:
            # First check if product exists
            check_query = text("""
                SELECT a.ProductId, a.ProductType, p.ProductTitle, p.ImageURL 
                FROM amazon_beauty a
                JOIN products p ON a.ProductId = p.ProductId
                WHERE a.ProductId = :product_id
            """)
            product = conn.execute(check_query, {"product_id": product_id}).fetchone()
            
            if not product:
                print(f"Product {product_id} not found in database")
                return []
                
            print(f"Found product {product_id} of type: {product.ProductType}")
            
            # Get recommendations with titles and images
            query = text("""
                SELECT DISTINCT 
                    a.ProductId, 
                    a.ProductType, 
                    p.ProductTitle,
                    p.ImageURL,
                    a.Rating, 
                    a.URL
                FROM amazon_beauty a
                JOIN products p ON a.ProductId = p.ProductId
                WHERE a.ProductId != :product_id
                    AND (
                        a.ProductType = :product_type
                        OR a.ProductType LIKE :product_type_pattern
                    )
                    AND a.Rating >= 4
                ORDER BY a.Rating DESC, RAND()
                LIMIT :num_recommendations
            """)
            
            recommendations = conn.execute(query, {
                "product_id": product_id,
                "product_type": product.ProductType,
                "product_type_pattern": f"%{product.ProductType}%",
                "num_recommendations": num_recommendations
            }).fetchall()
            
            # Convert to list of dictionaries
            recommendations_list = [{
                "ProductId": row.ProductId,
                "ProductType": row.ProductType,
                "ProductTitle": row.ProductTitle,
                "ImageURL": row.ImageURL if row.ImageURL else None,  # Include ImageURL
                "Rating": float(row.Rating),
                "URL": row.URL
            } for row in recommendations]
            
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
    if not product_url:
        return None
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(product_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try different image selectors
        image_tag = (
            soup.find("img", {"id": "landingImage"}) or
            soup.find("img", {"id": "main-image"}) or
            soup.find("img", {"class": "product-image"})
        )
        
        if image_tag and image_tag.get("src"):
            image_url = image_tag.get("src")
            # Verify it's a valid image URL
            if image_url.startswith('http') and any(ext in image_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                return image_url
                
    except Exception as e:
        print(f"Error fetching image for URL {product_url}: {e}")
    return None

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
                # First try to get image from products table
                query = text("""
                    SELECT p.ImageURL, p.URL, ab.URL as amazon_url
                    FROM products p
                    JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
                    WHERE p.ProductId = :product_id
                """)
                
                with get_db().connect() as conn:
                    result = conn.execute(query, {"product_id": rec['ProductId']}).fetchone()
                    
                    if result and result.ImageURL and result.ImageURL.strip():
                        rec['ImageURL'] = result.ImageURL
                    else:
                        # Try both URLs for image fetching
                        image_url = None
                        for url in [result.URL, result.amazon_url]:
                            if url:
                                image_url = fetch_image(url)
                                if image_url and 'placeholder' not in image_url:
                                    break
                        
                        rec['ImageURL'] = image_url or "http://localhost:5001/static/images/product-placeholder.jpg"
                        
                        # Update the database with the found image URL
                        if image_url and 'placeholder' not in image_url:
                            update_query = text("""
                                UPDATE products 
                                SET ImageURL = :image_url 
                                WHERE ProductId = :product_id
                            """)
                            conn.execute(update_query, {
                                "image_url": image_url,
                                "product_id": rec['ProductId']
                            })
                            conn.commit()
                
                print(f"Image URL for {rec['ProductId']}: {rec['ImageURL']}")
                
            except Exception as e:
                print(f"Error fetching image for product {rec['ProductId']}: {e}")
                rec['ImageURL'] = "http://localhost:5001/static/images/product-placeholder.jpg"
                
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
