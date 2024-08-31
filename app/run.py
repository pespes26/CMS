from app import app, db

if __name__ == "__main__":
    db.create_all()  # This will create the tables based on your models
    app.run(debug=True)
