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
        super(Ui, self).__init__()
        loadUi('servomcu_ui.ui', self)
        self.s_controller = servocontroller.ServoController()
        for comport in self.s_controller.list_coms():
            self.comport_combo.addItem(comport)
        
        self.mcu_toggleconnect.clicked.connect(partial(self.mcu_toggle, self.comport_combo.currentText()))

        self.show()

    def mcu_toggle(self, comport):
        if(self.mcu_toggleconnect.text() == "Connect"):
            self.s_controller.connect_mcu(comport)
            self.mcu_toggleconnect.setText("Disconnect")
        elif(self.mcu_toggleconnect.text() == "Disconnect"):
            self.s_controller.disconnect_mcu()
            self.mcu_toggleconnect.setText("Connect")

if __name__ == '__main__':
    import sys
    import PyQt5
    app = QApplication(sys.argv)
    window = Ui()

    sys.exit(app.exec_())