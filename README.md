# Course Management System - File Upload Feature

## Table of Contents
1. [Project Description](#project-description)
2. [Features](#features)
3. [Technologies and Libraries](#technologies-and-libraries)
4. [Installation](#installation)
5. [Running the Project](#running-the-project)
6. [File Structure](#file-structure)
7. [Contributing](#contributing)
8. [License](#license)

---

## Project Description
This is a Course Management System that allows users to upload JSON files for course management, built with Flask and using PostgreSQL as the database. The project includes a fixed sidebar navigation, a responsive form for file uploads, and backend support for database operations.

## Features
- Upload JSON files to manage courses.
- Store course data in a PostgreSQL database.
- Sidebar navigation for easy access to different sections.
- Responsive design and modern UI.
- Database migration with Flask-Migrate.

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

