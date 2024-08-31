from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # This generates a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:89562310@localhost:5433/coursesDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes, models
