from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.risk import Risk
from extensions import db

risks_bp = Blueprint('risks', __name__)

RISK_CATEGORIES = [
    'Information Security', 'Operational', 'Compliance', 'Financial',
    'Reputational', 'Third-Party / Vendor', 'Physical Security', 'Human Resources', 'Technology'
]

@risks_bp.route('/risks')
def list_risks():
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')
    query = Risk.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if category_filter:
        query = query.filter_by(category=category_filter)
    risks = query.order_by(Risk.risk_score.desc()).all()
    return render_template('risks.html', risks=risks, categories=RISK_CATEGORIES,
                           status_filter=status_filter, category_filter=category_filter)

@risks_bp.route('/risks/add', methods=['GET', 'POST'])
def add_risk():
    if request.method == 'POST':
        likelihood = int(request.form['likelihood'])
        impact = int(request.form['impact'])
        risk = Risk(
            title=request.form['title'],
            description=request.form.get('description', ''),
            category=request.form['category'],
            likelihood=likelihood, impact=impact,
            risk_score=likelihood * impact,
            status=request.form.get('status', 'Open'),
            owner=request.form.get('owner', ''),
            mitigation=request.form.get('mitigation', '')
        )
        db.session.add(risk)
        db.session.commit()
        flash('Risk added successfully!', 'success')
        return redirect(url_for('risks.list_risks'))
    return render_template('risk_form.html', risk=None, categories=RISK_CATEGORIES, action='Add')

@risks_bp.route('/risks/edit/<int:id>', methods=['GET', 'POST'])
def edit_risk(id):
    risk = Risk.query.get_or_404(id)
    if request.method == 'POST':
        risk.title = request.form['title']
        risk.description = request.form.get('description', '')
        risk.category = request.form['category']
        risk.likelihood = int(request.form['likelihood'])
        risk.impact = int(request.form['impact'])
        risk.risk_score = risk.likelihood * risk.impact
        risk.status = request.form.get('status', 'Open')
        risk.owner = request.form.get('owner', '')
        risk.mitigation = request.form.get('mitigation', '')
        db.session.commit()
        flash('Risk updated successfully!', 'success')
        return redirect(url_for('risks.list_risks'))
    return render_template('risk_form.html', risk=risk, categories=RISK_CATEGORIES, action='Edit')

@risks_bp.route('/risks/delete/<int:id>', methods=['POST'])
def delete_risk(id):
    risk = Risk.query.get_or_404(id)
    db.session.delete(risk)
    db.session.commit()
    flash('Risk deleted.', 'info')
    return redirect(url_for('risks.list_risks'))
