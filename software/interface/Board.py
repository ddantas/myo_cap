# -*- coding: utf-8 -*-

from serial import Serial
import sys
import glob

SHIFT = 60
MAX_CODE = 64

class Board:

    def __init__(self, settings):
        self.settings = settings
        self.serial = Serial()
        self.serial.baudrate = self.settings.getBaudrate()

    def testPort(self, port):
        self.serial.port = port
        self.serial.open()
        self.serial.close()

    def listPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                self.testPort(port)
                result.append(port)
            except:
                pass

        self.port = ''

        return result

    def start(self):
        self.serial.write("start\n")

    def stop(self):
        self.serial.write("stop\n")

    def rcvPkt(self):
        while self.serial.inWaiting() == 0:
            pass

        samples = []
        num_channels = self.settings.getChannelsPerBoard() * self.settings.getNBoards()

        # read from serial port
        packet = self.serial.readline()
        for i in range(num_channels):
            pos = i * 2
            samples.append(round((self.strToInt(packet[pos:pos + 2])), 5))

        return samples

    def strToInt(self, word):
        if (len(word) > 1):
            return int(((ord(word[0]) - SHIFT) * MAX_CODE) + (ord(word[1]) - SHIFT))
        else:
            return 0