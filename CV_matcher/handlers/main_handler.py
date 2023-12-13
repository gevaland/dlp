import sys

# from dlp.CV_matcher.handlers.cv_matcher_handler import (
#     road_sign_detection_treatment,
# )
from fastapi import UploadFile
import os
import random

sys.path.append("../infrastructure/")
sys.path.append("../configs/")
# from inference_model import TritonInference

from main_config import resume_storage, job_storage

from database_treatment import (
    add_file_to_db,
    get_all_jobs,
    get_all_resumes,
    get_resume_by_id,
    get_job_by_id,
    populate_resumes,
    populate_jobs,
)


def count_distance(one_file, rest_files):
    distances = []
    for rf in rest_files:
        if one_file.file_path != rf.file_path:
            distance = 0
            for x in range(len(one_file.vector)):
                distance += (one_file.vector[x] - rf.vector[x]) ** 2
            distance **= 0.5
            distances.append((rf, distance))
    top5 = sorted(distances, key=lambda x: x[1])[:5]
    return [x[0] for x in top5]


def get_text_vector(file_full_path):  # Этот вызов нужно передалать!
    with open(f"{file_full_path}", "r") as f:
        file_size = len(f.read())
    return [file_size]


def get_top5(file_id: UploadFile, option: str = None):
    if option == "Resume":
        top5 = count_distance(get_resume_by_id(file_id), get_all_jobs())
    elif option == "Job":
        top5 = count_distance(get_job_by_id(file_id), get_all_resumes())
    return top5


async def save_file(file: UploadFile, file_full_path: str):
    with open(file_full_path, "wb") as f:
        content = await file.read()
        f.write(content)


async def get_closest_files(file: UploadFile, option: str):
    storage_name = resume_storage if option == "Resume" else job_storage
    file_full_path = os.path.join(os.getcwd(), storage_name, file.filename)
    await save_file(file, file_full_path)
    vector = get_text_vector(file_full_path)
    file_id = await add_file_to_db(
        file,
        file.filename,
        option,
        vector,
    )
    closest_files = get_top5(file_id, option)
    closest_files_paths = [
        os.path.join(os.getcwd(), storage_name, x.file_path)
        for x in closest_files
    ]
    # triton = TritonInference()
    return {"files": closest_files_paths}


def populate_db():
    populate_resumes(
        os.path.join(os.getcwd(), resume_storage),
        vector_generator=get_text_vector,
    )
    populate_jobs(
        os.path.join(os.getcwd(), job_storage),
        vector_generator=get_text_vector,
    )
