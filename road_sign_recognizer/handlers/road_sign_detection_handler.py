import numpy as np


def road_sign_detection_treatment(image_np, triton):
    road_sign_detection_results = triton.road_sign_detector.inference(image_np)

    road_sign_boxes = np.expand_dims(
        road_sign_detection_results["bboxes"], axis=0
    )
    road_sign_scores = np.expand_dims(
        road_sign_detection_results["scores"], axis=0
    )
    road_sign_labels = np.expand_dims(
        road_sign_detection_results["labels"], axis=0
    )
    return road_sign_boxes, road_sign_scores, road_sign_labels
