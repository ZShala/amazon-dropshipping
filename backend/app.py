from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_cors import CORS
from model import get_recommendations, get_recommendations_with_images
from database_operations import get_data_from_db, get_category_products, fetch_product_details
import atexit
from sqlalchemy import create_engine, text
import multiprocessing
from sqlalchemy.pool import QueuePool
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

engine = None

def get_db():
    global engine
    if engine is None:
        try:
            engine = create_engine(
                'mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db',
                poolclass=QueuePool,
                pool_size=20, 
                max_overflow=30,
                pool_timeout=30,
                pool_recycle=1800,
                pool_pre_ping=True, 
                echo=False, 
                connect_args={
                    'connect_timeout': 10,
                    'read_timeout': 30,
                    'write_timeout': 30,
                    'use_pure': True,  
                }
            )
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            raise e
    return engine

@atexit.register
def cleanup():
    global engine
    if engine:
        engine.dispose()
        
    multiprocessing.current_process()._config['semprefix'] = '/mp'

@app.route('/recommendations', methods=['GET'])
def get_recommendations_endpoint():
    try:
        product_id = request.args.get('product_id')
        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400
            
        print(f"Processing recommendation request for product: {product_id}")
        
        engine = get_db()
        with engine.connect() as conn:
            exists_query = text("SELECT 1 FROM amazon_beauty WHERE ProductId = :pid")
            exists = conn.execute(exists_query, {"pid": product_id}).fetchone()
            
            if not exists:
                print(f"Product {product_id} not found")
                return jsonify({
                    "error": "Product not found",
                    "recommendations": []
                }), 404
        
        recommendations = get_recommendations_with_images(product_id)
        
        if not recommendations:
            print(f"No recommendations found for product {product_id}")
            return jsonify({
                "success": False,
                "error": "No recommendations found",
                "recommendations": []
            }), 404
            
        print(f"Returning {len(recommendations)} recommendations")
        return jsonify({
            "success": True,
            "recommendations": recommendations
        })
        
    except Exception as e:
        print(f"Error in recommendations endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/<category_type>', methods=['GET'])
def get_category_products_endpoint(category_type):
    try:
        print(f"Duke kërkuar produktet për kategorinë: {category_type}")
        engine = get_db()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = get_category_products(engine, category_type, page, per_page)
        print("API Response:", result) 
        
        if not result or not result.get('products'):
            print(f"Nuk u gjetën produkte për kategorinë: {category_type}")
            return jsonify({
                "message": f"No products found for category: {category_type}", 
                "products": [],
                "total": 0,
                "page": page,
                "per_page": per_page,
                "total_pages": 1
            }), 200  
            
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
        }), 200 

@app.route('/api/products/details/<product_id>', methods=['GET'])
def get_product_details_endpoint(product_id):
    try:
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
                product_details = fetch_product_details(result.URL)
                
                product = {
                    "ProductId": result.ProductId,
                    "ProductType": product_details["title"] or result.ProductType,
                    "Rating": float(result.avg_rating),
                    "URL": result.URL,
                    "ReviewCount": result.review_count,
                    "ImageURL": product_details["image_url"],
                    "price": product_details["price"],
                    "currency": "EUR"
                }
                
                return jsonify({"product": product})
            
            return jsonify({"error": "Product not found"}), 404
            
    except Exception as e:
        print(f"Error getting product details: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)

if __name__ == '__main__':
    engine = get_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
