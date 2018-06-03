
class ApiTiva():
    def setBps(self, serial, value):
        serial.write("B "+ str(value)+"\n")
        # waiting serial data
        while serial.inWaiting() == 0:
            pass
        packet = serial.readline()

    def setSampleRate(self, serial, value):
        serial.write("S "+ str(value)+"\n")
        # waiting serial data
        while serial.inWaiting() == 0:
            pass
        packet = serial.readline()

    def setNChannels(self, serial, value):
        serial.write("C "+ str(value)+"\n")
        # waiting serial data
        while serial.inWaiting() == 0:
            pass
        packet = serial.readline()

    def setNBoards(self, serial, value):
        serial.write("N "+ str(value)+"\n")
        # waiting serial data
        while serial.inWaiting() == 0:
            pass
        packet = serial.readline()

    def start(self, serial):
        serial.write("start\n")
        # waiting serial data
        while serial.inWaiting() == 0:
            pass
        packet = serial.readline()

    def stop(self, serial):
        serial.write("stop\n")
        # waiting serial data
        while serial.inWaiting() == 0:
            pass
        packet = serial.readline()
