import re
from datetime import datetime

from extensions import db


class ComplianceControl(db.Model):
    __tablename__ = 'compliance_controls'
    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(db.String(20), nullable=False)
    domain = db.Column(db.String(100), nullable=False)  # ISO 27001:2022 theme
    control_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Not Implemented')
    evidence = db.Column(db.Text, nullable=True)
    responsible = db.Column(db.String(100), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def status_color(self):
        colors = {'Implemented': 'success', 'Partial': 'warning', 'Not Implemented': 'danger'}
        return colors.get(self.status, 'secondary')

    def status_badge(self):
        badges = {'Implemented': 'Implemented', 'Partial': 'Partial', 'Not Implemented': 'Not Implemented'}
        return badges.get(self.status, '?')

    def is_new_in_2022(self):
        return self.control_id in NEW_IN_2022


def control_sort_key(control_id):
    """Sort 'A.5.2' before 'A.5.10' (natural order instead of text order)."""
    return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', control_id)]


ORGANIZATIONAL = 'Organizational controls'
PEOPLE = 'People controls'
PHYSICAL = 'Physical controls'
TECHNOLOGICAL = 'Technological controls'

# The 11 controls introduced in ISO/IEC 27001:2022 Annex A
NEW_IN_2022 = {
    'A.5.7', 'A.5.23', 'A.5.30', 'A.7.4', 'A.8.9', 'A.8.10',
    'A.8.11', 'A.8.12', 'A.8.16', 'A.8.23', 'A.8.28',
}

# ISO/IEC 27001:2022 Annex A: 93 controls in 4 themes.
# Control titles follow the standard; the one-line purposes are written in plain language.
ISO27001_2022_CONTROLS = [
    # A.5 Organizational controls (37)
    ('A.5.1', ORGANIZATIONAL, 'Policies for information security', 'Approved, published and regularly reviewed information security policies.'),
    ('A.5.2', ORGANIZATIONAL, 'Information security roles and responsibilities', 'Security roles and responsibilities are defined and assigned.'),
    ('A.5.3', ORGANIZATIONAL, 'Segregation of duties', 'Conflicting duties and areas of responsibility are separated.'),
    ('A.5.4', ORGANIZATIONAL, 'Management responsibilities', 'Management requires staff to apply security according to policy.'),
    ('A.5.5', ORGANIZATIONAL, 'Contact with authorities', 'Contact with relevant authorities is established and maintained.'),
    ('A.5.6', ORGANIZATIONAL, 'Contact with special interest groups', 'Contact with security forums and professional associations is maintained.'),
    ('A.5.7', ORGANIZATIONAL, 'Threat intelligence', 'Information about threats is collected and analysed to produce threat intelligence.'),
    ('A.5.8', ORGANIZATIONAL, 'Information security in project management', 'Security is built into project management.'),
    ('A.5.9', ORGANIZATIONAL, 'Inventory of information and other associated assets', 'An inventory of information and assets, with owners, is kept.'),
    ('A.5.10', ORGANIZATIONAL, 'Acceptable use of information and other associated assets', 'Rules for acceptable use and handling of assets are defined and applied.'),
    ('A.5.11', ORGANIZATIONAL, 'Return of assets', 'Assets are returned when employment or contracts end.'),
    ('A.5.12', ORGANIZATIONAL, 'Classification of information', 'Information is classified by confidentiality, integrity, availability and legal needs.'),
    ('A.5.13', ORGANIZATIONAL, 'Labelling of information', 'Procedures for labelling information follow the classification scheme.'),
    ('A.5.14', ORGANIZATIONAL, 'Information transfer', 'Rules and agreements protect information transferred inside and outside the organization.'),
    ('A.5.15', ORGANIZATIONAL, 'Access control', 'Rules for physical and logical access are set by business and security needs.'),
    ('A.5.16', ORGANIZATIONAL, 'Identity management', 'The full lifecycle of identities is managed.'),
    ('A.5.17', ORGANIZATIONAL, 'Authentication information', 'Allocation and management of authentication information is controlled.'),
    ('A.5.18', ORGANIZATIONAL, 'Access rights', 'Access rights are provisioned, reviewed, changed and removed by policy.'),
    ('A.5.19', ORGANIZATIONAL, 'Information security in supplier relationships', 'Risks from suppliers\' products and services are managed.'),
    ('A.5.20', ORGANIZATIONAL, 'Addressing information security within supplier agreements', 'Security requirements are agreed with each supplier.'),
    ('A.5.21', ORGANIZATIONAL, 'Managing information security in the ICT supply chain', 'Risks in the ICT product and service supply chain are managed.'),
    ('A.5.22', ORGANIZATIONAL, 'Monitoring, review and change management of supplier services', 'Supplier security and service delivery are monitored and reviewed.'),
    ('A.5.23', ORGANIZATIONAL, 'Information security for use of cloud services', 'Acquiring, using, managing and exiting cloud services follows security requirements.'),
    ('A.5.24', ORGANIZATIONAL, 'Information security incident management planning and preparation', 'Incident management processes, roles and responsibilities are planned.'),
    ('A.5.25', ORGANIZATIONAL, 'Assessment and decision on information security events', 'Security events are assessed and classified as incidents where needed.'),
    ('A.5.26', ORGANIZATIONAL, 'Response to information security incidents', 'Incidents are responded to under documented procedures.'),
    ('A.5.27', ORGANIZATIONAL, 'Learning from information security incidents', 'Lessons from incidents are used to strengthen controls.'),
    ('A.5.28', ORGANIZATIONAL, 'Collection of evidence', 'Evidence related to security events is identified, collected and preserved.'),
    ('A.5.29', ORGANIZATIONAL, 'Information security during disruption', 'Security is maintained at the right level during disruption.'),
    ('A.5.30', ORGANIZATIONAL, 'ICT readiness for business continuity', 'ICT readiness is planned, implemented and tested for continuity.'),
    ('A.5.31', ORGANIZATIONAL, 'Legal, statutory, regulatory and contractual requirements', 'Relevant legal, regulatory and contractual requirements are identified and met.'),
    ('A.5.32', ORGANIZATIONAL, 'Intellectual property rights', 'Procedures protect intellectual property rights.'),
    ('A.5.33', ORGANIZATIONAL, 'Protection of records', 'Records are protected from loss, destruction, falsification and unauthorized access.'),
    ('A.5.34', ORGANIZATIONAL, 'Privacy and protection of PII', 'Privacy and personal data are protected as required by law and contract.'),
    ('A.5.35', ORGANIZATIONAL, 'Independent review of information security', 'The approach to security is independently reviewed at planned intervals.'),
    ('A.5.36', ORGANIZATIONAL, 'Compliance with policies, rules and standards for information security', 'Compliance with security policies and standards is regularly reviewed.'),
    ('A.5.37', ORGANIZATIONAL, 'Documented operating procedures', 'Operating procedures for information processing are documented and available.'),

    # A.6 People controls (8)
    ('A.6.1', PEOPLE, 'Screening', 'Background checks are carried out on candidates before joining.'),
    ('A.6.2', PEOPLE, 'Terms and conditions of employment', 'Employment contracts state security responsibilities.'),
    ('A.6.3', PEOPLE, 'Information security awareness, education and training', 'Staff receive security awareness and training relevant to their role.'),
    ('A.6.4', PEOPLE, 'Disciplinary process', 'A disciplinary process exists for security policy violations.'),
    ('A.6.5', PEOPLE, 'Responsibilities after termination or change of employment', 'Security duties that continue after leaving or changing role are enforced.'),
    ('A.6.6', PEOPLE, 'Confidentiality or non-disclosure agreements', 'Confidentiality agreements are in place and reviewed.'),
    ('A.6.7', PEOPLE, 'Remote working', 'Security measures protect information when staff work remotely.'),
    ('A.6.8', PEOPLE, 'Information security event reporting', 'Staff can report security events quickly through set channels.'),

    # A.7 Physical controls (14)
    ('A.7.1', PHYSICAL, 'Physical security perimeters', 'Perimeters protect areas holding information and assets.'),
    ('A.7.2', PHYSICAL, 'Physical entry', 'Secure areas are protected by entry controls.'),
    ('A.7.3', PHYSICAL, 'Securing offices, rooms and facilities', 'Physical security is designed for offices, rooms and facilities.'),
    ('A.7.4', PHYSICAL, 'Physical security monitoring', 'Premises are monitored for unauthorized physical access.'),
    ('A.7.5', PHYSICAL, 'Protecting against physical and environmental threats', 'Protection against natural disasters and other physical threats is in place.'),
    ('A.7.6', PHYSICAL, 'Working in secure areas', 'Rules for working in secure areas are defined.'),
    ('A.7.7', PHYSICAL, 'Clear desk and clear screen', 'Clear desk and clear screen rules are enforced.'),
    ('A.7.8', PHYSICAL, 'Equipment siting and protection', 'Equipment is placed and protected securely.'),
    ('A.7.9', PHYSICAL, 'Security of assets off-premises', 'Assets used off-site are protected.'),
    ('A.7.10', PHYSICAL, 'Storage media', 'Storage media is managed through its lifecycle.'),
    ('A.7.11', PHYSICAL, 'Supporting utilities', 'Facilities are protected from power and utility failures.'),
    ('A.7.12', PHYSICAL, 'Cabling security', 'Power and data cables are protected from interception and damage.'),
    ('A.7.13', PHYSICAL, 'Equipment maintenance', 'Equipment is maintained correctly.'),
    ('A.7.14', PHYSICAL, 'Secure disposal or re-use of equipment', 'Data is removed before equipment is disposed of or reused.'),

    # A.8 Technological controls (34)
    ('A.8.1', TECHNOLOGICAL, 'User endpoint devices', 'Information on user devices is protected.'),
    ('A.8.2', TECHNOLOGICAL, 'Privileged access rights', 'Privileged access is restricted and managed.'),
    ('A.8.3', TECHNOLOGICAL, 'Information access restriction', 'Access to information is restricted according to the access control policy.'),
    ('A.8.4', TECHNOLOGICAL, 'Access to source code', 'Access to source code and development tools is managed.'),
    ('A.8.5', TECHNOLOGICAL, 'Secure authentication', 'Secure authentication methods are implemented.'),
    ('A.8.6', TECHNOLOGICAL, 'Capacity management', 'Resource use is monitored and adjusted to meet capacity needs.'),
    ('A.8.7', TECHNOLOGICAL, 'Protection against malware', 'Protection against malware is in place, with user awareness.'),
    ('A.8.8', TECHNOLOGICAL, 'Management of technical vulnerabilities', 'Vulnerabilities are identified, assessed and fixed.'),
    ('A.8.9', TECHNOLOGICAL, 'Configuration management', 'Security configurations of systems are set, documented and monitored.'),
    ('A.8.10', TECHNOLOGICAL, 'Information deletion', 'Information is deleted when no longer required.'),
    ('A.8.11', TECHNOLOGICAL, 'Data masking', 'Data masking is used in line with policy and legal needs.'),
    ('A.8.12', TECHNOLOGICAL, 'Data leakage prevention', 'Measures to prevent data leakage are applied to systems and networks.'),
    ('A.8.13', TECHNOLOGICAL, 'Information backup', 'Backups are taken and tested according to the backup policy.'),
    ('A.8.14', TECHNOLOGICAL, 'Redundancy of information processing facilities', 'Enough redundancy exists to meet availability needs.'),
    ('A.8.15', TECHNOLOGICAL, 'Logging', 'Logs of activities, exceptions and events are produced, stored and protected.'),
    ('A.8.16', TECHNOLOGICAL, 'Monitoring activities', 'Networks, systems and applications are monitored for anomalous behaviour.'),
    ('A.8.17', TECHNOLOGICAL, 'Clock synchronization', 'System clocks are synchronized to approved time sources.'),
    ('A.8.18', TECHNOLOGICAL, 'Use of privileged utility programs', 'Utility programs that can override controls are restricted.'),
    ('A.8.19', TECHNOLOGICAL, 'Installation of software on operational systems', 'Software installation on operational systems is controlled.'),
    ('A.8.20', TECHNOLOGICAL, 'Networks security', 'Networks and network devices are secured and managed.'),
    ('A.8.21', TECHNOLOGICAL, 'Security of network services', 'Security requirements for network services are defined and monitored.'),
    ('A.8.22', TECHNOLOGICAL, 'Segregation of networks', 'Groups of services, users and systems are segregated on networks.'),
    ('A.8.23', TECHNOLOGICAL, 'Web filtering', 'Access to external websites is managed to reduce exposure to malicious content.'),
    ('A.8.24', TECHNOLOGICAL, 'Use of cryptography', 'Rules for cryptography and key management are defined and applied.'),
    ('A.8.25', TECHNOLOGICAL, 'Secure development life cycle', 'Rules for secure development of software and systems are applied.'),
    ('A.8.26', TECHNOLOGICAL, 'Application security requirements', 'Security requirements are identified when developing or acquiring applications.'),
    ('A.8.27', TECHNOLOGICAL, 'Secure system architecture and engineering principles', 'Secure engineering principles are documented and applied.'),
    ('A.8.28', TECHNOLOGICAL, 'Secure coding', 'Secure coding principles are applied in software development.'),
    ('A.8.29', TECHNOLOGICAL, 'Security testing in development and acceptance', 'Security testing is defined and carried out in the development lifecycle.'),
    ('A.8.30', TECHNOLOGICAL, 'Outsourced development', 'Outsourced development is directed, monitored and reviewed.'),
    ('A.8.31', TECHNOLOGICAL, 'Separation of development, test and production environments', 'Development, test and production environments are kept separate.'),
    ('A.8.32', TECHNOLOGICAL, 'Change management', 'Changes to systems and facilities follow change management procedures.'),
    ('A.8.33', TECHNOLOGICAL, 'Test information', 'Test data is selected, protected and managed appropriately.'),
    ('A.8.34', TECHNOLOGICAL, 'Protection of information systems during audit testing', 'Audit tests on operational systems are planned and agreed to limit impact.'),
]


def _has_old_2013_controls():
    """True if the database still holds the retired ISO 27001:2013 control set (A.9 to A.18)."""
    for (cid,) in db.session.query(ComplianceControl.control_id).all():
        parts = cid.split('.')
        if len(parts) >= 2 and parts[1].isdigit() and int(parts[1]) > 8:
            return True
    return False


def seed_iso27001_controls():
    """Load the ISO/IEC 27001:2022 Annex A controls.

    Seeds an empty database, and replaces the old 2013 control set if an older
    version of this app created the database.
    """
    if ComplianceControl.query.count() > 0 and _has_old_2013_controls():
        ComplianceControl.query.delete()
        db.session.commit()

    if ComplianceControl.query.count() == 0:
        for ctrl in ISO27001_2022_CONTROLS:
            db.session.add(ComplianceControl(
                control_id=ctrl[0], domain=ctrl[1],
                control_name=ctrl[2], description=ctrl[3]
            ))
        db.session.commit()
