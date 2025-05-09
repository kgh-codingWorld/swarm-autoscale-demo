import pika # RabbitMQ과의 통신 담당
import subprocess
import time
from config import RABBITMQ_HOST, QUEUE_NAME, FASTAPI_SERVICE_NAME, WORKER_SERVICE_NAME

def get_queue_length():
    # RabbitMQ에 연결
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    # 채널 생성
    channel = connection.channel()
    # queue_declare: 큐의 상태 확인
    q = channel.queue_declare(queue=QUEUE_NAME, durable=True, passive=False)
    # message_count: 현재 큐에 쌓여있는 메시지 수
    length = q.method.message_count
    connection.close()
    return length

def decide_scale(length: int) -> int:
    if length > 50:
        return 5
    elif length > 30:
        return 4
    elif length > 20:
        return 3
    elif length > 10:
        return 2
    else:
        return 1


def get_current_scale(service: str) -> int:
    result = subprocess.run(
        ["docker", "service", "ps", service, "--filter", "desired-state=running", "--format", "{{.Name}}"],
        stdout=subprocess.PIPE,
        text=True
    )
    return len(result.stdout.strip().splitlines())

def scale_service(service: str, replicas: int):
    print(f"[스케일링] {service} → {replicas} replicas")
    subprocess.run(["docker", "service", "scale", f"{service}={replicas}"])

def monitor():
    print(f"[시작] RabbitMQ 큐 상태 감시 시작 (QUEUE = {QUEUE_NAME})")
    while True:
        try:
            length = get_queue_length()

            fastapi_desired = decide_scale(length)
            fastapi_current = get_current_scale(FASTAPI_SERVICE_NAME)

            worker_desired = decide_scale(length)
            worker_current = get_current_scale(WORKER_SERVICE_NAME)

            print(f"[큐 상태] 메시지 {length}개 → FastAPI {fastapi_desired} / {fastapi_current}, Worker {worker_desired} / {worker_current}")

            if fastapi_desired != fastapi_current:
                scale_service(FASTAPI_SERVICE_NAME, fastapi_desired)

            if worker_desired != worker_current:
                scale_service(WORKER_SERVICE_NAME, worker_desired)

            time.sleep(2) # 큐 상태를 2초마다 점검(현재 메시지 개수, 현재 서비스 replica 개수, 조정 필요 여부)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    monitor()
