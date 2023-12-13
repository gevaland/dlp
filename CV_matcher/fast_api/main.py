import sys
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

sys.path.append("../infrastructure/")
sys.path.append("../configs/")
sys.path.append("../handlers/")


from main_handler import get_closest_files, populate_db
from database_treatment import (
    create_db,
    create_tables_in_db,
)

app = FastAPI()
create_db()
create_tables_in_db()
populate_db()


@app.get("/")
async def read_root():
    """Displays greetings"""
    return {"Greetings": "Welcome to our CV matcher"}


@app.post("/matching/{option}")
async def process_file(option: str, file: UploadFile = File(...)):
    closest_files = await get_closest_files(file, option)
    return JSONResponse(content=closest_files)
