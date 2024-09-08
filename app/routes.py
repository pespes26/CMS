from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Course, LectureTime, PracticeTime
from sqlalchemy.exc import SQLAlchemyError

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        try:
            # Add course details
            course_name = request.form['name']
            coursenumber = request.form['courseID']
            new_course = Course(name=course_name, coursenumber=coursenumber)
            db.session.add(new_course)
            db.session.commit()

            # Add lectures
            lecture_days = request.form.getlist('lecture_days[]')
            lecture_start_times = request.form.getlist('lecture_start_time[]')
            lecture_end_times = request.form.getlist('lecture_end_time[]')
            lecture_buildings = request.form.getlist('lecture_building[]')
            lecture_classrooms = request.form.getlist('lecture_classroom[]')

            for day, start_time, end_time, building, classroom in zip(lecture_days, lecture_start_times, lecture_end_times, lecture_buildings, lecture_classrooms):
                building = "Online" if building == "0" else building
                classroom = "Online" if classroom == "0" else classroom

                new_lecture = LectureTime(
                    day=day,
                    start_time=start_time,
                    end_time=end_time,
                    building=building,
                    classroom=classroom,
                    course_id=new_course.id
                )
                db.session.add(new_lecture)

            # Add practices
            practice_days = request.form.getlist('practice_days[]')
            practice_start_times = request.form.getlist('practice_start_time[]')
            practice_end_times = request.form.getlist('practice_end_time[]')
            practice_buildings = request.form.getlist('practice_building[]')
            practice_classrooms = request.form.getlist('practice_classroom[]')

            for day, start_time, end_time, building, classroom in zip(practice_days, practice_start_times, practice_end_times, practice_buildings, practice_classrooms):
                building = "Online" if building == "0" else building
                classroom = "Online" if classroom == "0" else classroom

                new_practice = PracticeTime(
                    day=day,
                    start_time=start_time,
                    end_time=end_time,
                    building=building,
                    classroom=classroom,
                    course_id=new_course.id
                )
                db.session.add(new_practice)

            db.session.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('courses'))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", 'danger')
            return redirect(url_for('add_course'))

    return render_template('addCourse.html')

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('cList.html', courses=all_courses)

@app.route('/ctable')
def timetable():
    # Query all the courses and their lectures/practices from the database
    courses = Course.query.all()

    schedule = []

    # Loop through courses and gather lectures and practices
    for course in courses:
        # Add lectures to the schedule
        for lecture in course.lectures:
            schedule.append((course, {
                'day': lecture.day,
                'start_time': lecture.start_time,
                'end_time': lecture.end_time,
                'type': 'Lecture'
            }))

        # Add practices to the schedule
        for practice in course.practices:
            schedule.append((course, {
                'day': practice.day,
                'start_time': practice.start_time,
                'end_time': practice.end_time,
                'type': 'Practice'
            }))

    return render_template('cTable.html', schedule=schedule)

@app.route('/edit_course_details/<int:course_id>', methods=['GET', 'POST'])
def edit_course_details(course_id):
    course = Course.query.get_or_404(course_id)

    # Fetch the related lectures and practices
    lectures = LectureTime.query.filter_by(course_id=course_id).all()
    practices = PracticeTime.query.filter_by(course_id=course_id).all()

    if request.method == 'POST':
        edit_choice = request.form.get('edit_choice')

        if edit_choice == 'lecture':
            lecture_id = request.form.get('lecture_id')
            lecture = LectureTime.query.get_or_404(lecture_id)
            lecture.day = request.form.get('day')
            lecture.start_time = request.form.get('start_time')
            lecture.end_time = request.form.get('end_time')
            lecture.building = request.form.get('building')
            lecture.classroom = request.form.get('classroom')
            db.session.commit()
            flash('Lecture updated successfully!', 'success')

        elif edit_choice == 'practice':
            practice_id = request.form.get('practice_id')
            practice = PracticeTime.query.get_or_404(practice_id)
            practice.day = request.form.get('day')
            practice.start_time = request.form.get('start_time')
            practice.end_time = request.form.get('end_time')
            practice.building = request.form.get('building')
            practice.classroom = request.form.get('classroom')
            db.session.commit()
            flash('Practice updated successfully!', 'success')

        return redirect(url_for('courses'))

    return render_template('editCourseDetails.html', course=course, lectures=lectures, practices=practices)

@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('courses'))

@app.route('/course/<int:course_id>/edit_lecture/<int:lecture_id>', methods=['GET', 'POST'])
def edit_lecture(course_id, lecture_id):
    course = Course.query.get_or_404(course_id)
    lecture = LectureTime.query.get_or_404(lecture_id)

    if request.method == 'POST':
        lecture.day = request.form.get('day')
        lecture.start_time = request.form.get('start_time')
        lecture.end_time = request.form.get('end_time')
        lecture.building = request.form.get('building')
        lecture.classroom = request.form.get('classroom')

        db.session.commit()
        flash('Lecture updated successfully', 'success')
        return redirect(url_for('courses'))

    return render_template('editLecture.html', course=course, lecture=lecture)

@app.route('/course/<int:course_id>/edit_practice/<int:practice_id>', methods=['GET', 'POST'])
def edit_practice(course_id, practice_id):
    course = Course.query.get_or_404(course_id)
    practice = PracticeTime.query.get_or_404(practice_id)

    if request.method == 'POST':
        practice.day = request.form.get('day')
        practice.start_time = request.form.get('start_time')
        practice.end_time = request.form.get('end_time')
        practice.building = request.form.get('building')
        practice.classroom = request.form.get('classroom')

        db.session.commit()
        flash('Practice updated successfully', 'success')
        return redirect(url_for('courses'))

    return render_template('editPractice.html', course=course, practice=practice)

@app.route('/edit_pre', methods=['GET', 'POST'])
def edit_pre():
    if request.method == 'POST':
        # Get user preferences and restrictions (if any)
        schedule_pref = request.form.get('schedule_pref')

        # Handle form submission and store preferences (without generating an optimal schedule)
        flash('Preferences saved!', 'success')
        return redirect(url_for('timetable'))

    courses = Course.query.all()
    return render_template('editPer.html', courses=courses)

@app.route('/genetable')
def genetable():
    return render_template('geneTable.html')
