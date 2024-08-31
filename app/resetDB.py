from app import db

# Reflect the existing tables
db.reflect()

# Drop all tables
db.drop_all()
db.create_all()
