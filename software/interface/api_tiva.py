
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

    def recvPkt(self, len_ch, const_board):
        while self.serial.inWaiting() == 0:
            pass
        result = []

        # read from serial port
        packet = self.serial.readline()
        for i in range(len_ch):
            pos = i * 2
            result.append(round((self.strToInt(packet[pos:pos + 2]) * const_board), 5))
        return result

    def setSampleRate(self, value):
        self.serial.write("sr " + str(value) + "\n")
        packet = self.recvPkt(self.serial)

    def setNChannels(self, value):
        self.serial.write("sc " + str(value) + "\n")
        packet = self.recvPkt(self.serial)

    def setNBoards(self, value):
        self.serial.write("sb " + str(value) + "\n")
        packet = self.recvPkt(self.serial)

    # convert string to int
    def strToInt(self, word):
        if (len(word) > 1):
            return int(((ord(word[0]) - self.shift) * self.max_code) + (ord(word[1]) - self.shift))
        else:
            return 0