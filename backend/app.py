from flask import Flask, request, jsonify
from flask_cors import CORS
from model import get_recommendations_with_images
from database_operations import get_data_from_db, get_product_details, get_cart_recommendations, get_category_products, get_all_product_types
import atexit
from sqlalchemy import create_engine, text
import multiprocessing
from sqlalchemy.pool import QueuePool

app = Flask(__name__)
# Konfiguro CORS për të lejuar kërkesat nga frontend
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Krijojmë një engine të vetëm për të gjithë aplikacionin
engine = None

def get_db():
    global engine
    if engine is None:
        try:
            engine = create_engine(
                'mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db',
                poolclass=QueuePool,
                pool_size=20,  # Rrisim pool size
                max_overflow=30,
                pool_timeout=30,
                pool_recycle=1800,
                pool_pre_ping=True,  # Kontrollon lidhjen para përdorimit
                echo=False,  # Heqim logging për performancë më të mirë
                # Optimizime shtesë
                connect_args={
                    'connect_timeout': 10,
                    'read_timeout': 30,
                    'write_timeout': 30,
                    'use_pure': True,  # Përdor implementimin pure Python
                }
            )
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            raise e
    return engine

@atexit.register
def cleanup():
    """Pastron resurset në mbyllje të aplikacionit"""
    global engine
    if engine:
        engine.dispose()
    
    # Pastrojmë multiprocessing resources
    multiprocessing.current_process()._config['semprefix'] = '/mp'

@app.route('/first_5_products', methods=['GET'])
def first_5_products():
    try:
        engine = get_db()
        df_clean = get_data_from_db(engine)
        if df_clean is None:
            return jsonify({"error": "Gabim në leximin e të dhënave"}), 500
            
        # Marrim 5 produktet e para
        first_5 = df_clean.head(5)
        
        # Përgatisim listën e produkteve për return
        products = []
        for _, product_row in first_5.iterrows():
            products.append({
                "ProductId": product_row['ProductId'],
                "ProductType": product_row['ProductType'],
                "Rating": float(product_row['Rating']),
                "URL": product_row['URL']
            })
        
        return jsonify({'first_5_products': products})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/product/<product_id>', methods=['GET'])
def get_product_detail(product_id):
    try:
        engine = get_db()
        df_clean = get_data_from_db(engine)
        if df_clean is None:
            return jsonify({"error": "Gabim në leximin e të dhënave"}), 500
            
        # Gjejmë produktin specifik
        product = df_clean[df_clean['ProductId'] == product_id]
        
        if product.empty:
            return jsonify({"error": "Produkti nuk u gjet"}), 404
        
        product = product.iloc[0]

        return jsonify({
            "product": {
                "ProductId": product['ProductId'],
                "ProductType": product['ProductType'],
                "Rating": float(product['Rating']),
                "URL": product['URL']
            }
        })
    except Exception as e:
        return jsonify({"error": "Gabim i brendshëm"}), 500

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        engine = get_db()
        product_id = request.args.get('product_id')
        print(f"Duke kërkuar rekomandime për produktin: {product_id}")
        
        if not product_id:
            print("Nuk u dha product_id")
            return jsonify({"error": "Duhet të jepni një Product ID"}), 400
        
        # Kontrollojmë nëse produkti ekziston
        product_exists = get_product_details(engine, product_id)
        if not product_exists:
            print(f"Produkti {product_id} nuk u gjet në databazë")
            return jsonify({"error": f"Produkti {product_id} nuk ekziston"}), 404
        
        print("Duke gjeneruar rekomandimet...")
        recommendations = get_recommendations_with_images(product_id, engine)
        print(f"U gjetën {len(recommendations)} rekomandime")
        
        if not recommendations:
            print("Nuk u gjetën rekomandime")
            return jsonify({"error": "Nuk u gjetën rekomandime"}), 404
            
        return jsonify({
            "success": True,
            "product_id": product_id,
            "recommendations": recommendations
        })
        
    except Exception as e:
        print(f"Error në /recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommendations/cart', methods=['GET'])
def get_cart_recommendations():
    try:
        product_ids = request.args.get('products', '').split(',')
        if not product_ids:
            return jsonify({"error": "No products provided"}), 400

        engine = get_db()
        recommendations = get_cart_recommendations(engine, product_ids)
        
        return jsonify(recommendations)
        
    except Exception as e:
        print(f"Error në /cart recommendations: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/<category_type>', methods=['GET'])
def get_category_products_endpoint(category_type):
    try:
        print(f"Duke kërkuar produktet për kategorinë: {category_type}")
        engine = get_db()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = get_category_products(engine, category_type, page, per_page)
        print("API Response:", result)  # Debug log
        
        if not result or not result.get('products'):
            print(f"Nuk u gjetën produkte për kategorinë: {category_type}")
            return jsonify({
                "message": f"No products found for category: {category_type}", 
                "products": [],
                "total": 0,
                "page": page,
                "per_page": per_page,
                "total_pages": 1
            }), 200  # Changed to 200 to avoid frontend error
            
        return jsonify(result)
        
    except Exception as e:
        print(f"Error në /category endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "products": [],
            "total": 0,
            "page": 1,
            "per_page": 20,
            "total_pages": 1
        }), 200  # Changed to 200 to avoid frontend error

@app.route('/api/test', methods=['GET'])
def test_connection():
    return jsonify({"message": "Backend connection successful!"})

@app.route('/api/product-types', methods=['GET'])
def get_all_product_types_endpoint():
    try:
        engine = get_db()
        product_types = get_all_product_types(engine)
        
        if not product_types:
            return jsonify({
                "message": "No product types found", 
                "types": []
            }), 404
            
        return jsonify({
            "types": product_types
        })
        
    except Exception as e:
        print(f"Error në /product-types endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/image-cache', methods=['GET'])
def check_image_cache_endpoint():
    try:
        engine = get_db()
        query = text("""
            SELECT asin, image_url, last_updated 
            FROM product_images 
            ORDER BY last_updated DESC 
            LIMIT 100
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query)
            cached_images = [{
                "asin": row.asin,
                "image_url": row.image_url,
                "last_updated": row.last_updated
            } for row in result]
            
            # Merr statistikat
            stats_query = text("""
                SELECT 
                    COUNT(*) as total,
                    MIN(last_updated) as oldest,
                    MAX(last_updated) as newest
                FROM product_images
            """)
            stats = conn.execute(stats_query).fetchone()
            
            return jsonify({
                "cached_images": cached_images,
                "stats": {
                    "total_images": stats.total,
                    "oldest_cache": stats.oldest,
                    "newest_cache": stats.newest
                }
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/details/<product_id>', methods=['GET'])
def get_product_details(product_id):
    try:
        # Query për të marrë detajet e produktit
        query = text("""
            SELECT DISTINCT 
                p.ProductId,
                p.ProductType,
                p.Rating,
                p.URL,
                COUNT(*) as review_count,
                AVG(p.Rating) as avg_rating
            FROM amazon_beauty p
            WHERE p.ProductId = :product_id
            GROUP BY p.ProductId, p.ProductType, p.Rating, p.URL
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query, {"product_id": product_id}).fetchone()
            
            if result:
                # Nxjerr ASIN nga URL
                url_parts = result.URL.split('/')
                asin = next((part for part in url_parts 
                           if part.startswith('B0') or part.startswith('A0')), None)
                
                product = {
                    "ProductId": result.ProductId,
                    "ProductType": result.ProductType,
                    "Rating": float(result.avg_rating),
                    "URL": result.URL,
                    "ReviewCount": result.review_count,
                    "ASIN": asin,
                    "ImageURL": f"https://m.media-amazon.com/images/I/{asin}._SX300_SY300_QL70_ML2_.jpg"
                }
                
                return jsonify({"product": product})
            
            return jsonify({"error": "Product not found"}), 404
            
    except Exception as e:
        print(f"Error getting product details: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    engine = get_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
