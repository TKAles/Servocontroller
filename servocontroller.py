import pyfirmata
import serial

class ServoController:

    def __init__(self):
        super().__init__()
        self.com_port = ''
        self.mcu_instance = ''
        self.mcu_iterator = ''
        self.servo_stop_position = 90
        self.servo_min_pulse_us = 400
        self.servo_max_pulse_us = 2400

        self.micro_configuration = {"LeftRear": {"Pitch": 5, "Yaw": 6},
                                    "RightRear": {"Pitch": 7, "Yaw": 8},
                                    "LeftFront": {"Pitch": 14, "Yaw": 15},
                                    "RightFront": {"Pitch": 16, "Yaw": 17},
                                    "InsertTools": {"Left": 18, "Right": 19},
                                    "Prism": 20}

    def connect_mcu(self, com_port):
        """connect_mcu(com_port): Attempts to connect to a microcontroller running StandardFirmata on com_port."""

        self.mcu_instance = pyfirmata.ArduinoMega(com_port)
        self.mcu_iterator = pyfirmata.util.Iterator(self.mcu_instance)
        self.mcu_iterator.start()
        self.attach_servos()

    def disconnect_mcu(self):
        """disconnect_mcu(): Cleanly shutsdown the instance of the microcontroller associated with this object."""
        self.mcu_instance.exit()
        
    def list_coms(self):
        """list_coms(): returns a list of the available COM ports on Windows platforms."""
        com_strings = []
        for comports in serial.tools.list_ports.comports():
            com_strings.append(comports.device)
        return com_strings
    
    def attach_servos(self):
        self.servo_pins = [self.mcu_instance.get_pin('d:'+str(self.micro_configuration["LeftRear"]["Pitch"])+':s')]
        self.servo_pins[0].write(self.servo_stop_position)

    def update_servo(self, servo_pin, angle):
        servo_pin.write(int(angle))