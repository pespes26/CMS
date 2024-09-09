from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Course, LectureTime, PracticeTime
from sqlalchemy.exc import SQLAlchemyError
from datetime import time


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

    # Initialize an empty schedule
    schedule = {
        'Sunday': {hour: [] for hour in range(8, 22)},
        'Monday': {hour: [] for hour in range(8, 22)},
        'Tuesday': {hour: [] for hour in range(8, 22)},
        'Wednesday': {hour: [] for hour in range(8, 22)},
        'Thursday': {hour: [] for hour in range(8, 22)},
        'Friday': {hour: [] for hour in range(8, 22)},
    }

    # Loop through courses and add lectures/practices to the appropriate time slots
    for course in courses:
        # Add lectures to the schedule
        for lecture in course.lectures:
            day = lecture.day
            start_hour = int(lecture.start_time.strftime('%H'))
            end_hour = int(lecture.end_time.strftime('%H'))

            # For each hour of the lecture, append it to the schedule
            for hour in range(start_hour, end_hour):
                schedule[day][hour].append({
                    'course_name': course.name,
                    'type': 'Lecture'
                })

        # Add practices to the schedule
        for practice in course.practices:
            day = practice.day
            start_hour = int(practice.start_time.strftime('%H'))
            end_hour = int(practice.end_time.strftime('%H'))

            # For each hour of the practice, append it to the schedule
            for hour in range(start_hour, end_hour):
                schedule[day][hour].append({
                    'course_name': course.name,
                    'type': 'Practice'
                })

    # Print schedule to debug
    print(schedule)

    # Pass the structured schedule to the template
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
        # Gather preferences from form
        schedule_pref = request.form.get('schedule_pref')
        restricted_days = request.form.getlist('no_course_day[]')
        restricted_times_start = request.form.getlist('no_course_time_start[]')
        restricted_times_end = request.form.getlist('no_course_time_end[]')

        # Gather restricted time slots
        restricted_times = []
        for day, start, end in zip(restricted_days, restricted_times_start, restricted_times_end):
            restricted_times.append({
                'day': day,
                'start_time': start,
                'end_time': end
            })

        # Get the courses (replace this with real queries)
        courses = Course.query.all()

        # Build and optimize the schedule
        optimal_schedule, scheduling_errors = generate_optimal_schedule(courses, schedule_pref, restricted_times)

        # Render the timetable with the optimized schedule and errors
        return render_template('cTable.html', schedule=optimal_schedule, errors=scheduling_errors)

    # If the request method is GET, render the form
    courses = Course.query.all()
    return render_template('editPer.html', courses=courses)



def generate_optimal_schedule(courses, schedule_pref, restricted_times):
    # Initialize empty timetable (dict) for days and hours (e.g., 8-22 for each day)
    timetable = {
        'Sunday': {hour: None for hour in range(8, 22)},
        'Monday': {hour: None for hour in range(8, 22)},
        'Tuesday': {hour: None for hour in range(8, 22)},
        'Wednesday': {hour: None for hour in range(8, 22)},
        'Thursday': {hour: None for hour in range(8, 22)},
        'Friday': {hour: None for hour in range(8, 22)},
    }

    sorted_courses = sorted(courses, key=lambda c: len(c.lectures))
    scheduling_errors = []

    def is_time_available(day, start_time, end_time):
        for hour in range(start_time, end_time):
            if timetable[day][hour] is not None:
                return False
        return True

    def check_for_conflicts(day, start_time, end_time):
        for hour in range(start_time, end_time):
            if timetable[day][hour] is not None:
                return timetable[day][hour]  # Return the conflicting course
        return None

    def apply_restricted_times():
        for restriction in restricted_times:
            day = restriction['day']
            start_time = int(restriction['start_time'].split(':')[0])
            end_time = int(restriction['end_time'].split(':')[0])
            for hour in range(start_time, end_time):
                timetable[day][hour] = 'Unavailable'

    # Apply restricted times to the timetable
    apply_restricted_times()

    # Schedule courses into the timetable
    for course in sorted_courses:
        lecture_scheduled = False
        practice_scheduled = False

        # Try to schedule lectures
        for lecture in course.lectures:
            if lecture_scheduled:
                break  # If already scheduled, skip
            day = lecture.day
            start_time = int(lecture.start_time.strftime('%H'))
            end_time = int(lecture.end_time.strftime('%H'))
            conflicting_course = check_for_conflicts(day, start_time, end_time)

            if conflicting_course is None and is_time_available(day, start_time, end_time):
                for hour in range(start_time, end_time):
                    timetable[day][hour] = {
                        'course_name': course.name,
                        'type': 'Lecture'
                    }
                lecture_scheduled = True
            else:
                # Capture the specific reason for the scheduling failure
                if conflicting_course == 'Unavailable':
                    scheduling_errors.append(f"Lecture for {course.name} could not be scheduled due to time restrictions on {day} from {lecture.start_time} to {lecture.end_time}.")
                elif conflicting_course:
                    scheduling_errors.append(f"Lecture for {course.name} conflicts with {conflicting_course['course_name']} on {day} from {lecture.start_time} to {lecture.end_time}.")
                lecture_scheduled = True  # Mark it handled

        # Try to schedule practices
        for practice in course.practices:
            if practice_scheduled:
                break  # If already scheduled, skip
            day = practice.day
            start_time = int(practice.start_time.strftime('%H'))
            end_time = int(practice.end_time.strftime('%H'))
            conflicting_course = check_for_conflicts(day, start_time, end_time)

            if conflicting_course is None and is_time_available(day, start_time, end_time):
                for hour in range(start_time, end_time):
                    timetable[day][hour] = {
                        'course_name': course.name,
                        'type': 'Practice'
                    }
                practice_scheduled = True
            else:
                # Capture the specific reason for the scheduling failure
                if conflicting_course == 'Unavailable':
                    scheduling_errors.append(f"Practice for {course.name} could not be scheduled due to time restrictions on {day} from {practice.start_time} to {practice.end_time}.")
                elif conflicting_course:
                    scheduling_errors.append(f"Practice for {course.name} conflicts with {conflicting_course['course_name']} on {day} from {practice.start_time} to {practice.end_time}.")
                practice_scheduled = True  # Mark it handled

    return timetable, scheduling_errors


def spread_courses_across_days(timetable, schedule):
    """
    Spread the courses across as many days as possible.
    """
    for course, slot in schedule:
        day = slot['day']
        start_time = slot['start_time'].hour
        end_time = slot['end_time'].hour
        # Try to distribute evenly across all days
        for target_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            if day == target_day and is_time_available(timetable, target_day, start_time, end_time):
                for hour in range(start_time, end_time):
                    timetable[target_day][hour] = f"{course.name} ({slot['type']})"
                break
    return timetable



def pack_courses_into_fewer_days(timetable, schedule):
    """
    Pack courses into fewer days but avoid entirely empty days.
    """
    packed_days = ['Thursday', 'Friday']  # Try to pack classes into the end of the week
    other_days = ['Monday', 'Tuesday', 'Wednesday']  # Reserve these days for overflow if needed

    for course, slot in schedule:
        day = slot['day']
        start_time = slot['start_time'].hour
        end_time = slot['end_time'].hour
        # Try to pack the courses into the packed days
        for target_day in packed_days:
            if is_time_available(timetable, target_day, start_time, end_time):
                for hour in range(start_time, end_time):
                    timetable[target_day][hour] = f"{course.name} ({slot['type']})"
                break
        else:
            # If no space in packed days, place the class in the remaining days
            for target_day in other_days:
                if is_time_available(timetable, target_day, start_time, end_time):
                    for hour in range(start_time, end_time):
                        timetable[target_day][hour] = f"{course.name} ({slot['type']})"
                    break
    return timetable



# Route for generating the timetable
@app.route('/genetable', methods=['GET', 'POST'])
def genetable():
    if request.method == 'POST':
        # Gather preferences from the form
        schedule_pref = request.form.get('schedule_pref')
        restricted_days = request.form.getlist('no_course_day[]')
        restricted_times_start = request.form.getlist('no_course_time_start[]')
        restricted_times_end = request.form.getlist('no_course_time_end[]')

        restricted_times = []
        for day, start, end in zip(restricted_days, restricted_times_start, restricted_times_end):
            restricted_times.append({
                'day': day,
                'start_time': start,
                'end_time': end
            })

        # Get all courses
        courses = Course.query.all()

        # Generate the optimal schedule
        optimal_schedule = generate_optimal_schedule(courses, schedule_pref, restricted_times)

        # Render the timetable with the generated schedule
        return render_template('geneTable.html', schedule=optimal_schedule)

    return render_template('geneTable.html')
