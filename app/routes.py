from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta

from app.models import Database, HealthData
from app import db
from app.utils import (
    prepare_data_for_prophet, 
    forecast_with_prophet, 
    calculate_risk_score, 
    get_time_series_analysis,
    get_correlation_analysis,
    simulate_outbreak,
    generate_sample_data,
    get_health_stats
)

# Create Blueprint
bp = Blueprint('main', __name__)

# Initialize database
db = Database()

# Import sample data if it doesn't exist in MongoDB
@bp.before_app_first_request
def initialize_database():
    """Initialize the database with sample data if it doesn't exist."""
    if len(db.get_unique_countries('outbreaks')) == 0:
        # Data doesn't exist, import it
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_health_data.csv')
        if os.path.exists(csv_path):
            db.import_csv_to_mongodb(csv_path, 'outbreaks')

# Routes
@bp.route('/')
def index():
    """Render the main dashboard page."""
    # Get all countries and diseases for filters
    countries = db.get_unique_countries('outbreaks')
    diseases = db.get_unique_diseases('outbreaks')
    
    # Get summary stats for the dashboard
    summary_stats = db.get_summary_stats('outbreaks')
    
    return render_template(
        'index.html',
        countries=countries,
        diseases=diseases,
        summary_stats=summary_stats
    )

@bp.route('/api/data')
def get_data():
    """API endpoint to get filtered data."""
    country = request.args.get('country')
    disease = request.args.get('disease')
    
    # Get data based on filters
    if country and disease:
        data = db.get_data_by_country('outbreaks', country)
        data = [d for d in data if d['disease'] == disease]
    elif country:
        data = db.get_data_by_country('outbreaks', country)
    elif disease:
        data = db.get_data_by_disease('outbreaks', disease)
    else:
        data = db.get_all_data('outbreaks')
    
    return jsonify(data)

@bp.route('/api/forecast')
def get_forecast():
    """API endpoint to get disease forecast."""
    country = request.args.get('country')
    disease = request.args.get('disease')
    periods = int(request.args.get('periods', 30))
    
    # Get all data
    data = db.get_all_data('outbreaks')
    
    # Prepare data for Prophet
    prophet_data = prepare_data_for_prophet(data, disease, country)
    
    # Generate forecast
    forecast = forecast_with_prophet(prophet_data, periods)
    
    # Convert to list of dictionaries for JSON response
    result = forecast.to_dict('records')
    
    return jsonify(result)

@bp.route('/api/risk-assessment')
def get_risk_assessment():
    """API endpoint to get risk assessment."""
    country = request.args.get('country')
    disease = request.args.get('disease')
    
    # Get data based on filters
    if country and disease:
        data = db.get_data_by_country('outbreaks', country)
        data = [d for d in data if d['disease'] == disease]
    elif country:
        data = db.get_data_by_country('outbreaks', country)
    elif disease:
        data = db.get_data_by_disease('outbreaks', disease)
    else:
        data = db.get_all_data('outbreaks')
    
    # Calculate risk scores
    risk_data = calculate_risk_score(data)
    
    # Convert to list of dictionaries for JSON response
    result = risk_data.to_dict('records')
    
    return jsonify(result)

@bp.route('/api/time-series')
def get_time_series():
    """API endpoint to get time series analysis."""
    country = request.args.get('country')
    disease = request.args.get('disease')
    
    # Get all data
    data = db.get_all_data('outbreaks')
    
    # Perform time series analysis
    ts_data = get_time_series_analysis(data, country, disease)
    
    # Convert to list of dictionaries for JSON response
    result = ts_data.to_dict('records')
    
    return jsonify(result)

@bp.route('/api/correlations')
def get_correlations():
    """API endpoint to get correlation analysis."""
    country = request.args.get('country')
    disease = request.args.get('disease')
    
    # Get data based on filters
    if country and disease:
        data = db.get_data_by_country('outbreaks', country)
        data = [d for d in data if d['disease'] == disease]
    elif country:
        data = db.get_data_by_country('outbreaks', country)
    elif disease:
        data = db.get_data_by_disease('outbreaks', disease)
    else:
        data = db.get_all_data('outbreaks')
    
    # Calculate correlations
    corr_data = get_correlation_analysis(data)
    
    return jsonify(corr_data)

@bp.route('/api/simulate')
def get_simulation():
    """API endpoint to simulate a disease outbreak."""
    initial_cases = int(request.args.get('initial_cases', 100))
    r0 = float(request.args.get('r0', 2.5))
    days = int(request.args.get('days', 100))
    immunity_rate = float(request.args.get('immunity_rate', 0.0))
    
    # Run simulation
    sim_data = simulate_outbreak(initial_cases, r0, days, immunity_rate)
    
    return jsonify(sim_data)

@bp.route('/api/chatbot', methods=['POST'])
def chatbot():
    """API endpoint for the health chatbot."""
    data = request.json
    query = data.get('query', '')
    
    # This is a simple mock response
    # In a real application, you would integrate with Google Vertex AI here
    if 'covid' in query.lower():
        response = "COVID-19 is a respiratory illness caused by the SARS-CoV-2 virus. Common symptoms include fever, cough, and fatigue."
    elif 'influenza' in query.lower() or 'flu' in query.lower():
        response = "Influenza (flu) is a contagious respiratory illness caused by influenza viruses. It can cause mild to severe illness."
    elif 'dengue' in query.lower():
        response = "Dengue is a mosquito-borne viral disease that has rapidly spread in tropical and subtropical regions. Symptoms include high fever, headache, vomiting, and pain in muscles and joints."
    elif 'malaria' in query.lower():
        response = "Malaria is a life-threatening disease caused by parasites that are transmitted to people through the bites of infected female Anopheles mosquitoes."
    else:
        response = "I don't have specific information about that. Please ask about COVID-19, influenza, dengue, or malaria."
    
    return jsonify({'response': response})

@bp.route('/api/health-data', methods=['GET'])
def get_health_data():
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    data = HealthData.query.filter(
        HealthData.timestamp >= start_date
    ).order_by(HealthData.timestamp.desc()).all()
    
    return jsonify([item.to_dict() for item in data])

@bp.route('/api/health-data', methods=['POST'])
def add_health_data():
    data = request.get_json()
    
    health_record = HealthData(
        user_id=data.get('user_id', 'default_user'),
        heart_rate=data.get('heart_rate'),
        blood_pressure_systolic=data.get('blood_pressure_systolic'),
        blood_pressure_diastolic=data.get('blood_pressure_diastolic'),
        temperature=data.get('temperature'),
        weight=data.get('weight'),
        steps=data.get('steps'),
        sleep_hours=data.get('sleep_hours')
    )
    
    db.session.add(health_record)
    db.session.commit()
    
    return jsonify(health_record.to_dict()), 201

@bp.route('/api/stats')
def get_stats():
    stats = get_health_stats()
    return jsonify(stats)

@bp.route('/api/generate-sample-data', methods=['POST'])
def generate_sample():
    days = request.json.get('days', 30) if request.json else 30
    generate_sample_data(days)
    return jsonify({'message': f'Generated sample data for {days} days'})