# Dockerfile for the web service (Django app)
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Dockerfile for celery-worker
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add the wait-for-it script to the container
COPY wait-for-it /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Copy the application code to the container
COPY . /app

# Command to wait for Redis and start the Celery worker
CMD ["sh", "-c", "wait-for-it redis:6379 -- celery -A vote_cast worker --loglevel=info"]

# Dockerfile example
FROM ubuntu:22.04

# Update package list and install redis-tools
RUN apt-get update && apt-get install -y redis-tools

# Set the default command (optional, adjust as needed)
CMD ["bash"]
