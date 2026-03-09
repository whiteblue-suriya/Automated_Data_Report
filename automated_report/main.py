import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import pandas as pd
from analyzer import DataAnalyzer
from generator import ReportGenerator

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "sample_data.csv")
    output_path = os.path.join(base_dir, "output", "report.html")
    
    print("Loading data...")
    df = pd.read_csv(data_path)
    
    print("Analyzing data...")
    analyzer = DataAnalyzer(df)
    stats = analyzer.get_summary_statistics()
    insights = analyzer.get_key_insights()
    quality = analyzer.check_data_quality()
    
    print("Generating report...")
    generator = ReportGenerator()
    generator.generate_html_report(
        df=df,
        stats=stats,
        insights=insights,
        quality=quality,
        output_path=output_path
    )
    
    print(f"Report generated successfully: {output_path}")

if __name__ == "__main__":
    main()
