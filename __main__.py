#
# Detector Alignment Tool
# for use with JANUS KED
# 
# Coherent Photon Imaging, LLC
# Released under GPLv2, see LICENSE
# for information. 
# Version 0.2
# Thomas Ales, Feb 29 2020
from functools import partial
import sys
import threading
import time
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import cv2

from guilogic import ServoGUI, CameraObject

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('servonew.ui', self)
        self.show()
        self.gui_logic = ServoGUI()
        self.cameras = CameraObject()
        # Initalization Functions
        self.populate_ccd_combobox()
        # Qt Signal and Slot Functions
        self.cbox_ccds.currentIndexChanged.connect(self.change_ccd_source)
        self.ccd_update_qtimer = QtCore.QTimer()
        self.ccd_update_qtimer.timeout.connect(self.image_updater)
        self.ccd_update_qtimer.start(1000./60)
        # Startup Camera Thread
        self.frame_grabber = threading.Thread(self.cameras.camera_thread(
                                              self.cbox_ccds.currentIndex()), daemon=True)
        self.frame_grabber.run()

    def populate_ccd_combobox(self):
        '''
        populate_ccd_combobox: Scans through for the available cameras and populates the QtComboBox with
                               the image from the CCD.
        '''
        for camera_idx in range(0, self.cameras.available_cameras.__len__()):
            self.cbox_ccds.addItem("Camera " + camera_idx.__str__())

    def image_updater(self):
        '''
        image_updater(): Designed to be used with a QTimer. Repaints the graphics
                         view with the newest image from the selected CCD.
        '''
        _newScene = QtWidgets.QGraphicsScene()
        _qtimage = QtGui.QImage(self.cameras.current_opencv_frame, self.cameras.current_opencv_frame.shape[1],
                                self.cameras.current_opencv_frame.shape[0], QtGui.QImage.Format_RGB888)
        _pixmap = QtGui.QPixmap.fromImage(_qtimage)
        self.gv_ccdview.setScene(_newScene)
        _newScene.addPixmap(_pixmap)
        self.gv_ccdview.show()
        return

    def change_ccd_source(self, requested_camera=0):
        '''
        change_ccd_source(requested_camera): Function to connect to the QtComboBox
                                             indexChanged signal and start painting
                                             the new images to the QtGraphicsView.
        '''
        print("Requested Camera was: " + requested_camera.__str__())
        self.cameras.hasCCDChanged = True
        self.frame_grabber = threading.Thread(self.cameras.camera_thread(
                                              self.cbox_ccds.currentIndex()), daemon=True)

        


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

