from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Course, LectureTime, PracticeTime , AppUser
from flask_login import login_required, current_user , login_user ,logout_user
from sqlalchemy.exc import SQLAlchemyError
from datetime import time,datetime
import json
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash , check_password_hash


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/user')
@login_required  # This decorator ensures that only logged-in users can access the profile
def user():
    # Render a user profile page, passing the current user information
    return render_template('user.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AppUser.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = AppUser.query.filter_by(username=username).first()

        if existing_user:
            flash('Username is already taken.', 'danger')
            return redirect(url_for('register'))

        new_user = AppUser(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/add_course', methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in
def add_course():
    if request.method == 'POST':
        try:
            # Debug: Verify if current_user is set correctly
            print(f"Current user: {current_user}")  # Check if current_user is available
            print(f"Current User ID: {current_user.id}")  # Check the ID value
            
            # Check if current_user.id is None
            if current_user.id is None:
                flash("User ID is not available. Please ensure you are logged in.", 'danger')
                return redirect(url_for('add_course'))

            # Add course details and link to current user
            course_name = request.form['name']
            coursenumber = request.form['courseID']
            new_course = Course(
                name=course_name,
                coursenumber=coursenumber,
                user_id=current_user.id  # Link course to the current user
            )
            db.session.add(new_course)
            db.session.commit()

            # Add lectures
            lecture_days = request.form.getlist('lecture_days[]')
            lecture_start_times = request.form.getlist('lecture_start_time[]')
            lecture_end_times = request.form.getlist('lecture_end_time[]')
            lecture_buildings = request.form.getlist('lecture_building[]')
            lecture_classrooms = request.form.getlist('lecture_classroom[]')

            for day, start_time, end_time, building, classroom in zip(
                lecture_days, lecture_start_times, lecture_end_times, lecture_buildings, lecture_classrooms):
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

            for day, start_time, end_time, building, classroom in zip(
                practice_days, practice_start_times, practice_end_times, practice_buildings, practice_classrooms):
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
            return redirect(url_for('courses'))

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy Error: {str(e)}")  # Additional debug statement
            flash(f"An error occurred while adding the course: {str(e)}", 'danger')
            return redirect(url_for('add_course'))

    return render_template('addCourse.html')


@app.route('/')
@login_required
def index():
    return render_template('landing.html')

@app.route('/courses')
@login_required
def courses():
    # Fetch only the courses that belong to the current logged-in user
    user_courses = Course.query.filter_by(user_id=current_user.id).all()
    
    # Example initialization of schedule with default values to avoid missing keys
    schedule = {day: {hour: None for hour in range(8, 22)} for day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
    
    # Populate `schedule` as needed
    # Add logic here to populate `schedule` with actual data related to the user's courses

    return render_template('cList.html', courses=user_courses, schedule=schedule)

@app.route('/ctable')
@login_required
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
@login_required
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
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('courses'))

@app.route('/course/<int:course_id>/edit_lecture/<int:lecture_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
    """
    Generate the optimal schedule based on course list, user preferences, and time restrictions.
    """
    # Initialize the timetable (08:00 to 22:00 each day)
    timetable = {
        'Sunday': {hour: None for hour in range(8, 22)},
        'Monday': {hour: None for hour in range(8, 22)},
        'Tuesday': {hour: None for hour in range(8, 22)},
        'Wednesday': {hour: None for hour in range(8, 22)},
        'Thursday': {hour: None for hour in range(8, 22)},
        'Friday': {hour: None for hour in range(8, 22)},
    }

    scheduling_errors = []  # Track errors related to course scheduling

    def check_for_conflicts(day, start_time, end_time):
        """Check for any scheduling conflicts in the given time range."""
        for hour in range(start_time, end_time):
            if timetable[day][hour] is not None:
                return timetable[day][hour]  # Could return a string 'Unavailable' or course details
        return None

    def apply_restricted_times():
        """Apply restricted times to the timetable based on user preferences."""
        for restriction in restricted_times:
            day = restriction['day']
            start_time = datetime.strptime(restriction['start_time'], '%H:%M').hour
            end_time = datetime.strptime(restriction['end_time'], '%H:%M').hour
            for hour in range(start_time, end_time):
                timetable[day][hour] = 'Unavailable'
            print(f"Applied time restriction on {day} from {start_time}:00 to {end_time}:00")

    # Apply time restrictions
    apply_restricted_times()

    # Scheduling courses: handle lectures and practices
    for course in courses:
        lecture_scheduled = False
        practice_scheduled = False
        lecture_conflict_reasons = []
        practice_conflict_reasons = []

        # Try to schedule lectures
        for lecture in course.lectures:
            day = lecture.day
            start_time = lecture.start_time.hour
            end_time = lecture.end_time.hour

            print(f"Attempting to schedule {course.name} lecture on {day} from {start_time}:00 to {end_time}:00")

            # Check for conflicts
            conflicting_course = check_for_conflicts(day, start_time, end_time)
            if conflicting_course is None:
                # Schedule the lecture
                for hour in range(start_time, end_time):
                    timetable[day][hour] = {'course_name': course.name, 'type': 'Lecture'}
                print(f"Scheduled {course.name} lecture on {day} from {start_time}:00 to {end_time}:00")
                lecture_scheduled = True
                break
            else:
                conflict_reason = f"conflicts with {conflicting_course['course_name']}" if conflicting_course != 'Unavailable' else "time restrictions"
                lecture_conflict_reasons.append(f"{day} from {start_time}:00 to {end_time}:00 ({conflict_reason}).")

        if not lecture_scheduled:
            scheduling_errors.append(f"Lecture for {course.name} could not be scheduled due to {','.join(lecture_conflict_reasons)}.")
            print(f"Error scheduling {course.name} lecture: {lecture_conflict_reasons}")

        # Try to schedule practices
        for practice in course.practices:
            day = practice.day
            start_time = practice.start_time.hour
            end_time = practice.end_time.hour

            print(f"Attempting to schedule {course.name} practice on {day} from {start_time}:00 to {end_time}:00")

            # Check for conflicts
            conflicting_course = check_for_conflicts(day, start_time, end_time)
            if conflicting_course is None:
                # Schedule the practice
                for hour in range(start_time, end_time):
                    timetable[day][hour] = {'course_name': course.name, 'type': 'Practice'}
                print(f"Scheduled {course.name} practice on {day} from {start_time}:00 to {end_time}:00")
                practice_scheduled = True
                break
            else:
                conflict_reason = f"conflicts with {conflicting_course['course_name']}" if conflicting_course != 'Unavailable' else "time restrictions"
                practice_conflict_reasons.append(f"{day} from {start_time}:00 to {end_time}:00 ({conflict_reason}).")

        if not practice_scheduled:
            scheduling_errors.append(f"Practice for {course.name} could not be scheduled due to {', '.join(practice_conflict_reasons)}.")
            print(f"Error scheduling {course.name} practice: {practice_conflict_reasons}")

    return timetable, scheduling_errors
  
def spread_courses_across_days(timetable, schedule):
    """Spread courses evenly across the week, avoiding conflicts."""
    for course, slot in schedule:
        day = slot['day']
        start_time = slot['start_time'].hour
        end_time = slot['end_time'].hour

        for target_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            if is_time_available(timetable, target_day, start_time, end_time):
                for hour in range(start_time, end_time):
                    timetable[target_day][hour] = f"{course.name} ({slot['type']})"
                break
    return timetable

def pack_courses_into_fewer_days(timetable, schedule):
    """Pack courses into fewer days while avoiding entirely empty days."""
    packed_days = ['Thursday', 'Friday']
    other_days = ['Monday', 'Tuesday', 'Wednesday']

    for course, slot in schedule:
        start_time = slot['start_time'].hour
        end_time = slot['end_time'].hour

        for target_day in packed_days:
            if is_time_available(timetable, target_day, start_time, end_time):
                for hour in range(start_time, end_time):
                    timetable[target_day][hour] = f"{course.name} ({slot['type']})"
                break
        else:
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

def save_data_to_db(data):
    for course in data.get('courses', []):
        new_course = Course(
            name=course['name'],
            coursenumber=course['coursenumber'],
            lectures=course.get('lectures', []),
            practices=course.get('practices', [])
        )
        db.session.add(new_course)
    db.session.commit()

UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist


@app.route('/upload_json', methods=['GET', 'POST'])
@login_required
def upload_json():
    if request.method == 'POST':
        if 'json_file' not in request.files:
            flash("No file part in the request", "danger")
            return redirect(request.url)

        file = request.files['json_file']

        if file.filename == '':
            flash("No file selected", "danger")
            return redirect(request.url)

        if file and file.filename.endswith('.json'):
            try:
                # Save the file in the "uploads" directory
                filename = secure_filename(file.filename)
                file_path = os.path.join('uploads', filename)
                
                # Ensure the uploads directory exists
                if not os.path.exists('uploads'):
                    os.makedirs('uploads')

                file.save(file_path)

                # Load the JSON data from the file
                with open(file_path, 'r') as f:
                    data = json.load(f)

                # Process the JSON data and save it to the database
                for course_data in data['courses']:
                    new_course = Course(
                        name=course_data['name'],
                        coursenumber=course_data['coursenumber'],
                        user_id=current_user.id  # Link course to the logged-in user
                    )
                    db.session.add(new_course)
                    db.session.flush()  # Flush to get the course ID for foreign keys

                    # Add lectures
                    for lecture_data in course_data.get('lectures', []):
                        lecture = LectureTime(
                            day=lecture_data['day'],
                            start_time=lecture_data['start_time'],
                            end_time=lecture_data['end_time'],
                            building=lecture_data['building'],
                            classroom=lecture_data['classroom'],
                            course_id=new_course.id
                        )
                        db.session.add(lecture)

                    # Add practices
                    for practice_data in course_data.get('practices', []):
                        practice = PracticeTime(
                            day=practice_data['day'],
                            start_time=practice_data['start_time'],
                            end_time=practice_data['end_time'],
                            building=practice_data['building'],
                            classroom=practice_data['classroom'],
                            course_id=new_course.id
                        )
                        db.session.add(practice)

                # Commit the changes to the database
                db.session.commit()

                flash('Data saved successfully!', 'success')
                return redirect(url_for('courses'))

            except json.JSONDecodeError as e:
                flash(f'Error decoding JSON: {str(e)}', 'danger')
                return redirect(request.url)
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'Error saving data: {str(e)}', 'danger')
                return redirect(request.url)
            except Exception as e:
                flash(f'An unexpected error occurred: {str(e)}', 'danger')
                return redirect(request.url)

        flash("Invalid file format. Please upload a JSON file.", 'danger')
        return redirect(request.url)

    return render_template('upload_json.html')
