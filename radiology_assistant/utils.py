import os
import uuid
from flask import current_app
from PIL import Image

def save_temp_image(img):
    img_id = uuid.uuid4().hex
    _, img_ext = os.path.splitext(img.filename)
    img_name = img_id + img_ext
    img_path = os.path.join(current_app.root_path, "static", "images", "temp", img_name)

    p_img = Image.open(img)
    p_img.save(img_path)
    return img_name