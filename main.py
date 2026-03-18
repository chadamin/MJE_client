# =========================
# FastAPI WebSocket 서버
# =========================

from fastapi import FastAPI, WebSocket
import json
import csv
import time

from processor import process_data

app = FastAPI()

CSV_PATH = "storage/log.csv"

# =========================
# WebSocket 엔드포인트
# =========================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    print("클라이언트 연결됨")

    while True:
        try:
            # JSON 데이터 받기
            data = await websocket.receive_text()
            data = json.loads(data)

            # KPI 계산
            result = process_data(data)

            # CSV 저장
            with open(CSV_PATH, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    time.time(),
                    result["num_objects"],
                    result["avg_distance"],
                    result["density"],
                    result["bottleneck_score"]
                ])

            print("KPI:", result)

            # 필요하면 응답도 보낼 수 있음
            await websocket.send_text("ok")

        except Exception as e:
            print("연결 종료:", e)
            break