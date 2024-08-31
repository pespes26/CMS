from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'course'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courseID = db.Column(db.String(50), nullable=False)
    
    # Relationships
    lecture_times = db.relationship('LectureTime', backref='course', cascade="all, delete-orphan")
    practice_times = db.relationship('PracticeTime', backref='course', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Course {self.name}>'

class LectureTime(db.Model):
    __tablename__ = 'lecture_time'
    
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    building = db.Column(db.String(10), nullable=False)
    classroom = db.Column(db.String(10), nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        return f'<LectureTime {self.day} {self.start_time}-{self.end_time}>'

class PracticeTime(db.Model):
    __tablename__ = 'practice_time'
    
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    building = db.Column(db.String(10), nullable=False)
    classroom = db.Column(db.String(10), nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    def __repr__(self):
        return f'<PracticeTime {self.day} {self.start_time}-{self.end_time}>'
    
class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_pref = db.Column(db.String(50))
    priority_course_1 = db.Column(db.Integer, db.ForeignKey('course.id'))
    priority_course_2 = db.Column(db.Integer, db.ForeignKey('course.id'))
    no_course_day = db.Column(db.String(10))  # Store the day of the week
    no_course_time_start = db.Column(db.Time)
    no_course_time_end = db.Column(db.Time)

