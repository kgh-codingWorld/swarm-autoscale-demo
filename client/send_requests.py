import httpx
import time

URL = "http://localhost/async-task"  # Nginx가 프록시로 요청을 FastAPI에 전달함

while True:
    try:
        # FastAPI에 비동기 작업 요청 전송
        res = httpx.get(URL)
        # 응답 상태 코드와 JSON 내용 출력
        print("[요청 결과]", res.status_code, res.json())
    except Exception as e:
        print("[에러]", e)
    time.sleep(0.5)  # 0.5초 간격으로 부하 전송
