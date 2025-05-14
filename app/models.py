from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    heart_rate = db.Column(db.Float)
    blood_pressure = db.Column(db.String(20))
    temperature = db.Column(db.Float)
    oxygen_level = db.Column(db.Float)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<HealthData {self.timestamp}>' 