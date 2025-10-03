#!/usr/bin/env python3
"""
Script kryesor për ekzekutimin e të gjitha testeve
Për temën e masterit: ENHANCING DROPSHIPPING PERFORMANCE THROUGH RECOMMENDATION ENGINES
"""

import sys
import os
import time
import json
from datetime import datetime

# Importo testet
from test_algorithm_functionality import AlgorithmFunctionalityTester
from test_core_metrics import CoreMetricsTester
from test_performance import PerformanceTester
from test_integration import IntegrationTester
from test_edge_cases import EdgeCasesTester
from test_comparison import ComparisonTester

class MasterThesisTestRunner:
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    def run_algorithm_functionality_tests(self):
        """Ekzekuton testet e funksionalitetit të algoritmeve"""
        print("🔬 TESTET E FUNKSIONALITETIT TË ALGORITMEVE")
        print("=" * 60)
        
        tester = AlgorithmFunctionalityTester()
        tester.run_all_tests()
        self.results['algorithm_functionality'] = tester.results
        
        print("\n✅ Testet e funksionalitetit të algoritmeve u përfunduan\n")
    
    def run_core_metrics_tests(self):
        """Ekzekuton testet e metrikave kryesore"""
        print("📊 TESTET E METRIKAVE KRYESORE")
        print("=" * 60)
        
        tester = CoreMetricsTester()
        tester.run_all_tests()
        self.results['core_metrics'] = tester.results
        
        print("\n✅ Testet e metrikave kryesore u përfunduan\n")
    
    def run_performance_tests(self):
        """Ekzekuton testet e performancës"""
        print("⚡ TESTET E PERFORMANCËS")
        print("=" * 60)
        
        tester = PerformanceTester()
        tester.run_all_tests()
        self.results['performance'] = tester.results
        
        print("\n✅ Testet e performancës u përfunduan\n")
    
    def run_integration_tests(self):
        """Ekzekuton testet e integrimit"""
        print("🔗 TESTET E INTEGRIMIT")
        print("=" * 60)
        
        tester = IntegrationTester()
        tester.run_all_tests()
        self.results['integration'] = tester.results
        
        print("\n✅ Testet e integrimit u përfunduan\n")
    
    def run_edge_cases_tests(self):
        """Ekzekuton testet e edge cases"""
        print("🎯 TESTET E EDGE CASES")
        print("=" * 60)
        
        tester = EdgeCasesTester()
        tester.run_all_tests()
        self.results['edge_cases'] = tester.results
        
        print("\n✅ Testet e edge cases u përfunduan\n")
    
    def run_comparison_tests(self):
        """Ekzekuton testet e krahasimit"""
        print("⚖️  TESTET E KRAHASIMIT")
        print("=" * 60)
        
        tester = ComparisonTester()
        tester.run_all_tests()
        self.results['comparison'] = tester.results
        
        print("\n✅ Testet e krahasimit u përfunduan\n")
    
    def run_all_tests(self):
        """Ekzekuton të gjitha testet"""
        print("🚀 FILLIMI I TESTEVE TË PLOTA PËR TEMËN E MASTERIT")
        print("=" * 80)
        print("Tema: ENHANCING DROPSHIPPING PERFORMANCE THROUGH RECOMMENDATION ENGINES")
        print("=" * 80)
        
        self.start_time = time.time()
        
        try:
            # Ekzekuto testet në rend
            self.run_algorithm_functionality_tests()
            self.run_core_metrics_tests()
            self.run_performance_tests()
            self.run_integration_tests()
            self.run_edge_cases_tests()
            self.run_comparison_tests()
            
            self.end_time = time.time()
            
            # Krijo raportin përfundimtar
            self.create_final_report()
            
        except Exception as e:
            print(f"\n❌ GABIM NË EKZEKUTIMIN E TESTEVE: {str(e)}")
            self.end_time = time.time()
            self.create_error_report(str(e))
    
    def create_final_report(self):
        """Krijon raportin përfundimtar"""
        print("\n" + "=" * 80)
        print("📊 RAPORTI PËRFUNDIMTAR I TESTEVE")
        print("=" * 80)
        
        total_time = self.end_time - self.start_time
        
        print(f"⏱️  Koha totale e testimit: {total_time:.2f} sekonda ({total_time/60:.1f} minuta)")
        print(f"📅 Data dhe ora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Llogarit statistikat e përgjithshme
        total_tests = 0
        total_successful = 0
        
        for test_category, test_results in self.results.items():
            print(f"\n📋 {test_category.upper().replace('_', ' ')}:")
            
            if isinstance(test_results, dict):
                for sub_category, sub_results in test_results.items():
                    if isinstance(sub_results, dict) and 'summary' in sub_results:
                        summary = sub_results['summary']
                        total_tests += summary.get('total_tests', 0)
                        total_successful += summary.get('successful_tests', 0)
                        
                        success_rate = summary.get('success_rate', 0)
                        print(f"   {sub_category}: {summary.get('successful_tests', 0)}/{summary.get('total_tests', 0)} ({success_rate:.1f}%)")
        
        overall_success_rate = (total_successful / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n🎯 REZULTATI PËRFUNDIMTAR:")
        print(f"   Teste totale: {total_tests}")
        print(f"   Teste të suksesshme: {total_successful}")
        print(f"   Shkalla e suksesit: {overall_success_rate:.1f}%")
        
        # Vlerëso rezultatin
        if overall_success_rate >= 90:
            print(f"   🏆 REZULTATI: E SHKELUR (A+)")
        elif overall_success_rate >= 80:
            print(f"   🥇 REZULTATI: E MIRË (A)")
        elif overall_success_rate >= 70:
            print(f"   🥈 REZULTATI: E KËNAQSHME (B)")
        elif overall_success_rate >= 60:
            print(f"   🥉 REZULTATI: E DOBËT (C)")
        else:
            print(f"   ❌ REZULTATI: E DOBËT (D)")
        
        # Ruaj rezultatet
        self.save_results_to_file()
        
        print(f"\n✅ TË GJITHA TESTET U PËRFUNDUAN ME SUKSES!")
        print(f"📁 Rezultatet u ruajtën në skedarët JSON individualë")
        print(f"📊 Raporti përfundimtar u ruajt në: master_thesis_test_results.json")
    
    def create_error_report(self, error_message):
        """Krijon raportin e gabimit"""
        print(f"\n❌ RAPORTI I GABIMIT")
        print(f"Gabimi: {error_message}")
        print(f"Koha e testimit: {self.end_time - self.start_time:.2f} sekonda")
        
        # Ruaj raportin e gabimit
        error_report = {
            'error': error_message,
            'test_time': self.end_time - self.start_time,
            'timestamp': datetime.now().isoformat(),
            'results': self.results
        }
        
        with open('master_thesis_test_error.json', 'w', encoding='utf-8') as f:
            json.dump(error_report, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Raporti i gabimit u ruajt në: master_thesis_test_error.json")
    
    def save_results_to_file(self):
        """Ruan rezultatet në skedar JSON"""
        final_report = {
            'test_info': {
                'title': 'ENHANCING DROPSHIPPING PERFORMANCE THROUGH RECOMMENDATION ENGINES',
                'timestamp': datetime.now().isoformat(),
                'total_time': self.end_time - self.start_time,
                'test_categories': list(self.results.keys())
            },
            'results': self.results
        }
        
        with open('master_thesis_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("🎓 SISTEMI I TESTIMIT PËR TEMËN E MASTERIT")
    print("=" * 50)
    print("Tema: ENHANCING DROPSHIPPING PERFORMANCE THROUGH RECOMMENDATION ENGINES")
    print("=" * 50)
    print()
    
    runner = MasterThesisTestRunner()
    runner.run_all_tests()
