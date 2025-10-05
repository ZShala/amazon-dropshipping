#!/usr/bin/env python3
"""
Testet për metrikat kryesore të sistemit të rekomandimit
Për temën e masterit: ENHANCING DROPSHIPPING PERFORMANCE THROUGH RECOMMENDATION ENGINES
"""

import sys
import os
import time
import json
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine, text

# Shto path-in për të importuar recommendation_model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recommendation_model import AdvancedRecommendationEngine

class CoreMetricsTester:
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
        self.recommender = AdvancedRecommendationEngine(self.engine)
        self.results = {}
        self.test_products = ['B0009V1YR8', 'B0043OYFKU', 'B0000YUXI0', 'B0000020TR', 'B00000JGVX']
        
    def calculate_accuracy(self, recommendations, expected_categories=None):
        """Llogarit saktësinë e rekomandimeve"""
        if not recommendations:
            return 0.0
        
        # Për thjeshtësi, supozojmë se rekomandimet janë të sakta nëse kanë rating > 3.5
        correct_recommendations = sum(1 for rec in recommendations if rec.get('Rating', 0) > 3.5)
        total_recommendations = len(recommendations)
        
        return (correct_recommendations / total_recommendations) * 100 if total_recommendations > 0 else 0.0
    
    def calculate_precision(self, recommendations, threshold=3.5):
        """Llogarit precision"""
        if not recommendations:
            return 0.0
        
        relevant_recommendations = sum(1 for rec in recommendations if rec.get('Rating', 0) >= threshold)
        total_recommendations = len(recommendations)
        
        return (relevant_recommendations / total_recommendations) * 100 if total_recommendations > 0 else 0.0
    
    def calculate_recall(self, recommendations, threshold=3.5):
        """Llogarit recall"""
        if not recommendations:
            return 0.0
        
        # Për thjeshtësi, supozojmë se ka 4 rekomandime të mundshme të sakta
        relevant_recommendations = sum(1 for rec in recommendations if rec.get('Rating', 0) >= threshold)
        total_possible_relevant = 4  # Numri i rekomandimeve që kërkojmë
        
        return (relevant_recommendations / total_possible_relevant) * 100
    
    def calculate_f1_score(self, precision, recall):
        """Llogarit F1-score"""
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    def test_accuracy(self):
        """Testimi i saktësisë"""
        print("🧪 Testimi i saktësisë (Accuracy)...")
        
        results = {
            'test_name': 'Accuracy Test',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        for product_id in self.test_products:
            try:
                # Testo me sistemin hibrid
                recommendations = self.recommender.get_hybrid_recommendations(product_id, 4)
                accuracy = self.calculate_accuracy(recommendations)
                
                test_result = {
                    'product_id': product_id,
                    'accuracy': accuracy,
                    'recommendations_count': len(recommendations),
                    'success': len(recommendations) > 0
                }
                
                results['tests'].append(test_result)
                print(f"   ✅ {product_id}: Accuracy = {accuracy:.1f}%")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'accuracy': 0.0,
                    'error': str(e),
                    'success': False
                }
                results['tests'].append(test_result)
                print(f"   ❌ {product_id}: Gabim - {str(e)}")
        
        # Llogarit statistikat
        successful_tests = [test for test in results['tests'] if test['success']]
        avg_accuracy = np.mean([test['accuracy'] for test in successful_tests]) if successful_tests else 0.0
        
        results['summary'] = {
            'total_tests': len(results['tests']),
            'successful_tests': len(successful_tests),
            'average_accuracy': avg_accuracy,
            'min_accuracy': min([test['accuracy'] for test in successful_tests]) if successful_tests else 0.0,
            'max_accuracy': max([test['accuracy'] for test in successful_tests]) if successful_tests else 0.0
        }
        
        self.results['accuracy'] = results
        return results
    
    def test_precision(self):
        """Testimi i precision"""
        print("🧪 Testimi i precision...")
        
        results = {
            'test_name': 'Precision Test',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        for product_id in self.test_products:
            try:
                recommendations = self.recommender.get_hybrid_recommendations(product_id, 4)
                precision = self.calculate_precision(recommendations)
                
                test_result = {
                    'product_id': product_id,
                    'precision': precision,
                    'recommendations_count': len(recommendations),
                    'success': len(recommendations) > 0
                }
                
                results['tests'].append(test_result)
                print(f"   ✅ {product_id}: Precision = {precision:.1f}%")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'precision': 0.0,
                    'error': str(e),
                    'success': False
                }
                results['tests'].append(test_result)
                print(f"   ❌ {product_id}: Gabim - {str(e)}")
        
        # Llogarit statistikat
        successful_tests = [test for test in results['tests'] if test['success']]
        avg_precision = np.mean([test['precision'] for test in successful_tests]) if successful_tests else 0.0
        
        results['summary'] = {
            'total_tests': len(results['tests']),
            'successful_tests': len(successful_tests),
            'average_precision': avg_precision,
            'min_precision': min([test['precision'] for test in successful_tests]) if successful_tests else 0.0,
            'max_precision': max([test['precision'] for test in successful_tests]) if successful_tests else 0.0
        }
        
        self.results['precision'] = results
        return results
    
    def test_recall(self):
        """Testimi i recall"""
        print("🧪 Testimi i recall...")
        
        results = {
            'test_name': 'Recall Test',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        for product_id in self.test_products:
            try:
                recommendations = self.recommender.get_hybrid_recommendations(product_id, 4)
                recall = self.calculate_recall(recommendations)
                
                test_result = {
                    'product_id': product_id,
                    'recall': recall,
                    'recommendations_count': len(recommendations),
                    'success': len(recommendations) > 0
                }
                
                results['tests'].append(test_result)
                print(f"   ✅ {product_id}: Recall = {recall:.1f}%")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'recall': 0.0,
                    'error': str(e),
                    'success': False
                }
                results['tests'].append(test_result)
                print(f"   ❌ {product_id}: Gabim - {str(e)}")
        
        # Llogarit statistikat
        successful_tests = [test for test in results['tests'] if test['success']]
        avg_recall = np.mean([test['recall'] for test in successful_tests]) if successful_tests else 0.0
        
        results['summary'] = {
            'total_tests': len(results['tests']),
            'successful_tests': len(successful_tests),
            'average_recall': avg_recall,
            'min_recall': min([test['recall'] for test in successful_tests]) if successful_tests else 0.0,
            'max_recall': max([test['recall'] for test in successful_tests]) if successful_tests else 0.0
        }
        
        self.results['recall'] = results
        return results
    
    def test_f1_score(self):
        """Testimi i F1-score"""
        print("🧪 Testimi i F1-score...")
        
        results = {
            'test_name': 'F1-Score Test',
            'timestamp': datetime.now().isoformat(),
            'tests': []
        }
        
        for product_id in self.test_products:
            try:
                recommendations = self.recommender.get_hybrid_recommendations(product_id, 4)
                precision = self.calculate_precision(recommendations)
                recall = self.calculate_recall(recommendations)
                f1_score = self.calculate_f1_score(precision, recall)
                
                test_result = {
                    'product_id': product_id,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1_score,
                    'recommendations_count': len(recommendations),
                    'success': len(recommendations) > 0
                }
                
                results['tests'].append(test_result)
                print(f"   ✅ {product_id}: F1-Score = {f1_score:.1f}%")
                
            except Exception as e:
                test_result = {
                    'product_id': product_id,
                    'f1_score': 0.0,
                    'error': str(e),
                    'success': False
                }
                results['tests'].append(test_result)
                print(f"   ❌ {product_id}: Gabim - {str(e)}")
        
        # Llogarit statistikat
        successful_tests = [test for test in results['tests'] if test['success']]
        avg_f1_score = np.mean([test['f1_score'] for test in successful_tests]) if successful_tests else 0.0
        
        results['summary'] = {
            'total_tests': len(results['tests']),
            'successful_tests': len(successful_tests),
            'average_f1_score': avg_f1_score,
            'min_f1_score': min([test['f1_score'] for test in successful_tests]) if successful_tests else 0.0,
            'max_f1_score': max([test['f1_score'] for test in successful_tests]) if successful_tests else 0.0
        }
        
        self.results['f1_score'] = results
        return results
    
    def run_all_tests(self):
        """Ekzekuton të gjitha testet"""
        print("🚀 FILLIMI I TESTEVE TË METRIKAVE KRYESORE")
        print("=" * 60)
        
        # Ekzekuto testet
        self.test_accuracy()
        print()
        self.test_precision()
        print()
        self.test_recall()
        print()
        self.test_f1_score()
        print()
        
        # Krijo raportin përfundimtar
        self.create_final_report()
    
    def create_final_report(self):
        """Krijon raportin përfundimtar"""
        print("📊 RAPORTI PËRFUNDIMTAR I METRIKAVE")
        print("=" * 50)
        
        # Llogarit statistikat e përgjithshme
        total_tests = 0
        total_successful = 0
        
        for metric, results in self.results.items():
            summary = results['summary']
            total_tests += summary['total_tests']
            total_successful += summary['successful_tests']
            
            print(f"\n{metric.upper()}:")
            if 'average_accuracy' in summary:
                print(f"   Mesatarja: {summary['average_accuracy']:.1f}%")
                print(f"   Min: {summary['min_accuracy']:.1f}%")
                print(f"   Max: {summary['max_accuracy']:.1f}%")
            elif 'average_precision' in summary:
                print(f"   Mesatarja: {summary['average_precision']:.1f}%")
                print(f"   Min: {summary['min_precision']:.1f}%")
                print(f"   Max: {summary['max_precision']:.1f}%")
            elif 'average_recall' in summary:
                print(f"   Mesatarja: {summary['average_recall']:.1f}%")
                print(f"   Min: {summary['min_recall']:.1f}%")
                print(f"   Max: {summary['max_recall']:.1f}%")
            elif 'average_f1_score' in summary:
                print(f"   Mesatarja: {summary['average_f1_score']:.1f}%")
                print(f"   Min: {summary['min_f1_score']:.1f}%")
                print(f"   Max: {summary['max_f1_score']:.1f}%")
        
        overall_success_rate = (total_successful / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\nTOTALI:")
        print(f"   Teste totale: {total_tests}")
        print(f"   Teste të suksesshme: {total_successful}")
        print(f"   Shkalla e suksesit: {overall_success_rate:.1f}%")
        
        # Ruaj rezultatet në skedar
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """Ruan rezultatet në skedar JSON"""
        filename = f"test_results_core_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rezultatet u ruajtën në: {filename}")

if __name__ == "__main__":
    tester = CoreMetricsTester()
    tester.run_all_tests()
