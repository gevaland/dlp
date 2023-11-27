import sys
from road_sign_detection_handler import road_sign_detection_treatment
from draw_handler import draw_signs_on_image
import cv2
from fastapi import UploadFile
import os
import random

sys.path.append("../infrastructure/")
from inference_model import TritonInference

from database_treatment import (
    add_video,
    create_db,
    create_tables_in_db,
)


async def process_frame(frame, triton):
    (
        road_sign_boxes,
        road_sign_scores,
        road_sign_labels,
    ) = road_sign_detection_treatment(frame, triton=triton)
    result_frame = draw_signs_on_image(
        frame,
        (
            road_sign_boxes,
            road_sign_scores,
            road_sign_labels,
        ),
    )

    return result_frame


async def get_video_after_treatment(file: UploadFile):
    create_db()
    create_tables_in_db()
    before_treatment_path, after_treatment_path = await add_video(
        file,
        file.filename,
    )
    triton = TritonInference()

    video_capture = cv2.VideoCapture(before_treatment_path)

    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(
        after_treatment_path,
        fourcc,
        fps,
        (width, height),
    )

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        processed_frame = await process_frame(frame, triton)
        video_writer.write(processed_frame)
    video_capture.release()
    video_writer.release()
    tmp_output = (
        after_treatment_path[: after_treatment_path.rfind(".")]
        + str(random.randint(0, 9999999))
        + after_treatment_path[after_treatment_path.rfind(".") :]
    )
    os.system(
        f"ffmpeg -y -i {after_treatment_path} -vcodec libx264 {tmp_output}"
    )
    os.system(f"mv {tmp_output} {after_treatment_path}")
    os.system(f"rm {tmp_output}")
    return after_treatment_path
