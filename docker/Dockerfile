# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install the necessary packages directly
RUN pip install --no-cache-dir Flask==2.1.2 Flask-SQLAlchemy==2.5.1 psycopg2-binary==2.9.3

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py

# Run flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
