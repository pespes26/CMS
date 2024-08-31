from flask_sqlalchemy import SQLAlchemy
from app import db

db = SQLAlchemy()

from app import db

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courseid = db.Column(db.String(50), nullable=False)

    lectures = db.relationship('LectureTime', backref='course', lazy=True, cascade="all, delete-orphan")
    practices = db.relationship('PracticeTime', backref='course', lazy=True, cascade="all, delete-orphan")

class LectureTime(db.Model):
    __tablename__ = 'lecture_time'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    building = db.Column(db.String(10), nullable=False)
    classroom = db.Column(db.String(10), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class PracticeTime(db.Model):
    __tablename__ = 'practice_time'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    building = db.Column(db.String(10), nullable=False)
    classroom = db.Column(db.String(10), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)


    
class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_pref = db.Column(db.String(50), nullable=False)
    priority_course_1 = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    priority_course_2 = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    no_course_day = db.Column(db.String(50), nullable=True)
    no_course_time_start = db.Column(db.Time, nullable=True)
    no_course_time_end = db.Column(db.Time, nullable=True)

class FinalTimetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=False)
    slot_type = db.Column(db.String(50), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)