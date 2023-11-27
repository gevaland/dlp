import sys

sys.path.append("../infrastructure/")
sys.path.append("../configs/")

from drawing import (
    draw_all_on_image,
)


def draw_signs_on_image(image_np, data):
    result_img = draw_all_on_image(image_np, data)
    return result_img
