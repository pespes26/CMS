from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Course, LectureTime, PracticeTime , UserPreferences , FinalTimetable
from sqlalchemy.exc import SQLAlchemyError


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form.get('name')
        course_id = request.form.get('courseID')

        new_course = Course(name=course_name, courseid=course_id)
        db.session.add(new_course)
        db.session.commit()

        lecture_days = request.form.getlist('lecture_days[]')
        lecture_start_times = request.form.getlist('lecture_start_time[]')
        lecture_end_times = request.form.getlist('lecture_end_time[]')
        lecture_buildings = request.form.getlist('lecture_building[]')
        lecture_classrooms = request.form.getlist('lecture_classroom[]')

        for day, start_time, end_time, building, classroom in zip(lecture_days, lecture_start_times, lecture_end_times, lecture_buildings, lecture_classrooms):
            formatted_start_time = f"{start_time}:00:00"
            formatted_end_time = f"{end_time}:00:00"
            lecture_building = "Online" if building == '0' else building
            lecture_classroom = "Online" if classroom == '0' else classroom
            
            new_lecture = LectureTime(
                day=day,
                start_time=formatted_start_time,
                end_time=formatted_end_time,
                building=lecture_building,
                classroom=lecture_classroom,
                course_id=new_course.id
            )
            db.session.add(new_lecture)

        # Similarly for practices
        practice_days = request.form.getlist('practice_days[]')
        practice_start_times = request.form.getlist('practice_start_time[]')
        practice_end_times = request.form.getlist('practice_end_time[]')
        practice_buildings = request.form.getlist('practice_building[]')
        practice_classrooms = request.form.getlist('practice_classroom[]')

        for day, start_time, end_time, building, classroom in zip(practice_days, practice_start_times, practice_end_times, practice_buildings, practice_classrooms):
            formatted_start_time = f"{start_time}:00:00"
            formatted_end_time = f"{end_time}:00:00"
            practice_building = "Online" if building == '0' else building
            practice_classroom = "Online" if classroom == '0' else classroom

            new_practice = PracticeTime(
                day=day,
                start_time=formatted_start_time,
                end_time=formatted_end_time,
                building=practice_building,
                classroom=practice_classroom,
                course_id=new_course.id
            )
            db.session.add(new_practice)

        db.session.commit()
        return redirect(url_for('courses'))

    return render_template('addCourse.html')

@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/clist')
def courses():
    all_courses = Course.query.all()
    return render_template('cList.html', courses=all_courses)

@app.route('/ctable')
def timetable():
    return render_template('cTable.html')

@app.route('/edit_course', methods=['GET', 'POST'])
def edit_course():
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        if course_id:
            return redirect(url_for('edit_course_details', course_id=course_id))
        else:
            return redirect(url_for('edit_course'))

    courses = Course.query.all()
    return render_template('editCourse.html', courses=courses)

@app.route('/edit_course_details/<int:course_id>', methods=['GET', 'POST'])
def edit_course_details(course_id):
    # Fetch the course and handle 404 error if not found
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        try:
            edit_choice = request.form.get('edit_choice')
            if edit_choice == 'lecture':
                lecture_id = request.form.get('lecture_id')
                lecture = LectureTime.query.get_or_404(lecture_id)

                lecture.day = request.form.get('day')
                lecture.start_time = f"{request.form.get('start_time')}:00"
                lecture.end_time = f"{request.form.get('end_time')}:00"
                building = request.form.get('building')
                classroom = request.form.get('classroom')
                lecture.building = "Online" if building == '0' else building
                lecture.classroom = "Online" if classroom == '0' else classroom

                db.session.commit()
                flash('Lecture updated successfully!', 'success')

            elif edit_choice == 'practice':
                practice_id = request.form.get('practice_id')
                practice = PracticeTime.query.get_or_404(practice_id)

                practice.day = request.form.get('day')
                practice.start_time = f"{request.form.get('start_time')}:00"
                practice.end_time = f"{request.form.get('end_time')}:00"
                building = request.form.get('building')
                classroom = request.form.get('classroom')
                practice.building = "Online" if building == '0' else building
                practice.classroom = "Online" if classroom == '0' else classroom

                db.session.commit()
                flash('Practice updated successfully!', 'success')

        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
        finally:
            db.session.close()

        return redirect(url_for('edit_course_details', course_id=course.id))

    return render_template('editCourseDetails.html', course=course)


@app.route('/delete_course/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        course = db.session.merge(course)  # Ensure the course is attached to the current session
        db.session.delete(course)
        db.session.commit()
        flash('Course deleted successfully', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error deleting course: {str(e)}', 'danger')
    return redirect(url_for('courses'))


@app.route('/edit_pre', methods=['GET', 'POST'])
def edit_pre():
    if request.method == 'POST':
        # Get form data
        schedule_pref = request.form.get('schedule_pref')
        priority_course_1 = request.form.get('priority_course_1')
        priority_course_2 = request.form.get('priority_course_2')
        no_course_days = request.form.getlist('no_course_day')
        no_course_times_start = request.form.getlist('no_course_time_start')
        no_course_times_end = request.form.getlist('no_course_time_end')

        # Create a new UserPreferences object
        try:
            new_prefs = UserPreferences(
                schedule_pref=schedule_pref,
                priority_course_1=priority_course_1 if priority_course_1 else None,
                priority_course_2=priority_course_2 if priority_course_2 else None
            )
            db.session.add(new_prefs)
            db.session.commit()

            # Now, handle the restricted time entries
            for day, start_time, end_time in zip(no_course_days, no_course_times_start, no_course_times_end):
                restricted_time = RestrictedTime(
                    user_preferences_id=new_prefs.id,
                    day=day,
                    start_time=start_time,
                    end_time=end_time
                )
                db.session.add(restricted_time)

            db.session.commit()
            return redirect(url_for('courses'))

        except Exception as e:
            db.session.rollback()
            return str(e)

    courses = Course.query.all()
    return render_template('editPer.html', courses=courses)

@app.route('/genetable')
def genetable():
    return render_template('geneTable.html')
    



