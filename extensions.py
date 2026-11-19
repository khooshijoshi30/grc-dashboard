from flask_sqlalchemy import SQLAlchemy

# Single shared database instance, imported by app.py, models and routes.
# Keeping it here (not in app.py) avoids a circular import that creates two
# SQLAlchemy instances when the app is started with `python app.py`.
db = SQLAlchemy()
