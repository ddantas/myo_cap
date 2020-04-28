# -*- coding: utf-8 -*-

from   SerialPort import SerialPort
from   time   import sleep
import struct


BITS_PER_BYTE = 8

MAX_CODE = 64
SHIFT    = 60

class Board(SerialPort):

    def __init__(self, settings):
    
      
        self.settings = settings
        self.baudrate_ = self.settings.getBaudrate()
        
        # supeclass constructor
        super(Board, self).__init__(self.baudrate_)
        
        # Wait until all the Bytes arrive or the maximum of 5 seconds for the reception.
        self.timeout = 5 # seconds

       
       
    def receive(self):


        pkt_header = self.read(6)
        
        ## Convertes the 2 firsts bytes in op1 into a uint32
        instruction = ( pkt_header[0:2] ).decode()
                
        ## Convertes the 4 bytes in op1 into a uint32
        operand1 =  ( struct.unpack( '>I', pkt_header[2:6]) )[0]


        if (instruction == 'vu') or (instruction == 'me') or (instruction == 'mw') or instruction == 'ms':

            
            if instruction == 'vu':
                
                return operand1

            elif (instruction == 'me') or (instruction == 'mw'):
                
                operand2 = self.read(operand1.value)
                return     operand2.decode()

            elif instruction == 'ms':
                
                operand2 = self.read(operand1.value)
                return     self.decodePkt(operand2)

        elif instruction == 'ok':
            
            return instruction
     
     
    # Receive a packet of Strings having a (2 * number of channels) Chars from the Serial Port.
    # Returns a list with two integer values per channel. 
    def recvStringPkt(self, num_channels):
    
        while self.inWaiting() == 0:
            pass
            
        result = []

        # read from serial port
        packet = self.readline()
        for i in range(num_channels):
        
            pos = i * 2
            result.append( self.strToInt(packet[pos:pos + 2].decode("utf-8") ) )
        print( result )
            
        return result
        
        
    # convert string to int. Used for string transmission
    def strToInt(self, word):
        if (len(word) > 1):
            return int(((ord(word[0]) - SHIFT) * MAX_CODE) + (ord(word[1]) - SHIFT))
        else:
            return 0
 
 
 
    def decodePkt(self, pkt):
    
        return self.settings.getPktSize()


    
    #Commands    
    ## Note: Before call other Commands, Call stop() first.
    
    def start(self):
        
        command = b'ai'
        op      =  0  
        
        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)

        return self.receive()
    

    def stop(self):
        
        command = b'as'
        op      = 0
        
        packet  = struct.pack('>2sI', command, int(op))
        
        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def setSampleRate(self, sample_rate):
        
        command = b'sr'
        op      = sample_rate
        
        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    def setChannelsperBoard(self, channels_per_board):
        
        command = b'sc'
        op      = channels_per_board

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
        
        
    def setNumAcquisBoards(self, num_acquis_boards):
        
        command = b'sb'
        op      = num_acquis_boards

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
        
    
    def setBitsPerSample(self, bits_per_sample):
        
        command = b'ss'
        op      = bits_per_sample

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def setPacketSize(self, packet_size):
        
        command = b'sp'
        op      = packet_size

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def setFucGenFreq(self, func_gen_freq):
        
        command = b'sf'
        op      = func_gen_freq

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    

    def setAdcMode(self):
        
        command = b'fa'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def setSquareWaveMode(self):
        
        command = b'fq'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def setSineWaveMode(self):
        
        command = b'fn'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def setSawtoothWaveMode(self):
        
        command = b'fw'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
            
    
    def getSampleRate(self):
        
        command = b'gr'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def getChannelsperBoard(self):
        
        command = b'gc'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def getNumAcquisBoards(self):
        
        command = b'gb'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def getBitsPerSample(self):
        
        command = b'gs'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def getPacketSize(self):
        
        command = b'gp'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    
    
    def getFucGenFreq(self):
        
        command = b'gf'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
    

    def getStreamingWaveForm(self):
        
        command = b'gw'
        op      = 0

        packet  = struct.pack('>2sI', command, int(op))

        self.write( packet )
        self.reset_input_buffer()
        sleep(0.1)
        
        return self.receive()
        
