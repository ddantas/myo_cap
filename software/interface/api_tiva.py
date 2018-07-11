
class ApiTiva():
    def __init__(self, serial):
        # codification parameters
        self.serial = serial
        self.shift = 60
        self.max_code = 64

    def start(self):
        self.serial.write("start\n")
    
    def stop(self):
        self.serial.write("stop\n")

    def recvPkt(self):
        while self.serial.inWaiting() == 0:
            pass
        packet = ''
        for word in self.serial.readline().split():
            packet += str(self.strToInt(word)) + ' '
        packet = packet[:len(packet) - 1] + '\n'
        return packet

    def setSampleRate(self, value):
        self.serial.write("S " + str(value) + "\n")
        packet = self.recvPkt(self.serial)

    def setNChannels(self, value):
        self.serial.write("C " + str(value) + "\n")
        packet = self.recvPkt(self.serial)

    def setNBoards(self, value):
        self.serial.write("N " + str(value) + "\n")
        packet = self.recvPkt(self.serial)

    def strToInt(self, word):
        return int(((ord(word[0]) - self.shift) * self.max_code) + (ord(word[1]) - self.shift))
