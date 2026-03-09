import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ReportGenerator:
    def __init__(self):
        self.charts_dir = "output/charts"
        os.makedirs(self.charts_dir, exist_ok=True)
    
    def generate_charts(self, df):
        chart_paths = []
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            plt.figure(figsize=(10, 6))
            df[numeric_cols].hist(bins=20, figsize=(12, 8))
            plt.suptitle('Numerical Distributions')
            path = os.path.join(self.charts_dir, 'distributions.png')
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            chart_paths.append(('distributions', path))
        
        if len(numeric_cols) >= 2:
            plt.figure(figsize=(10, 8))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Correlation Matrix')
            path = os.path.join(self.charts_dir, 'correlation.png')
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            chart_paths.append(('correlation', path))
        
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols[:3]:
            plt.figure(figsize=(10, 6))
            df[col].value_counts().head(10).plot(kind='bar')
            plt.title(f'Top Values: {col}')
            plt.xticks(rotation=45)
            path = os.path.join(self.charts_dir, f'categorical_{col}.png')
            plt.tight_layout()
            plt.savefig(path)
            plt.close()
            chart_paths.append((f'categorical_{col}', path))
        
        return chart_paths
    
    def generate_html_report(self, df, stats, insights, quality, output_path):
        chart_paths = self.generate_charts(df)
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Automated Data Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .insight-box {{ background: #e8f4f8; border-left: 4px solid #3498db; padding: 15px; margin: 10px 0; border-radius: 4px; }}
        .warning {{ background: #fff3cd; border-left-color: #ffc107; }}
        .success {{ background: #d4edda; border-left-color: #28a745; }}
        .chart {{ margin: 20px 0; text-align: center; }}
        .chart img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 5px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
        .summary-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .summary-card h3 {{ margin: 0; font-size: 32px; }}
        .summary-card p {{ margin: 5px 0 0; opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Automated Data Analysis Report</h1>
        
        <h2>📈 Dataset Overview</h2>
        <div class="summary-grid">
            <div class="summary-card">
                <h3>{stats['shape'][0]}</h3>
                <p>Total Rows</p>
            </div>
            <div class="summary-card">
                <h3>{stats['shape'][1]}</h3>
                <p>Total Columns</p>
            </div>
            <div class="summary-card">
                <h3>{quality['duplicate_rows']}</h3>
                <p>Duplicate Rows</p>
            </div>
        </div>
        
        <h2>🔍 Key Insights</h2>
"""
        
        for insight in insights:
            html += f"""
        <div class="insight-box">
            <strong>{insight['column']}:</strong> {insight['message']}
        </div>
"""
        
        html += """
        <h2>📊 Data Visualizations</h2>
"""
        for chart_name, chart_path in chart_paths:
            html += f"""
        <div class="chart">
            <img src="{chart_path}" alt="{chart_name}">
        </div>
"""
        
        html += f"""
        <h2>✅ Data Quality Report</h2>
        <table>
            <tr><th>Column</th><th>Missing Values</th><th>Missing %</th></tr>
"""
        
        for col in quality['missing_values']:
            missing = quality['missing_values'][col]
            pct = quality['missing_percent'][col]
            css_class = 'warning' if pct > 0 else 'success'
            html += f"""
            <tr>
                <td>{col}</td>
                <td>{missing}</td>
                <td class="{css_class}">{pct:.2f}%</td>
            </tr>
"""
        
        html += """
        </table>
        
        <h2>📋 Summary Statistics</h2>
        <pre>"""
        html += str(df.describe())
        html += """</pre>
        
        <h2>📝 Column Information</h2>
        <table>
            <tr><th>Column Name</th><th>Data Type</th></tr>
"""
        
        for col, dtype in stats['dtypes'].items():
            html += f"""
            <tr><td>{col}</td><td>{dtype}</td></tr>
"""
        
        html += """
        </table>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
