import matplotlib.pyplot as plt
import seaborn as sns
import json
import pandas as pd
import os
import numpy as np

class ResultVisualizer:
    def __init__(self):
        """Inicializon vizualizuesin"""
        # Krijo direktorinë për grafikët nëse nuk ekziston
        self.graphs_dir = os.path.join(os.path.dirname(__file__), 'graphs')
        if not os.path.exists(self.graphs_dir):
            os.makedirs(self.graphs_dir)
        
        self.results = self.load_test_results()

    def generate_test_data(self):
        """Gjeneron të dhëna test për vizualizim"""
        # Gjenero 10 pika të dhënash për të simuluar përdorimin e memories përgjatë kohës
        memory_usage_pattern = [
            1200, 1500, 1800, 2100, 1900, 2300, 2000, 2200, 1800, 1600
        ]
        
        test_data = []
        
        for i, memory_usage in enumerate(memory_usage_pattern):
            data_point = {
                'detailed_results': {
                    'content_based_analysis': {
                        'category_match_rate': 0.85,
                        'avg_response_time': 180
                    },
                    'collaborative_analysis': {
                        'user_preference_match': 0.78,
                        'avg_response_time': 200
                    },
                    'hybrid_analysis': {
                        'overall_accuracy': 0.88,
                        'avg_response_time': 190
                    }
                },
                'resource_metrics': {
                    'cache_performance': {
                        'cache_hit_rate': 0.90,
                        'cache_miss_rate': 0.10
                    },
                    'memory_usage': {
                        'memory_used_mb': memory_usage,
                        'timestamp': f'2024-03-{i+1:02d}'
                    }
                }
            }
            test_data.append(data_point)
        
        # Krijo direktorinë testing nëse nuk ekziston
        testing_dir = os.path.join(os.path.dirname(__file__), 'testing')
        if not os.path.exists(testing_dir):
            os.makedirs(testing_dir)
        
        # Ruaj të dhënat në testing/test_results_sample.json
        test_file_path = os.path.join(testing_dir, 'test_results_sample.json')
        with open(test_file_path, 'w') as f:
            json.dump(test_data, f, indent=4)
        
        return test_data

    def load_test_results(self):
        """Ngarkon rezultatet nga JSON files"""
        testing_dir = os.path.join(os.path.dirname(__file__), 'testing')
        test_file_path = os.path.join(testing_dir, 'test_results_sample.json')
        
        print("\nLooking for test data...")
        
        if not os.path.exists(test_file_path):
            print("No test file found. Generating sample data...")
            return self.generate_test_data()
        
        try:
            with open(test_file_path, 'r') as f:
                data = json.load(f)
                print("Test data loaded successfully")
                return data
        except Exception as e:
            print(f"Error loading test data: {str(e)}")
            print("Generating new test data...")
            return self.generate_test_data()

    def plot_accuracy_metrics(self):
        """Vizualizon metrikat e saktësisë"""
        plt.figure(figsize=(12, 6))
        
        try:
            # Ekstrakto metrikat nga rezultatet me error handling
            metrics = {
                'Content-based': [],
                'Collaborative': [],
                'Hybrid': []
            }
            
            for r in self.results:
                if 'detailed_results' in r:
                    content = r.get('detailed_results', {}).get('content_based_analysis', {})
                    collab = r.get('detailed_results', {}).get('collaborative_analysis', {})
                    hybrid = r.get('detailed_results', {}).get('hybrid_analysis', {})
                    
                    metrics['Content-based'].append(content.get('category_match_rate', 0))
                    metrics['Collaborative'].append(collab.get('user_preference_match', 0))
                    metrics['Hybrid'].append(hybrid.get('overall_accuracy', 0))
            
            df = pd.DataFrame(metrics)
            df.mean().plot(kind='bar')
            plt.title('Krahasimi i Saktësisë së Metodave')
            plt.ylabel('Saktësia')
            plt.ylim(0, 1)
            plt.tight_layout()
            plt.savefig(os.path.join(self.graphs_dir, 'accuracy_comparison.png'))
            plt.close()
            
        except Exception as e:
            print(f"Error in plot_accuracy_metrics: {str(e)}")
            print("Available keys in results:", self.results[0].keys() if self.results else "No results")

    def plot_response_times(self):
        """Vizualizon kohën e përgjigjes"""
        plt.figure(figsize=(10, 6))
        
        try:
            times = {
                'Content-based': [],
                'Collaborative': [],
                'Hybrid': []
            }
            
            for r in self.results:
                if 'detailed_results' in r:
                    content = r.get('detailed_results', {}).get('content_based_analysis', {})
                    collab = r.get('detailed_results', {}).get('collaborative_analysis', {})
                    hybrid = r.get('detailed_results', {}).get('hybrid_analysis', {})
                    
                    times['Content-based'].append(content.get('avg_response_time', 0))
                    times['Collaborative'].append(collab.get('avg_response_time', 0))
                    times['Hybrid'].append(hybrid.get('avg_response_time', 0))
            
            df = pd.DataFrame(times)
            sns.boxplot(data=df)
            plt.title('Shpërndarja e Kohës së Përgjigjes')
            plt.ylabel('Koha (ms)')
            plt.tight_layout()
            plt.savefig(os.path.join(self.graphs_dir, 'response_times.png'))
            plt.close()
            
        except Exception as e:
            print(f"Error in plot_response_times: {str(e)}")

    def plot_cache_performance(self):
        """Vizualizon performancën e cache"""
        plt.figure(figsize=(8, 8))
        
        try:
            cache_metrics = []
            for r in self.results:
                if 'resource_metrics' in r:
                    cache = r.get('resource_metrics', {}).get('cache_performance', {})
                    cache_metrics.append(cache)
            
            hit_rates = [m.get('cache_hit_rate', 0) for m in cache_metrics]
            miss_rates = [m.get('cache_miss_rate', 0) for m in cache_metrics]
            
            plt.pie([np.mean(hit_rates), np.mean(miss_rates)], 
                    labels=['Cache Hits', 'Cache Misses'],
                    autopct='%1.1f%%',
                    colors=['#2ecc71', '#e74c3c'])
            plt.title('Cache Performance')
            plt.savefig(os.path.join(self.graphs_dir, 'cache_performance.png'))
            plt.close()
            
        except Exception as e:
            print(f"Error in plot_cache_performance: {str(e)}")

    def plot_memory_usage(self):
        """Vizualizon përdorimin e memories"""
        plt.figure(figsize=(12, 6))
        
        try:
            memory_data = []
            timestamps = []
            
            for r in self.results:
                if 'resource_metrics' in r:
                    memory = r.get('resource_metrics', {}).get('memory_usage', {})
                    if memory:
                        memory_used = memory.get('memory_used_mb', 0)
                        timestamp = memory.get('timestamp', '')
                        memory_data.append(memory_used)
                        timestamps.append(timestamp)
            
            if memory_data:
                plt.plot(range(len(memory_data)), memory_data, marker='o', linestyle='-', linewidth=2)
                plt.title('Përdorimi i Memories Gjatë Testimit')
                plt.ylabel('Memory Usage (MB)')
                plt.xlabel('Ekzekutimet')
                plt.grid(True, linestyle='--', alpha=0.7)
                
                # Formato boshtin x me timestamps
                if timestamps:
                    plt.xticks(range(len(timestamps)), 
                              [t.split()[0] for t in timestamps], 
                              rotation=45)
                
                plt.tight_layout()
                plt.savefig(os.path.join(self.graphs_dir, 'memory_usage.png'))
            else:
                print("No memory usage data available")
            
            plt.close()
            
        except Exception as e:
            print(f"Error in plot_memory_usage: {str(e)}")
            if self.results:
                print("Available keys:", self.results[0].keys())

    def generate_all_visualizations(self):
        """Gjeneron të gjitha vizualizimet"""
        self.plot_accuracy_metrics()
        self.plot_response_times()
        self.plot_cache_performance()
        self.plot_memory_usage()
        print("Vizualizimet u gjeneruan me sukses!")

if __name__ == "__main__":
    visualizer = ResultVisualizer()
    visualizer.generate_all_visualizations() 