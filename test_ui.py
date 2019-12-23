from PyQt5.uic import loadUiType, loadUi
from PyQt5.Qt import QMainWindow, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox, QTabWidget, QComboBox

import os
import glob
import serial
import serial.tools.list_ports
import pyfirmata
from functools import partial

class Ui(QMainWindow):


    def __init__(self):
        super(Ui, self).__init__()
        loadUi('test_ui.ui', self)
        self.mcu_instance = ''
        self.mcu_iterator = ''
        
        self.servo_cont_stop_position = 90
        self.servo_minimum_pulse_width = 400
        self.servo_maximum_pulse_width = 2400

        self.comport_combobox = self.findChild(QComboBox, 'com_ports')
        self.scan_com_ports()
        self.connect_mcu.clicked.connect(partial(self.connect_microcontroller, self.comport_combobox.currentText()))
        self.lr_pitch_stop.clicked.connect(self.stop_lr_pitch)
        self.disconnect_mcu.clicked.connect(self.disconnect_microcontroller)
        self.lr_pitch_v.setEnabled(False)
        self.lr_pitch_v.valueChanged.connect(self.adjust_left_rear_servos)
        
        self.show()

    def scan_com_ports(self):
        for comport in serial.tools.list_ports.comports():
            self.comport_combobox.addItem(comport.device)
        return 0

    def connect_microcontroller(self, s_comport):
        self.mcu_instance = pyfirmata.ArduinoMega(s_comport)
        self.mcu_iterator = pyfirmata.util.Iterator(self.mcu_instance)
        self.mcu_iterator.start()
        self.connect_mcu.setEnabled(False)
        self.connect_mcu.setText("Connected.")
        self.attach_left_rear_servos()
        self.lr_pitch_v.setEnabled(True)

    def attach_left_rear_servos(self, digitalpins=[5,6]):
        self.lr_pitch_servo = self.mcu_instance.get_pin('d:'+str(digitalpins[0])+':s')
        self.lr_pitch_servo.write(self.servo_cont_stop_position)

    def adjust_left_rear_servos(self, pitchvalue):
        print("new pitch value:" + pitchvalue.__str__() + "\n")
        self.lr_pitch_servo.write(pitchvalue)

    def disconnect_microcontroller(self):
        self.mcu_instance.exit()
        self.connect_mcu.setText("Connect")
        self.connect_mcu.setEnabled(True)
    
    def stop_lr_pitch(self):
        self.lr_pitch_v.setValue(90)

if __name__ == '__main__':
    import sys
    import PyQt5
    app = QApplication(sys.argv)
    window = Ui()

    sys.exit(app.exec_())