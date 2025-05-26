import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import random
from datetime import datetime, timedelta
from app.models import HealthData
from app import db

def prepare_data_for_prophet(data, disease_filter=None, country_filter=None):
    """Prepare data for Prophet forecasting model."""
    df = pd.DataFrame(data)
    
    # Apply filters if provided
    if disease_filter:
        df = df[df['disease'] == disease_filter]
    if country_filter:
        df = df[df['country'] == country_filter]
    
    # Group by date and sum cases
    df_grouped = df.groupby('date').agg({'cases': 'sum', 'deaths': 'sum', 'recovered': 'sum'}).reset_index()
    
    # Prophet requires columns 'ds' and 'y'
    df_prophet = df_grouped.rename(columns={'date': 'ds', 'cases': 'y'})
    
    return df_prophet

def forecast_with_prophet(data, periods=30):
    """Forecast future disease cases using Prophet."""
    # Initialize and fit Prophet model
    m = Prophet(yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=False)
    m.fit(data)
    
    # Create future dataframe for predictions
    future = m.make_future_dataframe(periods=periods)
    
    # Make predictions
    forecast = m.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

def calculate_risk_score(data, weights=None):
    """Calculate risk score for different regions based on multiple factors."""
    df = pd.DataFrame(data)
    
    # Default weights if not provided
    if weights is None:
        weights = {
            'cases': 0.4,
            'deaths': 0.4,
            'population_density': 0.1,
            'healthcare_index': 0.1
        }
    
    # Calculate case fatality rate
    df['cfr'] = df['deaths'] / df['cases']
    
    # Normalize the data
    scaler = StandardScaler()
    features = ['cases', 'deaths', 'cfr']
    df_scaled = pd.DataFrame(scaler.fit_transform(df[features]), columns=features)
    
    # Calculate risk score (simplified version)
    df['risk_score'] = (
        weights['cases'] * df_scaled['cases'] +
        weights['deaths'] * df_scaled['deaths']
    )
    
    return df[['country', 'disease', 'risk_score']]

def get_time_series_analysis(data, country=None, disease=None):
    """Perform time series analysis on the data."""
    df = pd.DataFrame(data)
    
    # Apply filters if provided
    if disease:
        df = df[df['disease'] == disease]
    if country:
        df = df[df['country'] == country]
    
    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])
    
    # Sort by date
    df = df.sort_values('date')
    
    # Calculate rolling averages
    df['cases_7day_avg'] = df['cases'].rolling(window=7, min_periods=1).mean()
    df['deaths_7day_avg'] = df['deaths'].rolling(window=7, min_periods=1).mean()
    
    # Calculate growth rate
    df['cases_growth'] = df['cases'].pct_change()
    df['deaths_growth'] = df['deaths'].pct_change()
    
    return df

def get_correlation_analysis(data):
    """Analyze correlations between different variables."""
    df = pd.DataFrame(data)
    
    # Calculate correlation matrix
    corr_matrix = df[['cases', 'deaths', 'recovered']].corr()
    
    return corr_matrix.to_dict()

def simulate_outbreak(initial_cases, r0, days, immunity_rate=0.0):
    """Simulate a disease outbreak using a simple SIR model."""
    population = 1000000  # Assuming a population of 1 million
    
    susceptible = population - initial_cases
    infected = initial_cases
    recovered = 0
    
    results = []
    
    for day in range(days):
        # Simple SIR model calculations
        new_infections = r0 * infected * susceptible / population * (1 - immunity_rate)
        new_recoveries = infected * 0.1  # Assuming 10% recovery rate
        
        susceptible -= new_infections
        infected += new_infections - new_recoveries
        recovered += new_recoveries
        
        results.append({
            'day': day,
            'susceptible': int(susceptible),
            'infected': int(infected),
            'recovered': int(recovered)
        })
    
    return results

def generate_sample_data(days=30):
    """Generate sample health data for testing"""
    # Clear existing data
    HealthData.query.delete()
    
    base_date = datetime.utcnow() - timedelta(days=days)
    
    for i in range(days * 3):  # 3 records per day on average
        timestamp = base_date + timedelta(
            days=i // 3,
            hours=random.randint(6, 22),
            minutes=random.randint(0, 59)
        )
        
        health_record = HealthData(
            user_id='sample_user',
            timestamp=timestamp,
            heart_rate=random.randint(60, 100),
            blood_pressure_systolic=random.randint(110, 140),
            blood_pressure_diastolic=random.randint(70, 90),
            temperature=round(random.uniform(97.0, 99.5), 1),
            weight=round(random.uniform(150, 180), 1),
            steps=random.randint(3000, 12000),
            sleep_hours=round(random.uniform(6, 9), 1)
        )
        
        db.session.add(health_record)
    
    db.session.commit()

def get_health_stats():
    """Calculate health statistics"""
    recent_data = HealthData.query.filter(
        HealthData.timestamp >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    if not recent_data:
        return {}
    
    heart_rates = [d.heart_rate for d in recent_data if d.heart_rate]
    steps = [d.steps for d in recent_data if d.steps]
    sleep_hours = [d.sleep_hours for d in recent_data if d.sleep_hours]
    
    stats = {
        'total_records': len(recent_data),
        'avg_heart_rate': round(sum(heart_rates) / len(heart_rates), 1) if heart_rates else 0,
        'avg_steps': round(sum(steps) / len(steps)) if steps else 0,
        'avg_sleep': round(sum(sleep_hours) / len(sleep_hours), 1) if sleep_hours else 0,
        'last_updated': recent_data[0].timestamp.isoformat() if recent_data else None
    }
    
    return stats