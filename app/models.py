from app import db

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    coursenumber = db.Column(db.String(50), nullable=False, unique=True)

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
