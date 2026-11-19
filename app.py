from flask import Flask
import os
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grc.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes.dashboard import dashboard_bp
    from routes.risks import risks_bp
    from routes.compliance import compliance_bp
    from routes.reports import reports_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(risks_bp)
    app.register_blueprint(compliance_bp)
    app.register_blueprint(reports_bp)

    with app.app_context():
        db.create_all()
        from models.compliance import seed_iso27001_controls
        seed_iso27001_controls()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.environ.get('FLASK_DEBUG', '1') == '1')
