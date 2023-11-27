import cv2
import sys


sys.path.append("../configs/")
from main_config import class2color, class_num2class


def draw_rectangle(img, bbox, color=None, thickness=1):
    img = cv2.rectangle(
        img,
        pt1=(round(bbox[0]), round(bbox[1])),
        pt2=(round(bbox[2]), round(bbox[3])),
        color=color,
        thickness=thickness,
    )
    return img


def draw_text(
    img,
    text,
    org,
    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=0.35,
    color=(0, 255, 0),
    thickness=1,
):
    img = cv2.putText(
        img,
        text=text,
        org=(round(org[0]), round(org[1])),
        fontFace=fontFace,
        fontScale=fontScale,
        color=color,
        thickness=thickness,
    )
    return img


def draw_all_on_image(img, inp):
    (
        bboxes,
        scores,
        types,
    ) = (
        inp[0][0],
        inp[1][0],
        inp[2][0],
    )
    for i in range(len(bboxes)):
        color = class2color[class_num2class[types[i]]]

        img = draw_rectangle(img, bboxes[i], color=color)
        img = draw_text(
            img,
            text=class_num2class[types[i]],
            org=[bboxes[i][0], bboxes[i][1] - 2],
            color=color,
        )
    return img
