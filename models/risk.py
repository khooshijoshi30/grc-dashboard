from extensions import db
from datetime import datetime

class Risk(db.Model):
    __tablename__ = 'risks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False)
    likelihood = db.Column(db.Integer, nullable=False)
    impact = db.Column(db.Integer, nullable=False)
    risk_score = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Open')
    owner = db.Column(db.String(100), nullable=True)
    mitigation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def risk_level(self):
        if self.risk_score <= 4:
            return 'Low'
        elif self.risk_score <= 9:
            return 'Medium'
        elif self.risk_score <= 16:
            return 'High'
        else:
            return 'Critical'

    def risk_color(self):
        level = self.risk_level()
        colors = {'Low': 'success', 'Medium': 'warning', 'High': 'danger', 'Critical': 'dark'}
        return colors.get(level, 'secondary')
