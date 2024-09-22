# Use a slim Python image
FROM python:3.12-slim

# Install required system packages
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set the working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose the application port
EXPOSE 8000

# Start the app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]