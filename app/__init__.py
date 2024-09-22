from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# Set the secret key for session management (use a fixed key in production)
app.secret_key = os.urandom(24)  # Change this for production use

# Configuration for PostgreSQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:89562310@localhost:5433/coursesDB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models and routes after initializing db and migrate
from app import routes, models
from app.models import AppUser

# Flask-Login user loader function
@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))

# Set up a login view if needed
login_manager.login_view = 'login'  # Replace 'login' with your actual login route endpoint
