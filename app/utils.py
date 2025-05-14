import pandas as pd
from datetime import datetime, timedelta

def load_health_data(file_path):
    """Load health data from CSV file"""
    return pd.read_csv(file_path)

def process_health_data(df):
    """Process and clean health data"""
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df.sort_values('timestamp', ascending=False)

def get_recent_data(df, hours=24):
    """Get data from the last 24 hours"""
    cutoff = datetime.now() - timedelta(hours=hours)
    return df[df['timestamp'] > cutoff] 