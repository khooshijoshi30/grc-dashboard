from flask import Blueprint, render_template
from models.risk import Risk
from models.compliance import ComplianceControl

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    risks = Risk.query.all()
    controls = ComplianceControl.query.all()
    total_risks = len(risks)
    open_risks = sum(1 for r in risks if r.status == 'Open')
    critical_risks = sum(1 for r in risks if r.risk_level() == 'Critical')
    total_controls = len(controls)
    implemented = sum(1 for c in controls if c.status == 'Implemented')
    partial = sum(1 for c in controls if c.status == 'Partial')
    not_implemented = sum(1 for c in controls if c.status == 'Not Implemented')
    compliance_score = round((implemented / total_controls) * 100, 1) if total_controls > 0 else 0
    risk_by_category = {}
    for r in risks:
        risk_by_category[r.category] = risk_by_category.get(r.category, 0) + 1
    risk_by_level = {
        'Critical': sum(1 for r in risks if r.risk_level() == 'Critical'),
        'High': sum(1 for r in risks if r.risk_level() == 'High'),
        'Medium': sum(1 for r in risks if r.risk_level() == 'Medium'),
        'Low': sum(1 for r in risks if r.risk_level() == 'Low'),
    }
    recent_risks = Risk.query.order_by(Risk.created_at.desc()).limit(5).all()
    return render_template('dashboard.html',
        total_risks=total_risks, open_risks=open_risks, critical_risks=critical_risks,
        compliance_score=compliance_score, implemented=implemented, partial=partial,
        not_implemented=not_implemented, total_controls=total_controls,
        risk_by_category=risk_by_category, risk_by_level=risk_by_level,
        recent_risks=recent_risks)
