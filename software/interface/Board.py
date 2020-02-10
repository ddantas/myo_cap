# -*- coding: utf-8 -*-

from serial import Serial
import sys
import glob
import ctypes
import struct

BITS_PER_BYTE = 8

class Board:

    def __init__(self, settings):
        self.settings = settings
        self.serial = Serial()
        self.serial.baudrate = self.settings.getBaudrate()
        self.serial.timeout = 5

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
    
    def getCommStatus(self):
        return self.serial.is_open

    def openComm(self, port):
        self.serial.port = port
        self.serial.open()
        

    def receive(self):
        while self.serial.inWaiting() == False:
            pass

        pkt_header = self.serial.read(6)
        instruction = pkt_header[0] + pkt_header[1]

        op1 = pkt_header[2] << ctypes.sizeof(ctypes.c_ubyte) * self.byteOffset(3)
        op1 = op1 | pkt_header[3] << ctypes.sizeof(ctypes.c_ubyte) * self.byteOffset(2)
        op1 = op1 | pkt_header[4] << ctypes.sizeof(ctypes.c_ubyte) * self.byteOffset(1)
        op1 = op1 | pkt_header[5] * self.byteOffset(0)

        if (instruction == 'vu') and (instruction == 'me') and (instruction == 'mw') and instruction == 'ms':
            op1 = ctypes.c_uint32(op1)

            if instruction == 'vu':
                return op1.value

            elif (instruction == 'me') or (instruction == 'mw'):
                op2 = self.serial.read(op1.value)
                return op2

            elif instruction == 'ms':
                op2 = self.serial.read(op1.value)
                return self.decodePkt(op2)

        elif instruction == 'ok':
            return instruction

    def byteOffset(self, pos):
        return BITS_PER_BYTE * pos

    # IMPLEMENT HERE DECODE
    def decodePkt(self, pkt):
        return self.settings.getPktSize()

    """def receive(self):
        while self.serial.inWaiting() == 0:
            pass

        samples = []

        packet = self.serial.readline()
        for i in range(self.settings.getChannelsPerBoard()):
            pos = i * 2
            samples.append(self.strToInt(packet[pos:pos + 2]))

        return samples

    def strToInt(self, word):
        if len(word) > 1:
            return int(((ord(word[0]) - 60) * 64) + (ord(word[1]) - 60))
        else:
            return 0"""
    
    #Commands    
    
    def start(self):
        
        command = 'ai'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    

    def stop(self):
        
        command = 'as'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def setSampleRate(self, sample_rate):
        
        command = 'sr'
        op      = struct.pack('<I', int(sample_rate))

        self.serial.write( command + op)

        return self.receive()
    
    def setChannelsperBoard(self, channels_per_board):
        
        command = 'sc'
        op      = struct.pack('<I', int(channels_per_board))

        self.serial.write( command + op)
        
        return self.receive()
        
        
    def setNumAcquisBoards(self, num_acquis_boards):
        
        command = 'sb'
        op      = struct.pack('<I', int(num_acquis_boards))

        self.serial.write( command + op)
        
        return self.receive()
        
    
    def setBitsPerSample(self, bits_per_sample):
        
        command = 'ss'
        op      = struct.pack('<I', int(bits_per_sample))

        self.serial.write( command + op)

        return self.receive()
    
    
    def setPacketSize(self, packet_size):
        
        command = 'sp'
        op      = struct.pack('<I', int(packet_size))

        self.serial.write( command + op)

        return self.receive()
    
    
    def setFucGenFreq(self, func_gen_freq):
        
        command = 'sf'
        op      = struct.pack('<I', int(func_gen_freq))

        self.serial.write( command + op)

        return self.receive()
    

    def setADCMode(self):
        
        command = 'fa'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def setSquareWaveMode(self):
        
        command = 'fq'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def setSineWaveMode(self):
        
        command = 'fn'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def setSawtoothWaveMode(self):
        
        command = 'fw'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def getSampleRate(self):
        
        command = 'gr'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def getChannelsperBoard(self):
        
        command = 'gc'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def getNumAcquisBoards(self):
        
        command = 'gb'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def getBitsPerSample(self):
        
        command = 'gs'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def getPacketSize(self):
        
        command = 'gp'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    
    
    def getFucGenFreq(self):
        
        command = 'gf'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()
    

    def getStreamingWaveForm(self):
        
        command = 'gw'
        op      = struct.pack('<I', int(0))

        self.serial.write( command + op)

        return self.receive()