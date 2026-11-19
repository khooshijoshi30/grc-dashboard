from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.compliance import ComplianceControl, control_sort_key
from extensions import db

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/compliance')
def list_controls():
    domain_filter = request.args.get('domain', '')
    status_filter = request.args.get('status', '')
    query = ComplianceControl.query
    if domain_filter:
        query = query.filter_by(domain=domain_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)
    controls = sorted(query.all(), key=lambda c: control_sort_key(c.control_id))
    all_controls = sorted(ComplianceControl.query.all(), key=lambda c: control_sort_key(c.control_id))
    domains = list(dict.fromkeys(c.domain for c in all_controls))
    return render_template('compliance.html', controls=controls, domains=domains,
                           domain_filter=domain_filter, status_filter=status_filter)

@compliance_bp.route('/compliance/update/<int:id>', methods=['POST'])
def update_control(id):
    control = ComplianceControl.query.get_or_404(id)
    control.status = request.form.get('status', control.status)
    control.evidence = request.form.get('evidence', control.evidence)
    control.responsible = request.form.get('responsible', control.responsible)
    db.session.commit()
    flash(f'Control {control.control_id} updated!', 'success')
    return redirect(url_for('compliance.list_controls'))

@compliance_bp.route('/gap-analysis')
def gap_analysis():
    controls = sorted(ComplianceControl.query.all(), key=lambda c: control_sort_key(c.control_id))
    total = len(controls)
    implemented = [c for c in controls if c.status == 'Implemented']
    partial = [c for c in controls if c.status == 'Partial']
    not_impl = [c for c in controls if c.status == 'Not Implemented']
    score = round(len(implemented) / total * 100, 1) if total > 0 else 0
    domain_stats = {}
    for c in controls:
        if c.domain not in domain_stats:
            domain_stats[c.domain] = {'total': 0, 'implemented': 0, 'partial': 0, 'not_implemented': 0}
        domain_stats[c.domain]['total'] += 1
        if c.status == 'Implemented':
            domain_stats[c.domain]['implemented'] += 1
        elif c.status == 'Partial':
            domain_stats[c.domain]['partial'] += 1
        else:
            domain_stats[c.domain]['not_implemented'] += 1
    new_controls = [c for c in controls if c.is_new_in_2022()]
    return render_template('gap_analysis.html',
        controls=controls, total=total, implemented=implemented,
        partial=partial, not_impl=not_impl, score=score, domain_stats=domain_stats,
        new_controls=new_controls)
