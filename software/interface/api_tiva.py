import struct
class ApiTiva():
    def __init__(self, serial):
        # codification parameters
        self.serial = serial
        self.shift = 60
        self.max_code = 64

    def start(self):
        self.serial.write("ai")
    
    def stop(self):
        self.serial.write("as")

    def recvPkt(self, len_ch, const_board):
        while self.serial.inWaiting() == 0:
            pass
        result = []

        # read from serial port
        packet = self.serial.readline()
        for i in range(len_ch):
            pos = i * 2
            result.append(round((self.strToInt(packet[pos:pos + 2])), 5))
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
    
    def setADCmode(self):
        self.serial.write("fa")

    
    def setFrequencyFuncGen(self, value):
        z = struct.pack('>i',int(value))
        self.serial.write("sf" + z)
        #packet = self.recvPkt(self.serial)

    def setFuncGenSquare(self, value):
        self.serial.write("fq")
        #packet = self.recvPkt(self.serial)

    def setFuncGenSawtooth(self, value):
        self.serial.write("fw")
        #packet = self.recvPkt(self.serial)

    def setFuncGenSine(self, value):        
        self.serial.write("fn")
        #self.serial.write(hex((int(value))))
        #packet = self.recvPkt(self.serial)

    def getFrequencyFuncGen(self, value):
        self.serial.write("gf " + str(value) + "\n")
        packet = self.recvPkt(self.serial)
        
    # convert string to int
    def strToInt(self, word):
        if (len(word) > 1):
            return int(((ord(word[0]) - self.shift) * self.max_code) + (ord(word[1]) - self.shift))
        else:
            return 0