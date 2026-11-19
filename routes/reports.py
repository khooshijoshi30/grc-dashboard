from flask import Blueprint, render_template, make_response
from models.risk import Risk
from models.compliance import ComplianceControl, control_sort_key
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import cm
import io
from datetime import datetime

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
def reports():
    risks = Risk.query.order_by(Risk.risk_score.desc()).all()
    controls = ComplianceControl.query.all()
    total_controls = len(controls)
    implemented = sum(1 for c in controls if c.status == 'Implemented')
    compliance_score = round((implemented / total_controls) * 100, 1) if total_controls > 0 else 0
    return render_template('reports.html', risks=risks, controls=controls,
                           compliance_score=compliance_score, now=datetime.now())

@reports_bp.route('/reports/pdf')
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  textColor=colors.HexColor('#1a3a5c'), fontSize=20)
    story.append(Paragraph("GRC Dashboard Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    risks = Risk.query.all()
    controls = sorted(ComplianceControl.query.all(), key=lambda c: control_sort_key(c.control_id))
    total = len(controls)
    implemented_count = sum(1 for c in controls if c.status == 'Implemented')
    score = round((implemented_count / total) * 100, 1) if total > 0 else 0
    story.append(Paragraph("Executive Summary", styles['Heading1']))
    summary_data = [
        ['Metric', 'Value'],
        ['Total Risks', str(len(risks))],
        ['Open Risks', str(sum(1 for r in risks if r.status == 'Open'))],
        ['Critical Risks', str(sum(1 for r in risks if r.risk_level() == 'Critical'))],
        ['ISO 27001:2022 Compliance Score', f'{score}%'],
        ['Controls Implemented', f'{implemented_count}/{total}'],
    ]
    t = Table(summary_data, colWidths=[8*cm, 8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a5c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Risk Register", styles['Heading1']))
    if risks:
        risk_data = [['Title', 'Category', 'Level', 'Score', 'Status']]
        for r in sorted(risks, key=lambda x: x.risk_score, reverse=True):
            risk_data.append([r.title[:35], r.category[:20], r.risk_level(), str(r.risk_score), r.status])
        rt = Table(risk_data, colWidths=[6*cm, 4*cm, 2.5*cm, 2*cm, 2.5*cm])
        rt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a5c')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 4),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f9f9f9')]),
        ]))
        story.append(rt)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("ISO 27001:2022 Gap Analysis", styles['Heading1']))
    not_impl = [c for c in controls if c.status != 'Implemented']
    if not_impl:
        gap_data = [['Control ID', 'Theme', 'Control Name', 'Status']]
        for c in not_impl:
            gap_data.append([c.control_id, c.domain[:20], c.control_name[:35], c.status])
        gt = Table(gap_data, colWidths=[2*cm, 4*cm, 7*cm, 4*cm])
        gt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a5c')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 4),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fff3cd')]),
        ]))
        story.append(gt)
    doc.build(story)
    buffer.seek(0)
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=GRC_Report_{datetime.now().strftime("%Y%m%d")}.pdf'
    return response
