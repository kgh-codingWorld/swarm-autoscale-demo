import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = os.getenv("QUEUE_NAME", "task_queue")
FASTAPI_SERVICE_NAME = os.getenv("FASTAPI_SERVICE_NAME")
WORKER_SERVICE_NAME = os.getenv("WORKER_SERVICE_NAME")