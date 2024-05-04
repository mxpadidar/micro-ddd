import redis

r = redis.Redis(host="localhost", port=6379, db=0)

# subscribe to a channel
pubsub = r.pubsub()
pubsub.subscribe("events")

# listen for messages

for message in pubsub.listen():
    print(message)
