#
# Detector Alignment Tool
# for use with JANUS KED
#
# ServoControllerObject Library for use with 
# SRVOCNTL hardware revision C
#  
# Coherent Photon Imaging, LLC
# Released under GPLv2, see LICENSE
# for information. 
# Version 0.2
# Thomas Ales, Feb 29 2020
#

import serial
import serial.tools.list_ports

class ServoControllerObject:
    
    def __init__(self):
        # Status bools
        self.is_connected = False
        self.is_homed = False

        # Requested Channel Configuration
        self.req_servo_channel = 0
        self.req_steps = 0
        self.req_direction = 0

        # Serial Details
        self.com_port = None

        # Channel Configuration Details
        # TODO: implement persistent JSON configuration for
        #       this structure
        self.channels = {"lf_pitch": {"channel": 0, "homed": False, "count": 0},
                        "lf_yaw": {"channel": 1, "homed": False, "count": 0}, 
                        "lr_pitch": {"channel": 2, "homed": False, "count": 0},
                         "lr_yaw": {"channel": 3, "homed": False, "count": 0}, 
                         "rf_pitch": {"channel": 4, "homed": False, "count": 0}, 
                         "rf_yaw": {"channel": 5, "homed": False, "count": 0},
                         "rr_pitch": {"channel": 6, "homed": False, "count": 0}, 
                         "rr_yaw": {"channel":  7, "homed": False, "count": 0},
                         "prism": {"channel": 8, "homed": False, "count": 0},
                         "pbs_pitch": {"channel": 9,  "homed": False, "count": 0},
                          "pbs_yaw": {"channel": 10, "homed": False, "count": 0},
                          "di_pitch": {"channel": 11, "homed": False, "count": 0},
                         "di_yaw": {"channel": 12, "homed": False, "count": 0}, 
                         "fo_pitch": {"channel": 13, "homed": False, "count": 0}, 
                         "fo_yaw": {"channel": 14, "homed": False, "count": 0},
                         "target_l": {"channel": 15, "inserted": False}, 
                         "target_r": {"channel": 16, "inserted": False}}
        
        return

    def scan_ports(self):
        '''
        scan_ports(): Checks the COM ports for any microcontrollers that 
                      may be connected. Currently returns a list of all
                      valid COM ports connected to the host.

        '''
        possible_ports = serial.tools.list_ports.comports()
        if possible_ports.__len__() == 0:
            print("No valid COMports found.")
            _portlist = ["No valid ports found."]
        else:
            _portlist = []
            for current_port in possible_ports:
                self._portlist.append(current_port.__str__())
         
        return _portlist

    def connect(self):
        '''
        connect(): connects to the COM port selected by the QComboBox.
                   expects that scan_ports() has been called already so that the 
                   QComboBox has the correct port listed.
        '''

        return








