import sys

from io import BytesIO

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

sys.path.append("../infrastructure/")
sys.path.append("../configs/")
sys.path.append("../handlers/")

from main_handler import get_video_after_treatment

app = FastAPI()


@app.get("/")
async def read_root():
    """Displays greetings"""
    return {"Greetings": "Welcome to our Road plate recognizer"}


@app.post("/upload_video")
async def process_video(video: UploadFile = File(...)):
    result_video_path = await get_video_after_treatment(video)
    return FileResponse(result_video_path, media_type="video/mp4")
