from app import db

class LectureTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courseID = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    lecture_times = db.relationship('LectureTime', backref='course', lazy=True)
    practice_day = db.Column(db.String(20), nullable=True)
    practice_time = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'courseID': self.courseID,
            'description': self.description,
            'lecture_times': [
                {'day': lt.day, 'time': lt.time} for lt in self.lecture_times
            ],
            'practice_day': self.practice_day,
            'practice_time': self.practice_time
        }

    def __repr__(self):
        return f'<Course {self.name} - {self.courseID}>'
