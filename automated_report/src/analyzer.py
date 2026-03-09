import pandas as pd
import numpy as np

class DataAnalyzer:
    def __init__(self, df):
        self.df = df
    
    def get_summary_statistics(self):
        stats = {}
        stats['shape'] = self.df.shape
        stats['columns'] = list(self.df.columns)
        stats['dtypes'] = self.df.dtypes.apply(str).to_dict()
        stats['numerical'] = self.df.describe().to_dict()
        stats['categorical'] = {}
        
        for col in self.df.select_dtypes(include=['object']).columns:
            stats['categorical'][col] = self.df[col].value_counts().head(5).to_dict()
        
        return stats
    
    def get_key_insights(self):
        insights = []
        
        for col in self.df.select_dtypes(include=[np.number]).columns:
            mean_val = self.df[col].mean()
            median_val = self.df[col].median()
            std_val = self.df[col].std()
            
            if std_val > 0:
                insights.append({
                    'type': 'distribution',
                    'column': col,
                    'message': f"'{col}' has mean={mean_val:.2f}, median={median_val:.2f}. Distribution is {'skewed' if abs(mean_val - median_val) > std_val else 'normal'}."
                })
        
        for col in self.df.select_dtypes(include=['object']).columns:
            top_value = self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'N/A'
            top_count = (self.df[col] == top_value).sum()
            insights.append({
                'type': 'categorical',
                'column': col,
                'message': f"Most common value in '{col}': '{top_value}' ({top_count} occurrences, {top_count/len(self.df)*100:.1f}%)"
            })
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            corr_matrix = self.df[numeric_cols].corr()
            for i, col1 in enumerate(corr_matrix.columns):
                for col2 in corr_matrix.columns[i+1:]:
                    corr_val = corr_matrix.loc[col1, col2]
                    if abs(corr_val) > 0.5:
                        insights.append({
                            'type': 'correlation',
                            'column': f"{col1} & {col2}",
                            'message': f"Strong correlation between '{col1}' and '{col2}': {corr_val:.3f}"
                        })
        
        return insights
    
    def check_data_quality(self):
        quality = {}
        quality['missing_values'] = self.df.isnull().sum().to_dict()
        quality['missing_percent'] = (self.df.isnull().sum() / len(self.df) * 100).to_dict()
        quality['duplicate_rows'] = self.df.duplicated().sum()
        quality['total_rows'] = len(self.df)
        
        return quality
