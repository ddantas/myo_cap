# -*- coding: utf-8 -*-

import serial
import sys
import glob
import ctypes
import struct
import time
import AuxFunctions as AuxFunc

BITS_PER_BYTE = 8
MAX_CODE = 64
SHIFT    = 60

class Board:

    def __init__(self, settings):
        self.settings = settings
        self.serial = serial.Serial()
        self.serial.baudrate = self.settings.getBaudrate()
        self.serial.timeout = 5

    def testPort(self, port):
        self.serial.port = port
        self.serial.open()
        self.serial.close()

    def listPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux'):
            ports = glob.glob('/dev/ttyACM[0-9]')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                self.openComm(port)
                self.closeComm()
                result.append(port)
            except:
                pass
        return result
    
    def getCommStatus(self):
        return self.serial.is_open

    def openComm(self, port):
        self.closeComm()
        self.serial.port = port
        self.serial.open()

    def closeComm(self):
        if self.getCommStatus():
            self.serial.close()

    def test(self):
        return self.stop() == 'ok'

    def receiveStrPkt(self):
        samples = []
        while self.serial.inWaiting() == 0:
            pass
        packet = self.serial.readline()
        for i in range(self.settings.getTotChannels()):
            pos = i * 2
            samples.append(self.strToInt(packet[pos:pos + 2].decode('utf-8')))
        return samples

    def strToInt(self, word):
        if len(word) > 1:
            return int(((ord(word[0]) - SHIFT) * MAX_CODE) + (ord(word[1]) - SHIFT))
        else:
            return 0

    def receive(self):
        try:
            pkt_header = self.serial.read(6)
            ## Convertes the 2 firsts bytes in op1 into a uint32
            instruction = (pkt_header[0:2]).decode()
            ## Convertes the 4 bytes in op1 into a uint32
            operand1 =  (struct.unpack('>I', pkt_header[2:6]))[0]
            if (instruction == 'vu') or (instruction == 'me') or (instruction == 'mw') or instruction == 'ms':            
                if instruction == 'vu':
                    return operand1
                elif (instruction == 'me') or (instruction == 'mw'):
                    operand2 = self.serial.read(operand1.value)
                    return     operand2.decode()
                elif instruction == 'ms':
                    operand2 = self.serial.read(operand1.value)
                    return     self.decodePkt(operand2)
            elif instruction == 'ok':
                return instruction
        except:
            return None

    def decodePkt(self, pkt):
        return self.settings.getPktSize()

    def write(self, packet):
        try:
            self.serial.write(packet)
            self.serial.reset_input_buffer()
            time.sleep(0.1)
        except:
            AuxFunc.showMessage('Error', 'Capture settings did not apply!\nPlease, connect the board.')

    #Commands    
    ## Note: Before call other Commands, Call stop() first.

    def start(self):
        command = b'ai'
        op =  0  
        packet = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()

    def stop(self):
        command = b'as'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()

    def setSampleRate(self, sample_rate):
        command = b'sr'
        op      = sample_rate
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def setChannelsperBoard(self, channels_per_board):
        command = b'sc'
        op      = channels_per_board
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
        
    def setNumAcquisBoards(self, num_acquis_boards):
        command = b'sb'
        op      = num_acquis_boards
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def setBitsPerSample(self, bits_per_sample):
        command = b'ss'
        op      = bits_per_sample
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def setPacketSize(self, packet_size):
        command = b'sp'
        op      = packet_size
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def setFucGenFreq(self, func_gen_freq):
        command = b'sf'
        op      = func_gen_freq
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()

    def setAdcMode(self):
        command = b'fa'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def setSquareWaveMode(self):
        command = b'fq'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def setSineWaveMode(self):
        command = b'fn'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def setSawtoothWaveMode(self):
        command = b'fw'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
            
    def getSampleRate(self):
        command = b'gr'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def getChannelsperBoard(self):
        command = b'gc'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def getNumAcquisBoards(self):
        command = b'gb'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def getBitsPerSample(self):
        command = b'gs'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()

    def getPacketSize(self):
        command = b'gp'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def getFucGenFreq(self):
        command = b'gf'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()
    
    def getStreamingWaveForm(self):
        command = b'gw'
        op      = 0
        packet  = struct.pack('>2sI', command, int(op))
        self.write(packet)
        return self.receive()