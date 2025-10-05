#!/usr/bin/env python3
"""
Testet për krahasimin e algoritmeve të rekomandimit
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

class ComparisonTester:
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://root:mysqlZ97*@localhost/dataset_db')
        self.recommender = AdvancedRecommendationEngine(self.engine)
        self.results = {}
        self.test_products = ['B0009V1YR8', 'B0043OYFKU', 'B0000YUXI0', 'B0000020TR', 'B00000JGVX']
        
    def calculate_metrics(self, recommendations):
        """Llogarit metrikat për rekomandime"""
        if not recommendations:
            return {
                'accuracy': 0.0,
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0,
                'diversity': 0.0,
                'avg_rating': 0.0
            }
        
        # Llogarit accuracy (rating > 3.5)
        correct_recommendations = sum(1 for rec in recommendations if rec.get('Rating', 0) > 3.5)
        accuracy = (correct_recommendations / len(recommendations)) * 100
        
        # Llogarit precision
        precision = accuracy  # Për thjeshtësi, precision = accuracy
        
        # Llogarit recall (supozojmë 4 rekomandime të mundshme)
        recall = (correct_recommendations / 4) * 100
        
        # Llogarit F1-score
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Llogarit diversitetin (numri i kategorive të ndryshme)
        categories = set(rec.get('ProductType', '') for rec in recommendations)
        diversity = (len(categories) / len(recommendations)) * 100 if recommendations else 0
        
        # Llogarit rating mesatar
        avg_rating = sum(rec.get('Rating', 0) for rec in recommendations) / len(recommendations)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'diversity': diversity,
            'avg_rating': avg_rating
        }
    
    def test_individual_algorithms(self):
        """Testimi i algoritmeve individuale"""
        print("🧪 Testimi i algoritmeve individuale...")
        
        results = {
            'test_name': 'Individual Algorithms Comparison',
            'timestamp': datetime.now().isoformat(),
            'algorithms': {}
        }
        
        algorithms = {
            'content_based': self.recommender.get_similar_products,
            'collaborative': self.recommender.get_collaborative_recommendations,
            'trend_based': self.recommender.get_trending_recommendations
        }
        
        for algo_name, algo_func in algorithms.items():
            print(f"   Testimi i {algo_name}...")
            
            algo_results = {
                'test_name': algo_name,
                'tests': [],
                'metrics': []
            }
            
            for product_id in self.test_products:
                try:
                    start_time = time.time()
                    recommendations = algo_func(product_id, 4)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    metrics = self.calculate_metrics(recommendations)
                    
                    test_result = {
                        'product_id': product_id,
                        'success': len(recommendations) > 0,
                        'recommendations_count': len(recommendations),
                        'response_time': response_time,
                        'metrics': metrics
                    }
                    
                    algo_results['tests'].append(test_result)
                    algo_results['metrics'].append(metrics)
                    
                    print(f"     ✅ {product_id}: {len(recommendations)} rekomandime, F1={metrics['f1_score']:.1f}%")
                    
                except Exception as e:
                    test_result = {
                        'product_id': product_id,
                        'success': False,
                        'error': str(e),
                        'response_time': 0,
                        'metrics': self.calculate_metrics([])
                    }
                    algo_results['tests'].append(test_result)
                    algo_results['metrics'].append(test_result['metrics'])
                    print(f"     ❌ {product_id}: Gabim - {str(e)}")
            
            # Llogarit statistikat për algoritmin
            successful_tests = [test for test in algo_results['tests'] if test['success']]
            if successful_tests:
                avg_metrics = {}
                for metric in ['accuracy', 'precision', 'recall', 'f1_score', 'diversity', 'avg_rating']:
                    values = [test['metrics'][metric] for test in successful_tests]
                    avg_metrics[f'avg_{metric}'] = np.mean(values)
                    avg_metrics[f'min_{metric}'] = np.min(values)
                    avg_metrics[f'max_{metric}'] = np.max(values)
                
                avg_response_time = np.mean([test['response_time'] for test in successful_tests])
                
                algo_results['summary'] = {
                    'total_tests': len(algo_results['tests']),
                    'successful_tests': len(successful_tests),
                    'success_rate': (len(successful_tests) / len(algo_results['tests'])) * 100,
                    'avg_response_time': avg_response_time,
                    **avg_metrics
                }
            else:
                algo_results['summary'] = {
                    'total_tests': len(algo_results['tests']),
                    'successful_tests': 0,
                    'success_rate': 0,
                    'avg_response_time': 0
                }
            
            results['algorithms'][algo_name] = algo_results
        
        self.results['individual_algorithms'] = results
        return results
    
    def test_hybrid_vs_individual(self):
        """Krahasimi i sistemit hibrid me algoritmet individuale"""
        print("🧪 Krahasimi i sistemit hibrid me algoritmet individuale...")
        
        results = {
            'test_name': 'Hybrid vs Individual Comparison',
            'timestamp': datetime.now().isoformat(),
            'comparisons': []
        }
        
        for product_id in self.test_products:
            print(f"   Testimi i {product_id}...")
            
            comparison = {
                'product_id': product_id,
                'algorithms': {}
            }
            
            # Testo algoritmet individuale
            individual_algorithms = {
                'content_based': self.recommender.get_similar_products,
                'collaborative': self.recommender.get_collaborative_recommendations,
                'trend_based': self.recommender.get_trending_recommendations
            }
            
            for algo_name, algo_func in individual_algorithms.items():
                try:
                    start_time = time.time()
                    recommendations = algo_func(product_id, 4)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    metrics = self.calculate_metrics(recommendations)
                    
                    comparison['algorithms'][algo_name] = {
                        'success': len(recommendations) > 0,
                        'recommendations_count': len(recommendations),
                        'response_time': response_time,
                        'metrics': metrics
                    }
                    
                except Exception as e:
                    comparison['algorithms'][algo_name] = {
                        'success': False,
                        'error': str(e),
                        'response_time': 0,
                        'metrics': self.calculate_metrics([])
                    }
            
            # Testo sistemin hibrid
            try:
                start_time = time.time()
                recommendations = self.recommender.get_hybrid_recommendations(product_id, 4)
                end_time = time.time()
                
                response_time = end_time - start_time
                metrics = self.calculate_metrics(recommendations)
                
                comparison['algorithms']['hybrid'] = {
                    'success': len(recommendations) > 0,
                    'recommendations_count': len(recommendations),
                    'response_time': response_time,
                    'metrics': metrics
                }
                
            except Exception as e:
                comparison['algorithms']['hybrid'] = {
                    'success': False,
                    'error': str(e),
                    'response_time': 0,
                    'metrics': self.calculate_metrics([])
                }
            
            results['comparisons'].append(comparison)
            
            # Printo rezultatet
            print(f"     Content-based: F1={comparison['algorithms']['content_based']['metrics']['f1_score']:.1f}%")
            print(f"     Collaborative: F1={comparison['algorithms']['collaborative']['metrics']['f1_score']:.1f}%")
            print(f"     Trend-based: F1={comparison['algorithms']['trend_based']['metrics']['f1_score']:.1f}%")
            print(f"     Hybrid: F1={comparison['algorithms']['hybrid']['metrics']['f1_score']:.1f}%")
        
        # Llogarit statistikat e përgjithshme
        all_metrics = {}
        for comparison in results['comparisons']:
            for algo_name, algo_data in comparison['algorithms'].items():
                if algo_name not in all_metrics:
                    all_metrics[algo_name] = []
                all_metrics[algo_name].append(algo_data['metrics'])
        
        summary = {}
        for algo_name, metrics_list in all_metrics.items():
            if metrics_list:
                summary[algo_name] = {}
                for metric in ['accuracy', 'precision', 'recall', 'f1_score', 'diversity', 'avg_rating']:
                    values = [m[metric] for m in metrics_list if metric in m]
                    if values:
                        summary[algo_name][f'avg_{metric}'] = np.mean(values)
                        summary[algo_name][f'min_{metric}'] = np.min(values)
                        summary[algo_name][f'max_{metric}'] = np.max(values)
        
        results['summary'] = summary
        self.results['hybrid_vs_individual'] = results
        return results
    
    def run_all_tests(self):
        """Ekzekuton të gjitha testet"""
        print("🚀 FILLIMI I TESTEVE TË KRAHASIMIT")
        print("=" * 60)
        
        # Ekzekuto testet
        self.test_individual_algorithms()
        print()
        self.test_hybrid_vs_individual()
        print()
        
        # Krijo raportin përfundimtar
        self.create_final_report()
    
    def create_final_report(self):
        """Krijon raportin përfundimtar"""
        print("📊 RAPORTI PËRFUNDIMTAR I KRAHASIMIT")
        print("=" * 50)
        
        # Raporti për algoritmet individuale
        if 'individual_algorithms' in self.results:
            print("\nALGORITMET INDIVIDUALE:")
            for algo_name, algo_data in self.results['individual_algorithms']['algorithms'].items():
                summary = algo_data['summary']
                print(f"\n{algo_name.upper()}:")
                print(f"   Sukses: {summary['successful_tests']}/{summary['total_tests']} ({summary['success_rate']:.1f}%)")
                print(f"   Koha mesatare: {summary['avg_response_time']:.3f}s")
                if 'avg_f1_score' in summary:
                    print(f"   F1-Score mesatar: {summary['avg_f1_score']:.1f}%")
                if 'avg_accuracy' in summary:
                    print(f"   Accuracy mesatar: {summary['avg_accuracy']:.1f}%")
                if 'avg_diversity' in summary:
                    print(f"   Diversiteti mesatar: {summary['avg_diversity']:.1f}%")
        
        # Raporti për krahasimin hibrid vs individual
        if 'hybrid_vs_individual' in self.results:
            print("\nKRAHASIMI HIBRID VS INDIVIDUAL:")
            summary = self.results['hybrid_vs_individual']['summary']
            
            for algo_name, metrics in summary.items():
                print(f"\n{algo_name.upper()}:")
                if 'avg_f1_score' in metrics:
                    print(f"   F1-Score mesatar: {metrics['avg_f1_score']:.1f}%")
                if 'avg_accuracy' in metrics:
                    print(f"   Accuracy mesatar: {metrics['avg_accuracy']:.1f}%")
                if 'avg_diversity' in metrics:
                    print(f"   Diversiteti mesatar: {metrics['avg_diversity']:.1f}%")
                if 'avg_avg_rating' in metrics:
                    print(f"   Rating mesatar: {metrics['avg_avg_rating']:.2f}")
        
        # Ruaj rezultatet në skedar
        self.save_results_to_file()
    
    def save_results_to_file(self):
        """Ruan rezultatet në skedar JSON"""
        filename = f"test_results_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rezultatet u ruajtën në: {filename}")

if __name__ == "__main__":
    tester = ComparisonTester()
    tester.run_all_tests()
