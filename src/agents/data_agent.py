import pandas as pd
from datetime import timedelta

class DataAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.data_path, parse_dates=['date'])
        if 'ctr' not in self.df.columns and 'clicks' in self.df.columns and 'impressions' in self.df.columns:
            self.df['ctr'] = self.df['clicks'] / self.df['impressions']
        if 'roas' not in self.df.columns and 'revenue' in self.df.columns and 'spend' in self.df.columns:
            self.df['roas'] = self.df['revenue'] / self.df['spend']
        return True

    def generate_summary(self):
        if self.df is None:
            self.load_data()
        df = self.df
        summary = {
            "overview":{
                "total_rows": len(df),
                "date_start": str(df['date'].min().date()) if not df['date'].isnull().all() else None,
                "date_end": str(df['date'].max().date()) if not df['date'].isnull().all() else None
            },
            "performance_metrics":{
                "avg_roas": float(df['roas'].mean()) if 'roas' in df else None,
                "avg_ctr": float(df['ctr'].mean()) if 'ctr' in df else None
            },
            "campaign_performance": df.groupby('campaign_name').agg({'spend':'sum','revenue':'sum','roas':'mean','ctr':'mean'}).round(3).to_dict('index'),
            "time_trends": df.groupby('date').agg({'spend':'sum','revenue':'sum','roas':'mean','ctr':'mean'}).round(3).to_dict('index')
        }
        return summary

    def get_low_ctr_campaigns(self, ctr_threshold=0.02):
        if self.df is None:
            self.load_data()
        agg = self.df.groupby('campaign_name').agg({'ctr':'mean','spend':'sum','clicks':'sum','creative_message':'first','creative_type':'first'}).reset_index()
        low = agg[agg['ctr'] < ctr_threshold]
        return low.to_dict('records')

    def get_high_performing_creatives(self, multiplier=1.5, ctr_threshold=0.02):
        if self.df is None:
            self.load_data()
        agg = self.df.groupby('campaign_name').agg({'ctr':'mean','revenue':'sum','creative_message':'first'}).reset_index()
        high = agg[agg['ctr'] > ctr_threshold * multiplier]
        return high.to_dict('records')
