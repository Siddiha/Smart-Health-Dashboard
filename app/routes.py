from flask import Blueprint, render_template, jsonify
from app.models import HealthData, db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/health-data')
def get_health_data():
    data = HealthData.query.order_by(HealthData.timestamp.desc()).limit(10).all()
    return jsonify([{
        'id': d.id,
        'timestamp': d.timestamp.isoformat(),
        'heart_rate': d.heart_rate,
        'blood_pressure': d.blood_pressure,
        'temperature': d.temperature,
        'oxygen_level': d.oxygen_level,
        'notes': d.notes
    } for d in data]) 