
class ApiTiva():
    def __init__(self):
        # codification parameters
        self.shift = 60
        self.max_code = 64

    def start(self, serial):
        serial.write("start\n")

    def stop(self, serial):
        serial.write("stop\n")

    def strToInt(self, word):
        return int(((ord(word[0]) - self.shift) * self.max_code) + (ord(word[1]) - self.shift))

    def recvPkt(self, serial):
        while serial.inWaiting() == 0:
            pass

        packet = ''
        for word in serial.readline().split():
            packet += str(self.strToInt(word)) + ';'
            # packet += str(word) + ';'

        packet = packet[:len(packet) - 1] + '\n'

        return packet

    def setSampleRate(self, serial, value):
        serial.write("S " + str(value) + "\n")
        packet = self.recvPkt(serial)

    def setNChannels(self, serial, value):
        serial.write("C " + str(value) + "\n")
        packet = self.recvPkt(serial)

    def setNBoards(self, serial, value):
        serial.write("N " + str(value) + "\n")
        packet = self.recvPkt(serial)
