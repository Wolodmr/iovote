# Use a base image with Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y redis-tools && apt-get clean

RUN apt-get update && apt-get install -y redis-tools netcat-openbsd && apt-get clean


# Copy application files
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait_for_it script and set execute permissions
# COPY celery_worker/wait_for_it /app/wait_for_it
# RUN chmod +x /app/wait_for_it

COPY ./celery_worker/celery_worker.sh /app/celery_worker.sh
RUN chmod +x /app/celery_worker.sh
# chmod +x ./celery-worker/celery-worker.sh



# Copy the rest of the project files
COPY . /app

# Set environment variables
ENV PYTHONPATH="/app:$PYTHONPATH"
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Command to run the Celery worker
CMD ["/bin/bash", "/app/celery_worker/celery_worker.sh"]
