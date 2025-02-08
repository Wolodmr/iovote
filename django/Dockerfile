# Use a Python image that matches your system
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y redis-tools && apt-get clean

# Copy requirements and install them
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Expose Django development server port
EXPOSE 8000

# Default command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
