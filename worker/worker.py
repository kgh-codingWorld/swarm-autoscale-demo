import pika
import time
import json
from config import RABBITMQ_HOST, QUEUE_NAME

def callback(ch, method, properties, body):
    task = json.loads(body)
    duration = task.get("duration", 1)
    print(f"[작업 수신] {task} → {duration}초 대기")
    time.sleep(duration)
    print(f"[작업 완료] {task}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print("[시작] 워커가 작업을 기다립니다...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
