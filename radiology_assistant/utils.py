import os
import uuid
from flask import current_app, session
from PIL import Image
import threading
import time
from radiology_assistant import app


def schedule_img_delete(img, secs, cur_app):
    time.sleep(secs)
    try:
        with cur_app.app_context():
            os.remove(os.path.join(cur_app.root_path, "static", "images", "temp", img))
    except:
        pass

def save_temp_image(img, secs):
    img_id = uuid.uuid4().hex
    _, img_ext = os.path.splitext(img.filename)
    img_name = img_id + img_ext
    img_path = os.path.join(current_app.root_path, "static", "images", "temp", img_name)

    p_img = Image.open(img)
    p_img.save(img_path)
    threading.Thread(target=schedule_img_delete, args=(img_name, secs, app), daemon=True).start()
    return img_name

def session_image(img_name):
    if session.get("uploaded_image") is not None:
        try:
            os.remove(os.path.join(current_app.root_path, "static", "images", "temp", session.get("uploaded_image")))
        except:
            pass
    session["uploaded_image"] = img_name

def dump_temp():
    temp = os.path.join(current_app.root_path, "static", "images", "temp")
    for f in os.listdir(temp):
        os.remove(os.path.join(temp, f))