# celery_worker/celery_worker.sh

set -e

while ! nc -z redis 6379; do
  echo "Waiting for Redis..."
  sleep 1
done
celery -A $CELERY_APP worker --loglevel=info

# Use the CELERY_APP environment variable, fallback to default
: "${CELERY_APP:=vote_cast.celery_app}"

# #!/bin/sh
# # Wait for the dependent services to be ready (e.g., Redis or RabbitMQ)
# if [ "$WAIT_FOR_IT" = "yes" ]; then
#   echo "Waiting for Redis to be available..."
#   /app/wait_for_it redis:6379 -- echo "Redis is up and running"
# fi

#!/bin/bash

# Wait for Redis to be ready (optional)
if [ -n "$REDIS_HOST" ]; then
    echo "Waiting for Redis..."
    until nc -z "$REDIS_HOST" "$REDIS_PORT"; do
        sleep 1
    done
fi
echo "Redis is ready. Starting Celery..."
celery -A vote_cast.celery_app worker --loglevel=info

python -c "import sys; print(sys.path)"

# Start the Celery worker
#!/bin/bash
echo "Starting Celery worker..."
export PYTHONPATH=/app

# Start the Celery worker
# celery -A vote_cast.celery_app.app worker --loglevel=info
celery -A vote_cast.celery_app worker --loglevel=debug


# chmod +x /app/wait_for_it

chmod +x ./celery_worker/celery_worker.sh





