# GUI Business Logic for KED Detector
# Alignment tool.
#
# Thomas Ales, Coherent Photon Imaging, LLC
# Feb 2020

import cv2
import time
from PyQt5 import QtGui

class ServoGUI:

    def __init__(self):
        self.GUIEnabled = True
        pass
        
class CameraObject:

    def __init__(self):
        '''
            __init__(): Constructor. On initalization, walk all connected cameras and
                        create an array that's usable by the VideoCapture constructor.
        '''
        cam_index = 0
        self.available_cameras = []

        self.isConnected = False
        self.isRunning = False
        self.hasCCDChanged = False
        self.current_camera_idx = 0
        self.current_opencv_frame = ''
        
        # Loop through all appending an array of all possible connected cameras. 
        # Once you get a camera that doesn't give you anything, stop.
        while True:
            tempcap = cv2.VideoCapture(cam_index + cv2.CAP_DSHOW)
            if not tempcap.read()[0]:
                break
            else:
                self.available_cameras.append(cam_index)
                tempcap.release()
                cam_index += 1
            
        return

    def camera_thread(self, camera_number, sleep_time=0.016):
        '''
        start_camera(camera_number): Starts the thread that grabs images off of the camera and paints it to the image
                                     image qtWidget. 
        '''
        _this_camera = cv2.VideoCapture(camera_number + cv2.CAP_DSHOW)
        self.isConnected = True
        self.isRunning = True
        self.hasCCDChanged = False
        while self.hasCCDChanged == False:
            # this kills the thread if the isRunning parameter is set False by an 
            # outside process
            if(self.isRunning == False):
                break
            # Grab image and sleep for requested amount of time
            retval, _opencv_frame = _this_camera.read()
            _rgb_img = cv2.cvtColor(_opencv_frame, cv2.COLOR_BGR2RGB)
            self.current_opencv_frame = _rgb_img
            cv2.waitKey(int(sleep_time*1000))
            time.sleep(sleep_time)
        self.isRunning = False
        _this_camera.release()
        self.isConnected = False
        return