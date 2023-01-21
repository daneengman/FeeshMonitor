enabled = True

try:
    from picamera2 import Picamera2
except:
    print("picamera unable to be imported")
    enabled = False

import datetime
import os
import time

class Camera:
    def __init__(self):
        if not os.path.exists("Photos"):
            os.mkdir("Photos")
        
        self.picam2 = Picamera2()
        self.picam2.start()
        time.sleep(2)
        print("word")
    
    def get_filepath(self):
        date = datetime.datetime.now().date() # issues with timezone?
        if not os.path.exists(f"Photos/{date}"):
            os.mkdir(f"Photos/{date}")
        return f"Photos/{date}/{datetime.datetime.now()}.png"
        

    def take_picture(self):
        if not enabled:
            return
        
        # picam2 = Picamera2()
        # camera_config = picam2.create_preview_configuration()
        # picam2.configure(camera_config)
        # picam2.start_preview(Preview.QTGL)
        self.picam2.capture_file(self.get_filepath())
        # with PiCamera() as camera:
        #     time.sleep(2)
        #     camera.resolution = (1280, 720)
        #     # camera.resolution = (1280, 720)
        #     camera.vflip = True
        #     camera.contrast = 10

        #     #taking a picture
        #     camera.capture(self.get_filepath())





# print("Took picture.")

# #taking a video
# file_name = "/home/pi/Pictures/video_" + str(time.time()) + ".h264"

# print("Start recording...")
# camera.start_recording(file_name)
# camera.wait_recording(5)
# camera.stop_recording()
# print("Finished recording.")