from functools import partial
import glob
import os
import serial
import serial.tools.list_ports
import pyfirmata

from PyQt5.uic import loadUiType, loadUi
from PyQt5.Qt import QMainWindow, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QTabWidget, QComboBox

import servocontroller

class Ui(QMainWindow):

    def __init__(self):
        # Load the ui file from the same directory
        super(Ui, self).__init__()
        loadUi('servomcu_ui.ui', self)
        # Initalize the ServoController object, and populate the COM port list.
        self.s_controller = servocontroller.ServoController()

        for comport in self.s_controller.list_coms():
            self.comport_combo.addItem(comport)
        
        # Qt Signals/Slots routing
        self.mcu_toggleconnect.clicked.connect(partial(self.mcu_toggle, self.comport_combo.currentText()))
        self.lr_pitch_slider.valueChanged.connect(self.lf_pitch_update)
        self.lr_pitch_stop.clicked.connect(self.lf_pstop)
        # Show the UI
        self.show()

    def mcu_toggle(self, comport):
        
        """mcu_toggle(comport): Connect/Disconnect to the microcontroller and update the MCU connect/disconnect button."""

        if(self.mcu_toggleconnect.text() == "Connect"):
            self.s_controller.connect_mcu(comport)
            self.mcu_toggleconnect.setText("Disconnect")
        elif(self.mcu_toggleconnect.text() == "Disconnect"):
            self.s_controller.disconnect_mcu()
            self.mcu_toggleconnect.setText("Connect")

    def lf_pitch_update(self, angle):
        self.s_controller.update_servo(self.s_controller.servo_pins[0], angle)

    def lf_pstop(self):
        self.lr_pitch_slider.setValue(self.s_controller.servo_stop_position)

if __name__ == '__main__':

    import sys
    import PyQt5
    app = QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())