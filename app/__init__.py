from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = os.urandom(24)  # This generates a random secret key each time the app starts

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:89562310@localhost:5433/coursesDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
