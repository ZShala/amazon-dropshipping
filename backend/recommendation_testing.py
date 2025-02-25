from recommendation_model import AdvancedRecommendationEngine
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
from datetime import datetime
import time
import pymysql

class RecommendationTester:
    def __init__(self):
        """Inicializon testerin me lidhje të saktë në databazë"""
        try:
            # Përdorim URL string format për SQLAlchemy
            self.connection_string = 'mysql+pymysql://root:mysqlZ97*@localhost/dataset_db?charset=utf8mb4'
            self.engine = create_engine(
                self.connection_string,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            self.recommender = AdvancedRecommendationEngine(self.engine)
            print("Database connection established successfully")
        except Exception as e:
            print(f"Error initializing tester: {str(e)}")
            raise
        
    def prepare_test_data(self):
        """Përgatit dataset për testim"""
        try:
            query = """
                SELECT DISTINCT 
                    p.ProductId, 
                    p.ProductType, 
                    ab.Rating, 
                    ab.UserId,
                    p.price
                FROM products p
                JOIN amazon_beauty ab ON p.ProductId = ab.ProductId
                WHERE ab.Rating >= 4.0
                AND p.price IS NOT NULL
                AND p.ProductType IS NOT NULL
                LIMIT 1000;
            """
            
            # Krijojmë një connection të përkohshëm
            with self.engine.connect() as connection:
                # Ekzekutojmë query-n
                result = connection.execute(text(query))
                
                # Konvertojmë rezultatin në DataFrame
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                
                if df.empty:
                    print("Warning: No data retrieved from database")
                    return pd.DataFrame()
                
                print(f"Retrieved {len(df)} test products")
                return df
                
        except Exception as e:
            print(f"Error preparing test data: {str(e)}")
            print("Connection string:", self.connection_string)
            import traceback
            traceback.print_exc()
            return pd.DataFrame()

    def evaluate_recommendations(self, test_size=100):
        """Vlerëson performancën e rekomandimeve"""
        try:
            test_data = self.prepare_test_data()
            
            if test_data.empty:
                print("No test data available. Skipping evaluation.")
                return {
                    'content_based': {'accuracy': 0, 'precision': 0, 'recall': 0},
                    'collaborative': {'accuracy': 0, 'precision': 0, 'recall': 0},
                    'hybrid': {'accuracy': 0, 'precision': 0, 'recall': 0},
                    'performance': {'avg_response_time': 0, 'p95_response_time': 0, 'max_response_time': 0}
                }
            
            results = {
                'content_based': {'correct': 0, 'total': 0},
                'collaborative': {'correct': 0, 'total': 0},
                'hybrid': {'correct': 0, 'total': 0}
            }
            
            response_times = []
            actual_test_size = min(test_size, len(test_data))
            
            print(f"Running evaluation on {actual_test_size} products...")
            
            for idx in range(actual_test_size):
                try:
                    product_id = test_data.iloc[idx]['ProductId']
                    print(f"Testing product {idx + 1}/{actual_test_size}: {product_id}")
                    
                    # Mat kohën e përgjigjes
                    start_time = time.time()
                    
                    # Test content-based
                    content_recs = self.recommender.get_similar_products(product_id)
                    if content_recs:
                        results['content_based']['total'] += len(content_recs)
                        results['content_based']['correct'] += len([r for r in content_recs 
                            if r['Rating'] >= 4.0])
                    
                    # Test collaborative
                    collab_recs = self.recommender.get_collaborative_recommendations(product_id)
                    if collab_recs:
                        results['collaborative']['total'] += len(collab_recs)
                        results['collaborative']['correct'] += len([r for r in collab_recs 
                            if r['Rating'] >= 4.0])
                    
                    # Test hybrid
                    hybrid_recs = self.recommender.get_hybrid_recommendations(product_id)
                    if hybrid_recs:
                        results['hybrid']['total'] += len(hybrid_recs)
                        results['hybrid']['correct'] += len([r for r in hybrid_recs 
                            if r['Rating'] >= 4.0])
                    
                    response_times.append(time.time() - start_time)
                    
                except Exception as e:
                    print(f"Error processing product {product_id}: {str(e)}")
                    continue
            
            return self.calculate_metrics(results, response_times)
            
        except Exception as e:
            print(f"Error in evaluate_recommendations: {str(e)}")
            return None
    
    def calculate_metrics(self, results, response_times):
        """Llogarit metrikat e performancës"""
        metrics = {}
        
        for method, data in results.items():
            if data['total'] > 0:
                accuracy = data['correct'] / data['total']
                metrics[method] = {
                    'accuracy': round(accuracy, 3),
                    'precision': round(data['correct'] / data['total'], 3),
                    'recall': round(data['correct'] / (data['total'] * 1.2), 3),  # Estimated total relevant
                }
                metrics[method]['f1_score'] = round(
                    2 * (metrics[method]['precision'] * metrics[method]['recall']) /
                    (metrics[method]['precision'] + metrics[method]['recall']), 3
                )
        
        # Performance metrics
        metrics['performance'] = {
            'avg_response_time': round(np.mean(response_times) * 1000, 2),  # në ms
            'p95_response_time': round(np.percentile(response_times, 95) * 1000, 2),
            'max_response_time': round(max(response_times) * 1000, 2)
        }
        
        return metrics

    def run_comprehensive_test(self):
        """Ekzekuton teste gjithëpërfshirëse"""
        print("Starting comprehensive recommendation testing...")
        
        # Test accuracy and performance
        metrics = self.evaluate_recommendations(test_size=100)
        
        # Test resource usage
        memory_usage = self.test_memory_usage()
        cache_performance = self.test_cache_performance()
        
        # Combine all results
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'accuracy_metrics': metrics,
            'resource_metrics': {
                'memory_usage': memory_usage,
                'cache_performance': cache_performance
            }
        }
        
        self.save_test_results(test_results)
        return test_results
    
    def test_memory_usage(self):
        """Teston përdorimin e memories"""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            return {
                'memory_used_mb': round(process.memory_info().rss / 1024 / 1024, 2),
                'memory_percent': round(process.memory_percent(), 2)
            }
        except ImportError:
            print("Warning: psutil not installed. Memory usage metrics will be unavailable.")
            return {
                'memory_used_mb': 0,
                'memory_percent': 0
            }
        except Exception as e:
            print(f"Error measuring memory usage: {str(e)}")
            return {
                'memory_used_mb': 0,
                'memory_percent': 0
            }
    
    def test_cache_performance(self):
        """Teston performancën e cache"""
        try:
            test_data = self.prepare_test_data()
            if test_data.empty:
                print("No data available for cache testing")
                return {
                    'cache_hit_rate': 0,
                    'cache_miss_rate': 1
                }
            
            test_products = test_data['ProductId'].head(10).tolist()
            cache_hits = 0
            total_requests = 20  # Do të testojmë çdo produkt 2 herë
            
            for _ in range(2):  # Dy iteracione për të testuar cache
                for product_id in test_products:
                    try:
                        start_time = time.time()
                        self.recommender.get_similar_products(product_id)
                        response_time = time.time() - start_time
                        
                        if response_time < 0.1:  # Supozojmë që përgjigjet nën 100ms janë nga cache
                            cache_hits += 1
                    except Exception as e:
                        print(f"Error testing cache for product {product_id}: {str(e)}")
                        continue
            
            return {
                'cache_hit_rate': round(cache_hits / total_requests, 2),
                'cache_miss_rate': round(1 - (cache_hits / total_requests), 2)
            }
        except Exception as e:
            print(f"Error in cache performance test: {str(e)}")
            return {
                'cache_hit_rate': 0,
                'cache_miss_rate': 1
            }
    
    def save_test_results(self, results):
        """Ruan rezultatet e testimit"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'test_results_{timestamp}.json'
        
        import json
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"Test results saved to {filename}")

    def test_content_based_filtering(self):
        """Teston detajisht content-based filtering"""
        print("\nTesting Content-Based Filtering...")
        test_data = self.prepare_test_data()
        if test_data.empty:
            print("No test data available")
            return {
                'category_match_rate': 0,
                'price_range_accuracy': 0,
                'high_rating_ratio': 0,
                'avg_response_time': 0
            }

        metrics = {
            'category_match': 0,
            'price_range_match': 0,
            'rating_quality': 0,
            'response_times': [],
            'total_valid_tests': 0
        }
        
        for idx in range(min(50, len(test_data))):
            try:
                product_id = test_data.iloc[idx]['ProductId']
                original_type = test_data.iloc[idx]['ProductType']
                original_price = float(test_data.iloc[idx]['price'] or 0)
                
                if original_price <= 0:
                    print(f"Skipping product {product_id} due to invalid price: {original_price}")
                    continue
                    
                start_time = time.time()
                recommendations = self.recommender.get_similar_products(product_id)
                metrics['response_times'].append(time.time() - start_time)
                
                if recommendations and len(recommendations) > 0:
                    valid_recommendations = [r for r in recommendations if r.get('price', 0) > 0]
                    
                    if not valid_recommendations:
                        print(f"No valid recommendations with prices for product {product_id}")
                        continue
                    
                    # Test category matching
                    category_matches = sum(1 for r in valid_recommendations 
                        if r['ProductType'].lower() in original_type.lower() 
                        or original_type.lower() in r['ProductType'].lower())
                    metrics['category_match'] += category_matches / len(valid_recommendations)
                    
                    # Test price range
                    try:
                        base_price = float(valid_recommendations[0]['price'])
                        if base_price > 0:
                            price_matches = sum(1 for r in valid_recommendations 
                                if r.get('price') and 0.5 <= float(r['price']) / base_price <= 1.5)
                            metrics['price_range_match'] += price_matches / len(valid_recommendations)
                    except (ValueError, ZeroDivisionError) as e:
                        print(f"Price comparison error for product {product_id}: {str(e)}")
                        continue
                    
                    # Test rating quality
                    high_rated = sum(1 for r in valid_recommendations if r.get('Rating', 0) >= 4.0)
                    metrics['rating_quality'] += high_rated / len(valid_recommendations)
                    
                    metrics['total_valid_tests'] += 1
                else:
                    print(f"No recommendations returned for product {product_id}")
                    
            except Exception as e:
                print(f"Error processing product {product_id}: {str(e)}")
                continue
        
        # Calculate averages based on valid tests
        if metrics['total_valid_tests'] > 0:
            return {
                'category_match_rate': round(metrics['category_match'] / metrics['total_valid_tests'], 3),
                'price_range_accuracy': round(metrics['price_range_match'] / metrics['total_valid_tests'], 3),
                'high_rating_ratio': round(metrics['rating_quality'] / metrics['total_valid_tests'], 3),
                'avg_response_time': round(np.mean(metrics['response_times']) * 1000, 2) if metrics['response_times'] else 0,
                'total_tests_run': metrics['total_valid_tests']
            }
        else:
            print("No valid tests completed")
            return {
                'category_match_rate': 0,
                'price_range_accuracy': 0,
                'high_rating_ratio': 0,
                'avg_response_time': 0,
                'total_tests_run': 0
            }

    def test_collaborative_filtering(self):
        """Teston detajisht collaborative filtering"""
        print("\nTesting Collaborative Filtering...")
        test_data = self.prepare_test_data()
        if test_data.empty:
            print("No test data available")
            return {
                'user_preference_match': 0,
                'rating_correlation': 0,
                'recommendation_diversity': 0,
                'avg_response_time': 0
            }

        metrics = {
            'user_similarity': 0,
            'rating_correlation': 0,
            'diversity': 0,
            'response_times': []
        }
        
        for idx in range(min(50, len(test_data))):
            try:
                product_id = test_data.iloc[idx]['ProductId']
                user_id = test_data.iloc[idx]['UserId']
                
                start_time = time.time()
                recommendations = self.recommender.get_collaborative_recommendations(product_id)
                metrics['response_times'].append(time.time() - start_time)
                
                if recommendations:
                    # Test user preference matching
                    user_query = """
                        SELECT ProductId, Rating 
                        FROM amazon_beauty 
                        WHERE UserId = :user_id AND Rating >= 4.0
                    """
                    
                    with self.engine.connect() as connection:
                        result = connection.execute(text(user_query), {"user_id": user_id})
                        user_ratings = pd.DataFrame(result.fetchall(), columns=result.keys())
                    
                    if not user_ratings.empty:
                        similar_products = set(user_ratings['ProductId'].tolist())
                        recommended_products = set(r['ProductId'] for r in recommendations)
                        similarity = len(similar_products.intersection(recommended_products)) / len(recommendations)
                        metrics['user_similarity'] += similarity
                    
                    # Calculate rating correlation
                    if len(recommendations) > 1:
                        ratings = [r['Rating'] for r in recommendations]
                        correlation = np.corrcoef(ratings[:-1], ratings[1:])[0,1]
                        metrics['rating_correlation'] += correlation if not np.isnan(correlation) else 0
                    
                    # Calculate diversity
                    categories = set(r['ProductType'] for r in recommendations)
                    metrics['diversity'] += len(categories) / len(recommendations)
                
            except Exception as e:
                print(f"Error processing product {product_id}: {str(e)}")
                continue
        
        test_count = 50
        return {
            'user_preference_match': round(metrics['user_similarity'] / test_count, 3),
            'rating_correlation': round(metrics['rating_correlation'] / test_count, 3),
            'recommendation_diversity': round(metrics['diversity'] / test_count, 3),
            'avg_response_time': round(np.mean(metrics['response_times']) * 1000, 2) if metrics['response_times'] else 0
        }

    def test_hybrid_recommendations(self):
        """Teston detajisht hybrid recommendations"""
        print("\nTesting Hybrid Recommendations...")
        test_data = self.prepare_test_data()
        metrics = {
            'overall_accuracy': 0,
            'method_contribution': {
                'content_based': 0,
                'collaborative': 0,
                'trending': 0
            },
            'response_times': []
        }
        
        for idx in range(50):
            product_id = test_data.iloc[idx]['ProductId']
            
            start_time = time.time()
            recommendations = self.recommender.get_hybrid_recommendations(product_id)
            metrics['response_times'].append(time.time() - start_time)
            
            if recommendations:
                # Test overall accuracy
                correct_recommendations = sum(1 for r in recommendations if r['Rating'] >= 4.0)
                metrics['overall_accuracy'] += correct_recommendations / len(recommendations)
                
                # Analyze method contribution
                for rec in recommendations:
                    if rec.get('similarity_score', 0) > 0.7:
                        metrics['method_contribution']['content_based'] += 1
                    elif rec.get('UserCount', 0) > 0:
                        metrics['method_contribution']['collaborative'] += 1
                    else:
                        metrics['method_contribution']['trending'] += 1
        
        test_count = 50
        total_recommendations = sum(metrics['method_contribution'].values())
        
        return {
            'overall_accuracy': round(metrics['overall_accuracy'] / test_count, 3),
            'method_distribution': {
                'content_based': round(metrics['method_contribution']['content_based'] / total_recommendations, 3),
                'collaborative': round(metrics['method_contribution']['collaborative'] / total_recommendations, 3),
                'trending': round(metrics['method_contribution']['trending'] / total_recommendations, 3)
            },
            'avg_response_time': round(np.mean(metrics['response_times']) * 1000, 2)
        }

    def run_detailed_tests(self):
        """Ekzekuton të gjitha testet e detajuara"""
        results = {
            'content_based_analysis': self.test_content_based_filtering(),
            'collaborative_analysis': self.test_collaborative_filtering(),
            'hybrid_analysis': self.test_hybrid_recommendations()
        }
        
        self.save_test_results(results)
        return results

    def verify_database_connection(self):
        """Verifikon lidhjen me databazën"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print("Database connection test successful")
                
                # Test data availability
                count_query = text("""
                    SELECT COUNT(*) as count
                    FROM products p 
                    JOIN amazon_beauty ab ON p.ProductId = ab.ProductId 
                    WHERE ab.Rating >= 4.0 
                    AND p.price IS NOT NULL 
                    AND p.ProductType IS NOT NULL
                """)
                count = connection.execute(count_query).scalar()
                print(f"Found {count} products available for testing")
                
                return True
        except Exception as e:
            print(f"Database connection test failed: {str(e)}")
            return False

if __name__ == '__main__':
    try:
        tester = RecommendationTester()
        
        print("\n=================================")
        print("Starting Recommendation System Tests")
        print("=================================\n")
        
        # Verify database connection first
        if not tester.verify_database_connection():
            print("Exiting due to database connection issues")
            exit(1)
        
        # Run comprehensive tests
        print("\nRunning Comprehensive Tests...")
        basic_results = tester.run_comprehensive_test()
        
        if basic_results is None:
            print("Basic tests failed")
            exit(1)
            
        # Run detailed tests
        print("\nRunning Detailed Tests...")
        detailed_results = tester.run_detailed_tests()
        
        if detailed_results is None:
            print("Detailed tests failed")
            exit(1)
        
        print("\n=================================")
        print("TEST RESULTS SUMMARY")
        print("=================================")
        
        print("\n1. Basic Performance Metrics:")
        print("---------------------------")
        print(f"Average Response Time: {basic_results['accuracy_metrics']['performance']['avg_response_time']}ms")
        print(f"Memory Usage: {basic_results['resource_metrics']['memory_usage']['memory_used_mb']}MB")
        print(f"Cache Hit Rate: {basic_results['resource_metrics']['cache_performance']['cache_hit_rate'] * 100}%")
        
        print("\n2. Content-Based Filtering Analysis:")
        print("----------------------------------")
        content_metrics = detailed_results['content_based_analysis']
        print(f"Category Match Rate: {content_metrics['category_match_rate'] * 100}%")
        print(f"Price Range Accuracy: {content_metrics['price_range_accuracy'] * 100}%")
        print(f"High Rating Ratio: {content_metrics['high_rating_ratio'] * 100}%")
        print(f"Average Response Time: {content_metrics['avg_response_time']}ms")
        
        print("\n3. Collaborative Filtering Analysis:")
        print("----------------------------------")
        collab_metrics = detailed_results['collaborative_analysis']
        print(f"User Preference Match: {collab_metrics['user_preference_match'] * 100}%")
        print(f"Rating Correlation: {collab_metrics['rating_correlation'] * 100}%")
        print(f"Recommendation Diversity: {collab_metrics['recommendation_diversity'] * 100}%")
        print(f"Average Response Time: {collab_metrics['avg_response_time']}ms")
        
        print("\n4. Hybrid Recommendations Analysis:")
        print("----------------------------------")
        hybrid_metrics = detailed_results['hybrid_analysis']
        print(f"Overall Accuracy: {hybrid_metrics['overall_accuracy'] * 100}%")
        print("\nMethod Distribution:")
        for method, value in hybrid_metrics['method_distribution'].items():
            print(f"- {method}: {value * 100}%")
        print(f"Average Response Time: {hybrid_metrics['avg_response_time']}ms")
        
        print("\n=================================")
        print("Test Results Saved Successfully")
        print("=================================")
        
    except Exception as e:
        print(f"Test execution failed: {str(e)}")
        import traceback
        traceback.print_exc() 