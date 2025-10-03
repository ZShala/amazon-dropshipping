#!/usr/bin/env python3
"""
Testet për funksionalitetin e algoritmeve të rekomandimit
Për temën e masterit: ENHANCING DROPSHIPPING PERFORMANCE THROUGH RECOMMENDATION ENGINES
"""

import sys
import os
import time
import json
from datetime import datetime
from sqlalchemy import create_engine, text
from recommendation_model import AdvancedRecommendationEngine

class AlgorithmFunctionalityTester:
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
        self.recommender = AdvancedRecommendationEngine(self.engine)
        self.results = {}
        self.test_products = ['B0009V1YR8', 'B0043OYFKU', 'B0000YUXI0', 'B0000020TR', 'B00000JGVX']
        
    def test_content_based_filtering(self):
        """Testimi i Content-based Filtering"""
        print("🧪 Testimi i Content-based Filtering...")
        
        results = {
            'test_name': 'Content-based Filtering',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        for product_id in self.test_products:
            try:
                start_time = time.time()
                recommendations = self.recommender.get_similar_products(product_id, 4)
                end_time = time.time()
                
                test_result = {
                    'product_id': product_id,
                    'success': len(recommendations) > 0,
                    'recommendations_count': len(recommendations),
                    'response_time': end_time - start_time,
                    'recommendations': recommendations[:2] if recommendations else []  # Vetëm 2 për dokumentim
                }
                
                results['tests'].append(test_result)
                print(f"   ✅ {product_id}: {len(recommendations)} rekomandime në {end_time - start_time:.3f}s")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'success': False,
                    'error': str(e),
                    'response_time': 0
                }
                results['tests'].append(test_result)
                print(f"   ❌ {product_id}: Gabim - {str(e)}")
        
        # Llogarit statistikat
        successful_tests = sum(1 for test in results['tests'] if test['success'])
        total_tests = len(results['tests'])
        avg_response_time = sum(test['response_time'] for test in results['tests'] if test['success']) / max(successful_tests, 1)
        
        results['summary'] = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': (successful_tests / total_tests) * 100,
            'average_response_time': avg_response_time
        }
        
        self.results['content_based'] = results
        return results
    
    def test_collaborative_filtering(self):
        """Testimi i Collaborative Filtering"""
        print("🧪 Testimi i Collaborative Filtering...")
        
        results = {
            'test_name': 'Collaborative Filtering',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        for product_id in self.test_products:
            try:
                start_time = time.time()
                recommendations = self.recommender.get_collaborative_recommendations(product_id, 4)
                end_time = time.time()
                
                test_result = {
                    'product_id': product_id,
                    'success': len(recommendations) > 0,
                    'recommendations_count': len(recommendations),
                    'response_time': end_time - start_time,
                    'recommendations': recommendations[:2] if recommendations else []
                }
                
                results['tests'].append(test_result)
                print(f"   ✅ {product_id}: {len(recommendations)} rekomandime në {end_time - start_time:.3f}s")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'success': False,
                    'error': str(e),
                    'response_time': 0
                }
                results['tests'].append(test_result)
                print(f"   ❌ {product_id}: Gabim - {str(e)}")
        
        # Llogarit statistikat
        successful_tests = sum(1 for test in results['tests'] if test['success'])
        total_tests = len(results['tests'])
        avg_response_time = sum(test['response_time'] for test in results['tests'] if test['success']) / max(successful_tests, 1)
        
        results['summary'] = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': (successful_tests / total_tests) * 100,
            'average_response_time': avg_response_time
        }
        
        self.results['collaborative'] = results
        return results
    
    def test_trend_based_filtering(self):
        """Testimi i Trend-based Filtering"""
        print("🧪 Testimi i Trend-based Filtering...")
        
        results = {
            'test_name': 'Trend-based Filtering',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        for product_id in self.test_products:
            try:
                start_time = time.time()
                recommendations = self.recommender.get_trending_recommendations(product_id, 4)
                end_time = time.time()
                
                test_result = {
                    'product_id': product_id,
                    'success': len(recommendations) > 0,
                    'recommendations_count': len(recommendations),
                    'response_time': end_time - start_time,
                    'recommendations': recommendations[:2] if recommendations else []
                }
                
                results['tests'].append(test_result)
                print(f"   ✅ {product_id}: {len(recommendations)} rekomandime në {end_time - start_time:.3f}s")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'success': False,
                    'error': str(e),
                    'response_time': 0
                }
                results['tests'].append(test_result)
                print(f"   ❌ {product_id}: Gabim - {str(e)}")
        
        # Llogarit statistikat
        successful_tests = sum(1 for test in results['tests'] if test['success'])
        total_tests = len(results['tests'])
        avg_response_time = sum(test['response_time'] for test in results['tests'] if test['success']) / max(successful_tests, 1)
        
        results['summary'] = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': (successful_tests / total_tests) * 100,
            'average_response_time': avg_response_time
        }
        
        self.results['trend_based'] = results
        return results
    
    def test_hybrid_system(self):
        """Testimi i sistemit hibrid"""
        print("🧪 Testimi i sistemit hibrid...")
        
        results = {
            'test_name': 'Hybrid System',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        for product_id in self.test_products:
            try:
                start_time = time.time()
                recommendations = self.recommender.get_hybrid_recommendations(product_id, 4)
                end_time = time.time()
                
                test_result = {
                    'product_id': product_id,
                    'success': len(recommendations) > 0,
                    'recommendations_count': len(recommendations),
                    'response_time': end_time - start_time,
                    'recommendations': recommendations[:2] if recommendations else []
                }
                
                results['tests'].append(test_result)
                print(f"   ✅ {product_id}: {len(recommendations)} rekomandime në {end_time - start_time:.3f}s")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'success': False,
                    'error': str(e),
                    'response_time': 0
                }
                results['tests'].append(test_result)
                print(f"   ❌ {product_id}: Gabim - {str(e)}")
        
        # Llogarit statistikat
        successful_tests = sum(1 for test in results['tests'] if test['success'])
        total_tests = len(results['tests'])
        avg_response_time = sum(test['response_time'] for test in results['tests'] if test['success']) / max(successful_tests, 1)
        
        results['summary'] = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': (successful_tests / total_tests) * 100,
            'average_response_time': avg_response_time
        }
        
        self.results['hybrid'] = results
        return results
    
    def run_all_tests(self):
        """Ekzekuton të gjitha testet"""
        print("🚀 FILLIMI I TESTEVE TË FUNKSIONALITETIT TË ALGORITMEVE")
        print("=" * 60)
        
        # Ekzekuto testet
        self.test_content_based_filtering()
        print()
        self.test_collaborative_filtering()
        print()
        self.test_trend_based_filtering()
        print()
        self.test_hybrid_system()
        print()
        
        # Krijo raportin përfundimtar
        self.create_final_report()
    
    def create_final_report(self):
        """Krijon raportin përfundimtar"""
        print("📊 RAPORTI PËRFUNDIMTAR")
        print("=" * 40)
        
        # Llogarit statistikat e përgjithshme
        total_tests = 0
        total_successful = 0
        total_response_time = 0
        
        for algorithm, results in self.results.items():
            summary = results['summary']
            total_tests += summary['total_tests']
            total_successful += summary['successful_tests']
            total_response_time += summary['average_response_time'] * summary['successful_tests']
            
            print(f"\n{algorithm.upper()}:")
            print(f"   Sukses: {summary['successful_tests']}/{summary['total_tests']} ({summary['success_rate']:.1f}%)")
            print(f"   Koha mesatare: {summary['average_response_time']:.3f}s")
        
        overall_success_rate = (total_successful / total_tests) * 100 if total_tests > 0 else 0
        overall_avg_time = total_response_time / max(total_successful, 1)
        
        print(f"\nTOTALI:")
        print(f"   Teste totale: {total_tests}")
        print(f"   Teste të suksesshme: {total_successful}")
        print(f"   Shkalla e suksesit: {overall_success_rate:.1f}%")
        print(f"   Koha mesatare: {overall_avg_time:.3f}s")
        
        # Ruaj rezultatet në skedar
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """Ruan rezultatet në skedar JSON"""
        filename = f"test_results_algorithm_functionality_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rezultatet u ruajtën në: {filename}")

if __name__ == "__main__":
    tester = AlgorithmFunctionalityTester()
    tester.run_all_tests()
