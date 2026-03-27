# server.py

from fastapi import FastAPI
from models import FrameData
from processor import process_frame

import cv2
from visualizer import draw_map

app = FastAPI()

# =========================
# 서버 상태 (선택: FPS 확인용)
# =========================
frame_count = 0


# =========================
# 메인 API
# =========================
@app.post("/frame")
def frame(data: FrameData):
    global frame_count

    # -------------------------
    # 1. 데이터 처리 (거리, 속도 등)
    # -------------------------
    result = process_frame(data)

    # -------------------------
    # 2. 시각화 (Top View)
    # -------------------------
    try:
        img = draw_map(result["objects"])

        cv2.imshow("Top View (Mac)", img)
        cv2.waitKey(1)

    except Exception as e:
        print("Visualization Error:", e)

    # -------------------------
    # 3. 간단한 로그 (디버깅용)
    # -------------------------
    frame_count += 1

    if frame_count % 30 == 0:
        print(f"[INFO] Received frames: {frame_count}")

    # -------------------------
    # 4. 결과 반환 (Ubuntu 비교용)
    # -------------------------
    return result