import numpy as np
from storage import prev_objects
from decision import assign_car

# =========================
# 기본 계산
# =========================

def calc_distance(o):
    return np.sqrt(o.x**2 + o.y**2 + o.z**2)

def calc_speed(curr, prev):
    dt = curr.timestamp - prev["timestamp"]

    if dt <= 0:
        return 0

    dx = curr.x - prev["x"]
    dy = curr.y - prev["y"]
    dz = curr.z - prev["z"]

    return np.sqrt(dx**2 + dy**2 + dz**2) / dt


def calc_object_distance(o1, o2):
    return np.sqrt(
        (o1.x - o2.x)**2 +
        (o1.y - o2.y)**2 +
        (o1.z - o2.z)**2
    )


def calc_volume(o):
    return o.width * o.height * o.depth


# =========================
# 메인 처리
# =========================

def process_frame(data):

    object_results = []

    # -------------------------
    # 객체별 처리
    # -------------------------
    for obj in data.objects:

        result = {}
        result["id"] = obj.id

        # 거리
        distance = calc_distance(obj)
        result["distance"] = distance

        # 속도
        if obj.id in prev_objects:
            speed = calc_speed(obj, prev_objects[obj.id])
        else:
            speed = 0

        result["speed"] = speed

        # 소요 시간 (distance / speed)
        if speed > 0:
            result["eta"] = distance / speed
        else:
            result["eta"] = None

        # 부피
        volume = calc_volume(obj)
        result["volume"] = volume

        # RC카 배정
        result["rc_car"] = assign_car(volume)

        # 저장
        prev_objects[obj.id] = obj.dict()

        object_results.append(result)

    # -------------------------
    # 객체 간 거리
    # -------------------------
    pair_distances = []

    for i in range(len(data.objects)):
        for j in range(i + 1, len(data.objects)):

            d = calc_object_distance(data.objects[i], data.objects[j])

            pair_distances.append({
                "pair": [data.objects[i].id, data.objects[j].id],
                "distance": d
            })

    return {
        "objects": object_results,
        "object_distances": pair_distances
    }
