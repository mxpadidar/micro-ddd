import time

from celery import Celery

from shared.logger import Logger
from shared.message_broker import RedisMessageBroker
from shared.settings import REDIS_DB, REDIS_HOST, REDIS_PORT

logger = Logger("Celery Worker")

app = Celery("micro_ddd", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")


message_broker = RedisMessageBroker(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


@app.task
def start_storage_cursor():
    message_broker.subscribe("file_used")

    while True:
        message = message_broker.get_message()
        if message:
            file_id = message["file_id"]
            user_id = message["user_id"]
            logger.info(f"File {file_id} was used by user {user_id}")
        else:
            # If there are no messages, sleep for a short time to avoid busy-waiting
            time.sleep(0.1)


@app.task
def start_auth_cursor():
    print("Starting auth cursor")


if __name__ == "__main__":
    app.start()
