import pyfirmata
import serial

class ServoController:

    def __init__(self):
        super().__init__()
        self.com_port = ''
        self.mcu_instance = ''
        self.mcu_iterator = ''

    def connect_mcu(self, com_port):
        self.mcu_instance = pyfirmata.ArduinoMega(com_port)
        self.mcu_iterator = pyfirmata.util.Iterator(self.mcu_instance)
        self.mcu_iterator.start()

    def disconnect_mcu(self):
        self.mcu_instance.exit()
        
    def list_coms(self):
        com_strings = []
        for comports in serial.tools.list_ports.comports():
            com_strings.append(comports.device)

        return com_strings