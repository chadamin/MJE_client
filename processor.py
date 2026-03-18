# =========================
# KPI 계산 모듈
# =========================

import numpy as np


def process_data(data):
    """
    Ubuntu에서 받은 데이터(JSON)를 기반으로
    KPI 계산 수행
    """

    objects = data.get("objects", [])
    pointcloud = data.get("pointcloud", [])

    # =========================
    # 1. 객체 수 (Queue Length)
    # =========================
    num_objects = len(objects)

    # =========================
    # 2. 평균 거리
    # =========================
    distances = [obj["distance"] for obj in objects if obj["distance"] > 0]

    if len(distances) > 0:
        avg_distance = np.mean(distances)
    else:
        avg_distance = 0

    # =========================
    # 3. Point Cloud 밀도
    # =========================
    # 간단히: 점 개수 기반
    density = len(pointcloud)

    # =========================
    # 4. 병목 점수 (간단 모델)
    # =========================
    # 객체 많고 거리 가까울수록 위험

    bottleneck_score = 0

    if num_objects > 0:
        bottleneck_score = (num_objects * 0.5) + (1 / (avg_distance + 0.1))

    return {
        "num_objects": num_objects,
        "avg_distance": float(avg_distance),
        "density": density,
        "bottleneck_score": float(bottleneck_score)
    }