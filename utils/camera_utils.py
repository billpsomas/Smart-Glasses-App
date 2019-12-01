from picamera import PiCamera
from time import sleep

def get_snapshot_rasbery():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    camera.capture('image.jpg')
    camera.stop_preview()


