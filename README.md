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
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-Migrate==3.1.0
psycopg2-binary==2.9.1
Werkzeug==2.0.1
SQLAlchemy==1.3.23
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

### File Stuture:

├── app.py                   # Main Flask application file
├── config.py                # Configuration file for database settings
├── templates/               # HTML files for Flask
│   └── index.html           # Main page template
├── static/                  # Static files such as CSS, JavaScript, and images
│   └── styles.css           # Main stylesheet
├── migrations/              # Folder for database migrations
├── upload/                  # Folder for uploaded files
├── .env                     # Environment file to store secrets (not tracked in Git)
├── README.md                # Project documentation
└── requirements.txt         # List of required Python packages




-





