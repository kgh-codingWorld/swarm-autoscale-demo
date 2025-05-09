from fastapi import FastAPI
import pika
import json
import random
import socket
from config import RABBITMQ_HOST, QUEUE_NAME

app = FastAPI()

@app.get("/async-task")
def send_task():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    duration = random.randint(1, 10)
    task_data = {"action": "sleep", "duration": duration}
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(task_data),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()
    return {
        "status": "task queued",
        "duration": duration,
        "handled_by": socket.gethostname()  # 여기서 어떤 인스턴스가 처리했는지 확인 가능
    }
