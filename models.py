from pydantic import BaseModel
from typing import List

class ObjectData(BaseModel):
    id: int
    x: float
    y: float
    z: float
    width: float
    height: float
    depth: float
    timestamp: float

class FrameData(BaseModel):
    objects: List[ObjectData]