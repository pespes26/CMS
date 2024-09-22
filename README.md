# Course Management System - File Upload Feature

## Table of Contents
1. [Project Description](#project-description)
2. [Features](#features)
3. [Technologies and Libraries](#technologies-and-libraries)
4. [Installation](#installation)
5. [Running the Project](#running-the-project)
6. [File Structure](#file-structure)

---

## Project Description
The **Course Management System** is a web-based platform designed to streamline the process of managing course schedules for students and administrators. The system allows users to upload JSON files containing course data, which is then parsed and used to generate a dynamic schedule. Additionally, users can manually add courses through an intuitive form interface, providing flexibility for those who prefer to input data directly.

Built using the Flask web framework and PostgreSQL as the relational database, the system ensures smooth data management and real-time schedule generation. The platform’s goal is to provide users with an efficient way to create, view, and modify their academic schedules. Whether users upload JSON files or manually input data, the system handles it all with ease, offering the option to personalize schedules based on user preferences.

By leveraging Flask-SQLAlchemy for database interactions and Flask-Migrate for handling migrations, the system ensures reliable data management and seamless evolution of the application. The user interface is designed to be responsive, enabling seamless use across devices.

### Key Features:
- **Course Management**: Users can upload JSON files containing course data or manually add courses through a web form.
- **Dynamic Schedule Generation**: Automatically generate and display course schedules in real-time.
- **Personalization**: Users can set preferences for preferred study days, avoiding certain days, and prioritizing specific courses.
- **Real-time Updates**: As changes are made, the schedule is updated dynamically, allowing users to see the latest version without needing to refresh.
- **Responsive Design**: The interface is optimized for use across different devices, ensuring an intuitive experience on both desktop and mobile.

The platform offers a robust backend to handle all database interactions securely, and it adheres to best practices in web development, ensuring a secure, scalable, and user-friendly experience. Whether users are looking to automate schedule creation or manually manage course details, this system provides the tools they need to do so efficiently.

This project was developed to address the tedious process of creating and managing academic schedules, offering users both automation and manual flexibility.


## Technologies and Libraries

### Frontend:
- **HTML5**: Structure of the web pages.
- **CSS3**: Styling of the pages, including Flexbox for responsive layout.
- **JavaScript**: For client-side interactions (if used).
- **Font**: Poppins for modern typography.

### Backend:
- **Flask 2.0.1**: Python micro web framework for serving the web application.
- **Flask-SQLAlchemy 2.5.1**: For interacting with the PostgreSQL database.
- **Flask-Migrate 3.1.0**: For handling database migrations.
- **Werkzeug 2.0.1**: For handling various WSGI operations.
- **psycopg2-binary 2.9.1**: PostgreSQL database adapter for Python.

### Database:
- **PostgreSQL**: The relational database used to store course information.

## Installation (Windows)

### Prerequisites:
- **Python 3.7 or above** installed on your machine. You can download it from the [official Python website](https://www.python.org/downloads/).
- **PostgreSQL** installed and set up. Download it from [here](https://www.postgresql.org/download/).
- **pip** installed for package management (usually installed with Python).

### Clone the Repository:
```bash
git clone https://github.com/pespes26/CMS
cd course-management-system
```
## Create a Virtual Environment (Windows):
1. Open the Command Prompt or PowerShell.
2. Navigate to the project directory.
3. Run the following command to create a virtual environment:
```bash
python -m venv venv
```
4. Activate the virtual environment:
```bash
venv\Scripts\activate
```
### Install Required Packages:
```bash
pip install -r requirements.txt
```
## Required Packages:
These packages are listed in the requirements.txt file and will be installed automatically:
```bash
alembic==1.13.2
blinker==1.8.2
click==8.1.7
colorama==0.4.6
et-xmlfile==1.1.0
Flask==3.0.3
Flask-Login==0.6.3
Flask-Migrate==4.0.7
Flask-SQLAlchemy==3.1.1
greenlet==3.1.0
gunicorn==23.0.0
itsdangerous==2.2.0
Jinja2==3.1.4
Mako==1.3.5
MarkupSafe==2.1.5
numpy==2.1.0
openpyxl==3.1.5
packaging==24.1
pandas==2.2.2
psycopg2-binary==2.9.9
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2024.1
six==1.16.0
SQLAlchemy==2.0.34
typing_extensions==4.12.2
tzdata==2024.1
Werkzeug==3.0.3
psycopg2-binary==2.9.9 --only-binary psycopg2-binary

```
### Set up PostgreSQL:
1. Install PostgreSQL on your machine and set up a new database.
2. Configure your connection in the config.py file:
 ```bash
SQLALCHEMY_DATABASE_URI = 'postgresql://<USERNAME>:<PASSWORD>@localhost/<DB_NAME>'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Database Migrations:
1. Initialize the migrations folder:
 ```bash
flask db init
```
2. Create the migration script:
```bash
flask db migrate -m "Initial migration"
```
3. Apply the migration to the database:
```bash
flask db upgrade
```

### Running the Project:
1. Open the Command Prompt or PowerShell.
2. Navigate to the project directory.
3. Activate the virtual environment (if not already activated):
```bash
venv\Scripts\activate
```
4. Run the Flask application:
```bash
flask run
```
5. Open your browser and go to http://127.0.0.1:5000/ to view the project.

## File Structure

```bash
course-management-system/
├── app.py                   # Main Flask application file
├── config.py                # Configuration file for environment settings
├── templates/               # HTML templates for rendering views
│   └── index.html           # Main page for the app
├── static/                  # Static assets such as CSS, JavaScript, images
│   ├── styles.css           # Main stylesheet
│   └── script.js            # JavaScript file (if applicable)
├── migrations/              # Database migration files
├── upload/                  # Directory for uploaded course files
├── .env                     # Environment variables (ignored by Git)
├── requirements.txt         # List of required Python packages
├── README.md                # Project documentation (this file)
└── docker-compose.yml       # Docker configuration file for setting up the project










