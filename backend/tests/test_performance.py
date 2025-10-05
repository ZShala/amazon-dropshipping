#!/usr/bin/env python3
import sys
import os
import time
import json
import psutil
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine, text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recommendation_model import AdvancedRecommendationEngine

class PerformanceTester:
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
        self.recommender = AdvancedRecommendationEngine(self.engine)
        self.results = {}
        self.test_products = ['B0009V1YR8', 'B0043OYFKU', 'B0000YUXI0', 'B0000020TR', 'B00000JGVX']
        
    def get_memory_usage(self):
        """Merr përdorimin aktual të memories"""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB
        
    def test_response_time(self):
        """Testimi i kohës së përgjigjes"""
        print("Testimi i kohës së përgjigjes (Response Time)...")
        
        results = {
            'test_name': 'Response Time Test',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        algorithms = {
            'content_based': self.recommender.get_similar_products,
            'collaborative': self.recommender.get_collaborative_recommendations,
            'trend_based': self.recommender.get_trending_recommendations,
            'hybrid': self.recommender.get_hybrid_recommendations
        }
        
        for algo_name, algo_func in algorithms.items():
            print(f"   Testimi i {algo_name}...")
            algo_times = []
            
            for product_id in self.test_products:
                try:
                    start_time = time.time()
                    recommendations = algo_func(product_id, 4)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    algo_times.append(response_time)
                    
                    test_result = {
                        'algorithm': algo_name,
                        'product_id': product_id,
                        'response_time': response_time,
                        'recommendations_count': len(recommendations),
                        'success': len(recommendations) > 0
                    }
                    
                    results['tests'].append(test_result)
                    print(f"     {product_id}: {response_time:.3f}s")
                    
                except Exception as e:
                    test_result = {
                        'algorithm': algo_name,
                        'product_id': product_id,
                        'response_time': 0.0,
                        'error': str(e),
                        'success': False
                    }
                    results['tests'].append(test_result)
                    print(f"     {product_id}: Gabim - {str(e)}")
            
            # Llogarit statistikat për algoritmin
            if algo_times:
                avg_time = np.mean(algo_times)
                min_time = np.min(algo_times)
                max_time = np.max(algo_times)
                
                print(f"   📊 {algo_name}: Mesatarja = {avg_time:.3f}s, Min = {min_time:.3f}s, Max = {max_time:.3f}s")
        
        # Llogarit statistikat e përgjithshme
        successful_tests = [test for test in results['tests'] if test['success']]
        all_times = [test['response_time'] for test in successful_tests]
        
        results['summary'] = {
            'total_tests': len(results['tests']),
            'successful_tests': len(successful_tests),
            'average_response_time': np.mean(all_times) if all_times else 0.0,
            'min_response_time': np.min(all_times) if all_times else 0.0,
            'max_response_time': np.max(all_times) if all_times else 0.0,
            'std_response_time': np.std(all_times) if all_times else 0.0
        }
        
        self.results['response_time'] = results
        return results
    
    def test_memory_usage(self):
        """Testimi i përdorimit të memories"""
        print("Testimi i përdorimit të memories (Memory Usage)...")
        
        results = {
            'test_name': 'Memory Usage Test',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        initial_memory = self.get_memory_usage()
        
        algorithms = {
            'content_based': self.recommender.get_similar_products,
            'collaborative': self.recommender.get_collaborative_recommendations,
            'trend_based': self.recommender.get_trending_recommendations,
            'hybrid': self.recommender.get_hybrid_recommendations
        }
        
        for algo_name, algo_func in algorithms.items():
            print(f"   Testimi i {algo_name}...")
            algo_memory_usage = []
            
            for product_id in self.test_products:
                try:
                    memory_before = self.get_memory_usage()
                    
                    recommendations = algo_func(product_id, 4)
             
                    memory_after = self.get_memory_usage()
                    
                    memory_used = memory_after - memory_before
                    algo_memory_usage.append(memory_used)
                    
                    test_result = {
                        'algorithm': algo_name,
                        'product_id': product_id,
                        'memory_before': memory_before,
                        'memory_after': memory_after,
                        'memory_used': memory_used,
                        'recommendations_count': len(recommendations),
                        'success': len(recommendations) > 0
                    }
                    
                    results['tests'].append(test_result)
                    print(f"     {product_id}: {memory_used:.2f}MB")
                    
                except Exception as e:
                    test_result = {
                        'algorithm': algo_name,
                        'product_id': product_id,
                        'memory_used': 0.0,
                        'error': str(e),
                        'success': False
                    }
                    results['tests'].append(test_result)
                    print(f"     {product_id}: Gabim - {str(e)}")
            
            # Llogarit statistikat për algoritmin
            if algo_memory_usage:
                avg_memory = np.mean(algo_memory_usage)
                min_memory = np.min(algo_memory_usage)
                max_memory = np.max(algo_memory_usage)
                
                print(f"   📊 {algo_name}: Mesatarja = {avg_memory:.2f}MB, Min = {min_memory:.2f}MB, Max = {max_memory:.2f}MB")
   
        successful_tests = [test for test in results['tests'] if test['success']]
        all_memory_usage = [test['memory_used'] for test in successful_tests]
        
        results['summary'] = {
            'total_tests': len(results['tests']),
            'successful_tests': len(successful_tests),
            'initial_memory': initial_memory,
            'average_memory_usage': np.mean(all_memory_usage) if all_memory_usage else 0.0,
            'min_memory_usage': np.min(all_memory_usage) if all_memory_usage else 0.0,
            'max_memory_usage': np.max(all_memory_usage) if all_memory_usage else 0.0,
            'std_memory_usage': np.std(all_memory_usage) if all_memory_usage else 0.0
        }
        
        self.results['memory_usage'] = results
        return results
    
    def test_throughput(self):
        """Testimi i throughput-it (numri i rekomandimeve për sekondë)"""
        print("Testimi i throughput-it...")
        
        results = {
            'test_name': 'Throughput Test',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
     
        print("   Testimi i throughput-it me sistemin hibrid...")
        
        start_time = time.time()
        total_recommendations = 0
        
        for product_id in self.test_products:
            try:
                recommendations = self.recommender.get_hybrid_recommendations(product_id, 4)
                total_recommendations += len(recommendations)
                
                test_result = {
                    'product_id': product_id,
                    'recommendations_count': len(recommendations),
                    'success': len(recommendations) > 0
                }
                
                results['tests'].append(test_result)
                print(f"     ✅ {product_id}: {len(recommendations)} rekomandime")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'recommendations_count': 0,
                    'error': str(e),
                    'success': False
                }
                results['tests'].append(test_result)
                print(f"     ❌ {product_id}: Gabim - {str(e)}")
        
        end_time = time.time()
        total_time = end_time - start_time
        throughput = total_recommendations / total_time if total_time > 0 else 0
        
        results['summary'] = {
            'total_tests': len(results['tests']),
            'successful_tests': sum(1 for test in results['tests'] if test['success']),
            'total_recommendations': total_recommendations,
            'total_time': total_time,
            'throughput': throughput
        }
        
        print(f"   Throughput: {throughput:.2f} rekomandime/sekondë")
        
        self.results['throughput'] = results
        return results
    
    def run_all_tests(self):
        """Ekzekuton të gjitha testet"""
        print("🚀 FILLIMI I TESTEVE TË PERFORMANCËS")
        print("=" * 60)
        
        self.test_response_time()
        print()
        self.test_memory_usage()
        print()
        self.test_throughput()
        print()
        
        self.create_final_report()
    
    def create_final_report(self):
        """Krijon raportin përfundimtar"""
        print("📊 RAPORTI PËRFUNDIMTAR I PERFORMANCËS")
        print("=" * 50)
        
        total_tests = 0
        total_successful = 0
        
        for test_type, results in self.results.items():
            summary = results['summary']
            total_tests += summary['total_tests']
            total_successful += summary['successful_tests']
            
            print(f"\n{test_type.upper()}:")
            if 'average_response_time' in summary:
                print(f"   Koha mesatare: {summary['average_response_time']:.3f}s")
                print(f"   Koha minimale: {summary['min_response_time']:.3f}s")
                print(f"   Koha maksimale: {summary['max_response_time']:.3f}s")
                print(f"   Devijimi standard: {summary['std_response_time']:.3f}s")
            elif 'average_memory_usage' in summary:
                print(f"   Memoria mesatare: {summary['average_memory_usage']:.2f}MB")
                print(f"   Memoria minimale: {summary['min_memory_usage']:.2f}MB")
                print(f"   Memoria maksimale: {summary['max_memory_usage']:.2f}MB")
                print(f"   Devijimi standard: {summary['std_memory_usage']:.2f}MB")
            elif 'throughput' in summary:
                print(f"   Throughput: {summary['throughput']:.2f} rekomandime/sekondë")
                print(f"   Rekomandime totale: {summary['total_recommendations']}")
                print(f"   Koha totale: {summary['total_time']:.3f}s")
        
        overall_success_rate = (total_successful / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\nTOTALI:")
        print(f"   Teste totale: {total_tests}")
        print(f"   Teste të suksesshme: {total_successful}")
        print(f"   Shkalla e suksesit: {overall_success_rate:.1f}%")
        
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """Ruan rezultatet në skedar JSON"""
        filename = f"test_results_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rezultatet u ruajtën në: {filename}")

if __name__ == "__main__":
    tester = PerformanceTester()
    tester.run_all_tests()
