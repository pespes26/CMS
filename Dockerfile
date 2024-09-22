# Use the official Python slim image
FROM python:3.12-slim

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
