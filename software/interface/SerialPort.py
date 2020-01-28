
import sys
import glob
from serial import Serial

BAUDRATE = 921600

class SerialPort(Serial):

    def __init__(self):
        super(SerialPort, self).__init__()

        self.baudrate = BAUDRATE
        self.timeout = 1

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

    def testPort(self, port):
        self.port = port
        self.open()
        self.close()