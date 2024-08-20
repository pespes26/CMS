from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Course, LectureTime

@app.route('/')
@app.route('/index')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/add', methods=['POST'])
def add_course():
    try:
        name = request.form.get('name')
        courseID = request.form.get('courseID')
        description = request.form.get('description')
        lecture_days = request.form.getlist('lecture_days[]')
        lecture_times = request.form.getlist('lecture_times[]')
        practice_day = request.form.get('practice_day')
        practice_time = request.form.get('practice_time')

        if name and courseID and lecture_days and lecture_times:
            # Step 1: Create the new course
            new_course = Course(
                name=name,
                courseID=courseID,
                description=description,
                practice_day=practice_day,
                practice_time=practice_time
            )
            db.session.add(new_course)
            db.session.commit()  # Commit the course to generate the ID

            # Step 2: Now that the course ID is available, add lecture times
            for day, time in zip(lecture_days, lecture_times):
                new_lecture_time = LectureTime(day=day, time=time, course_id=new_course.id)
                db.session.add(new_lecture_time)

            db.session.commit()  # Commit the lecture times to the database
        
        return redirect(url_for('index'))

    except Exception as e:
        print(f"An error occurred: {e}")
        return "An internal error occurred", 500

# Route to edit a course using a form (Update)
@app.route('/edit/<int:id>')
def edit_course(id):
    course = Course.query.get(id)
    if course:
        return render_template('edit.html', course=course)
    return redirect(url_for('index'))

# Route to update a course's information (Update)
@app.route('/update/<int:id>', methods=['POST'])
def update_course(id):
    course = Course.query.get(id)
    if course:
        course.name = request.form.get('name')
        course.description = request.form.get('description')
        db.session.commit()
    return redirect(url_for('index'))

# Route to delete a course by its ID (Delete)
@app.route('/delete/<int:id>')
def delete_course(id):
    course = Course.query.get(id)
    if course:
        db.session.delete(course)
        db.session.commit()
    return redirect(url_for('index'))

# Route to get all courses as JSON (Read)
@app.route('/courses/json')
def get_courses_json():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

# Route to add a new course using JSON (Create)
@app.route('/courses/json', methods=['POST'])
def add_course_json():
    data = request.get_json()
    if not data or not 'name' in data or not 'description' in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    new_course = Course(name=data['name'], description=data['description'])
    db.session.add(new_course)
    db.session.commit()

    return jsonify(new_course.to_dict()), 201

# Route to update a course using JSON (Update)
@app.route('/courses/json/<int:id>', methods=['PUT'])
def update_course_json(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    data = request.get_json()
    if not data or not 'name' in data or not 'description' in data:
        return jsonify({'error': 'Invalid input'}), 400

    course.name = data['name']
    course.description = data['description']
    db.session.commit()

    return jsonify(course.to_dict())

# Route to delete a course using JSON (Delete)
@app.route('/courses/json/<int:id>', methods=['DELETE'])
def delete_course_json(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'Course deleted'}), 200
