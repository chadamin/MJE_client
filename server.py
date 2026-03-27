from fastapi import FastAPI
from models import FrameData
from processor import process_frame

app = FastAPI()

@app.post("/frame")
def frame(data: FrameData):
    return process_frame(data)