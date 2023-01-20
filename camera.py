from picamera import PiCamera
import time

class camera:
    def __init__(self):
        pass

    def take_picture(self, filepath):
        camera = PiCamera()
        # time.sleep(2)
        camera.resolution = (1280, 720)
        camera.resolution = (1280, 720)
        camera.vflip = True
        camera.contrast = 10

        #taking a picture
        camera.capture(filepath)





# print("Took picture.")

# #taking a video
# file_name = "/home/pi/Pictures/video_" + str(time.time()) + ".h264"

# print("Start recording...")
# camera.start_recording(file_name)
# camera.wait_recording(5)
# camera.stop_recording()
# print("Finished recording.")