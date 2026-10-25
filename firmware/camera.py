"""
camera.py - takes a photo with the pi camera module 3 and saves it.

NOTE: not tested yet, no hardware. when the camera arrives, first check the pi
even sees it:  rpicam-hello --list-cameras  (older pi os: libcamera-hello)
"""
import os
import time

from picamera2 import Picamera2
from libcamera import controls

PHOTO_DIR = os.path.expanduser("~/photos")  # every photo gets saved here, full res


def take_photo():
    """take one full-res photo, save it, return the file path"""
    os.makedirs(PHOTO_DIR, exist_ok=True)
    path = os.path.join(PHOTO_DIR, time.strftime("%Y%m%d_%H%M%S") + ".jpg")

    cam = Picamera2()
    try:
        cam.configure(cam.create_still_configuration())  # full sensor res (~12MP)
        cam.start()
        time.sleep(1)
        cam.set_controls({"AfMode": controls.AfModeEnum.Auto})
        cam.autofocus_cycle()
        cam.capture_file(path)
    finally:
        cam.close()
    return path