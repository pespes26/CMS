from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for many-to-many relationship between users and courses
user_courses = db.Table('user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)


class AppUser(db.Model):
    __tablename__ = 'app_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

        # Verify password
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    # These methods and properties are required by Flask-Login
    @property
    def is_active(self):
        # Return True if the user is active, you can modify this if you have an 'active' field
        return True

    @property
    def is_authenticated(self):
        # Return True if the user is authenticated
        return True

    @property
    def is_anonymous(self):
        # Return False, as this is an authenticated user
        return False

    def get_id(self):
        # Return the user ID in a string format (Flask-Login requirement)
        return str(self.id)

    # Relationship to Course
    courses = db.relationship('Course', backref='user', lazy=True)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    coursenumber = db.Column(db.String(50), nullable=False, unique=True)

    # Foreign key to associate courses with users
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)

    # Relationships with cascading delete
    lectures = db.relationship('LectureTime', backref='course', lazy=True, cascade="all, delete-orphan")
    practices = db.relationship('PracticeTime', backref='course', lazy=True, cascade="all, delete-orphan")

class LectureTime(db.Model):
    __tablename__ = 'lecture_time'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    building = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class PracticeTime(db.Model):
    __tablename__ = 'practice_time'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    building = db.Column(db.String(50), nullable=False)
    classroom = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
