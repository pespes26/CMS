from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.urandom(24)  # Generates a random secret key each time the app starts

# Configuration for PostgreSQL Database
# Use the DATABASE_URL environment variable, falling back to localhost for development
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:89562310@localhost:5433/coursesDB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models and routes after initializing db and migrate
from app import routes, models
