import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0)

# Clear the current database
client.flushdb()

# Uncomment the following line to clear all databases:
# client.flushall()

print("Redis cache cleared.")
