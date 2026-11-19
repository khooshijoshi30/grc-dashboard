<h1 align="center">GRC Dashboard</h1>

<p align="center">
  <b>A web app for managing an information security risk register and tracking ISO/IEC 27001:2022 control compliance</b><br>
  Risk register · ISO 27001:2022 Annex A tracking · Gap analysis by theme · PDF reporting
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0-000000" alt="Flask">
  <img src="https://img.shields.io/badge/Database-SQLite-0f766e" alt="SQLite">
  <img src="https://img.shields.io/badge/Standard-ISO%2027001%3A2022-ca8a04" alt="ISO 27001:2022">
  <img src="https://img.shields.io/badge/Domain-GRC-2650b8" alt="GRC">
</p>

---

## 📌 At a glance

| | |
| --- | --- |
| **What** | A Flask web application that brings risk management and ISO 27001 compliance tracking into one dashboard |
| **Who it's for** | GRC, security and compliance teams that track risks and control status in spreadsheets today |
| **Risk scoring** | Likelihood (1–5) × Impact (1–5) = score out of 25 → Low / Medium / High / Critical |
| **Compliance** | All **93 ISO/IEC 27001:2022 Annex A controls** in 4 themes, each marked Implemented / Partial / Not Implemented with evidence and owner |
| **Reporting** | Live dashboard, domain-wise gap analysis, and a one-click PDF management report |

---

## ✨ Features

**📊 Dashboard**
- Total, open and critical risks at a glance
- Overall ISO 27001 compliance score
- Charts of risks by level and controls by status
- Most recent risks

**⚠️ Risk register**
- Add, edit and delete risks with title, description, category, owner and mitigation
- Automatic risk score (likelihood × impact) and risk level
- 9 risk categories: Information Security, Operational, Compliance, Financial, Reputational, Third-Party / Vendor, Physical Security, Human Resources, Technology
- Filter by status and category; sorted by highest score first

**✅ ISO 27001:2022 control tracking**
- All 93 Annex A controls pre-loaded on first run, grouped into the 4 themes:
  - **A.5 Organizational** (37) · **A.6 People** (8) · **A.7 Physical** (14) · **A.8 Technological** (34)
- The **11 controls new in 2022** are tagged *New* (e.g., A.5.7 Threat intelligence, A.5.23 Cloud services, A.8.12 Data leakage prevention)
- Set status, record evidence and assign a responsible person for each control
- Filter by theme and status

**🔍 Gap analysis**
- Overall compliance score
- Theme-by-theme breakdown with chart (implemented, partial, not implemented, score)
- List of all controls that are not yet implemented

**📄 Reports**
- On-screen report view
- **PDF export** with an executive summary, the full risk register and the ISO 27001:2022 gap list (generated with ReportLab)

---

## 🔄 Version history

| Version | Change |
| --- | --- |
| 2.0 | Upgraded from the retired ISO 27001:2013 control set to **ISO/IEC 27001:2022** (93 controls, 4 themes, *New* tags); fixed a startup crash caused by a circular import; secret key now read from an environment variable |
| 1.0 | Risk register, ISO 27001:2013 control tracking, gap analysis, PDF reports |

---

## 🧮 How the scoring works

**Risk level**

| Score (L × I) | Level |
| --- | --- |
| 1 – 4 | Low |
| 5 – 9 | Medium |
| 10 – 16 | High |
| 17 – 25 | Critical |

**Compliance score**

```
Compliance score = Implemented controls ÷ Total controls × 100
```

Partial controls are tracked and reported separately, but do not count towards the score, so the score reflects only fully implemented controls.

---

## 🛠️ Tech stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Flask (blueprints for dashboard, risks, compliance, reports) |
| Database | SQLite with Flask-SQLAlchemy |
| Frontend | Jinja2 templates, Bootstrap 5, Bootstrap Icons, Chart.js |
| Reports | ReportLab (PDF) |

---

## 🚀 Run it locally

```bash
# 1. Clone the repository
git clone https://github.com/khooshijoshi30/grc-dashboard.git
cd grc-dashboard

# 2. (Optional) create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the app
python app.py
```

Open **http://127.0.0.1:5000** in your browser. The database (`grc.db`) and the 93 ISO 27001:2022 controls are created automatically on first run. A database created by an older version with the 2013 controls is upgraded automatically; existing risks are kept.

> For anything beyond local use, set your own `SECRET_KEY` environment variable and run with `FLASK_DEBUG=0`.

---

## 📂 Project structure

```
grc-dashboard/
├── app.py              ← app factory, config, blueprint registration, seeding
├── extensions.py       ← shared database instance
├── requirements.txt
├── models/
│   ├── risk.py         ← Risk model, risk level logic
│   └── compliance.py   ← ComplianceControl model, ISO 27001:2022 Annex A controls
├── routes/
│   ├── dashboard.py    ← dashboard metrics
│   ├── risks.py        ← risk register (add, edit, delete, filter)
│   ├── compliance.py   ← control tracking and gap analysis
│   └── reports.py      ← report view and PDF export
└── templates/          ← Jinja2 HTML pages
```

---

## 🛠️ Skills demonstrated

- **Risk management:** risk identification, likelihood × impact scoring, risk levels, ownership and mitigation tracking
- **Compliance management:** ISO/IEC 27001:2022 Annex A control tracking (93 controls, 4 themes), evidence recording, gap analysis
- **Reporting:** management-level summaries and PDF reports
- **Development:** Python, Flask, SQLAlchemy ORM, Jinja2, Bootstrap, Chart.js

---

## 🔭 Planned improvements

- Add control mappings for **DPDP Act 2023**, **GDPR** and **SOC 2**
- Risk heat map (likelihood × impact grid)
- User login and role-based access

---

## 🔗 Related projects

- [Personal Data Breach Response Playbook & Tabletop Kit](https://github.com/khooshijoshi30/dpdp-breach-response-playbook)
- [ROPA & DPIA: AI Credit Scoring at an Indian NBFC](https://github.com/khooshijoshi30/dpdp-ropa-dpia-assessment)
- [Vendor Risk Desk: TPRM programme and working risk scoring tool](https://github.com/khooshijoshi30/vendor-risk-desk)

---

## 👩‍💻 About the author

**Khooshi Joshi**
