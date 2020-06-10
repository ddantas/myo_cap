# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:54:41 2020

@author: asaphe
"""

import ctypes
import struct

class Unpacker:
    
    def __init__(self, settings):
        
        #################################################################################
        
        #                                Parameters
        
        #################################################################################
        
        self.settings = settings
        
        # Create a vector type with two uint64 
        self.uint64_array   = ctypes.c_uint64 * 2
        
        # Create a vector with two uint64 for the Input of Unpack Function.  
        
        self.unpack_in      = self.uint64_array(0,0)
        self.unpack_in_ptr  = ctypes.pointer( self.unpack_in )
        
        # List of all Decoded Samples
        self.decoded_pkt = []
        
        # Create a vector with two uint64 for the Output of left_shift_128b Function.
        self.shifted_var     = self.uint64_array(0,0)
        self.shifted_var_ptr = ctypes.pointer( self.shifted_var )
        
        # Create a vector with two uint64 for the Output of right_justifie Function.
        self.justified_var     = self.uint64_array(0,0)
        self.justified_var_ptr = ctypes.pointer( self.justified_var )
        
        # Create the bitmask
        self.bitmask      = self.uint64_array(0,0)
        self.bitmask_ptr  = ctypes.pointer( self.bitmask )
        
        # Create a vector with 8 uint16(Samples) to Store the Unpack Result.  
        self.uint16_array = ctypes.c_int16 * 8
        self.unpack_out   = self.uint16_array(0,0)
        self.unpack_out_ptr  = ctypes.pointer( self.unpack_out )
        
        # Load the bits per sample used        
        self.bits_per_sample = self.settings.getBitsPerSample()


    
    # Left shifts a 16bits variable like one of 128 bits
    #--------------------------------------------------------------------------------
    def left_shift_128b( self, in_var, shift_left , bits_per_sample_, shifted_var_ptr):
    
            shifted_var_ptr.contents[0] = in_var                                                                         # High Word
            shifted_var_ptr.contents[0] = shifted_var_ptr.contents[0] << (     8 * ctypes.sizeof(ctypes.c_int64) - bits_per_sample_)                  # Put the Sample as much left as possible.
            shifted_var_ptr.contents[0] = shifted_var_ptr.contents[0] >> ( 2 * 8 * ctypes.sizeof(ctypes.c_int64) - bits_per_sample_ - shift_left)     # Shift Right Reverse with bits_per_Sample_ of offset
    
            shifted_var_ptr.contents[1] = in_var                                                                         #  Low Word
            shifted_var_ptr.contents[1] = shifted_var_ptr.contents[1] << shift_left                                      #  Shift the Low Word to the Left.
            

    
    
    
    # Right Justifie a 16bits value in a 128bits variable with a previus left shift
    #--------------------------------------------------------------------------------
    def right_justifie( self, in_var, shift_left , bits_per_sample_, justified_var_ptr):
        

        #Processing of the High word of the Input Variable
        #-------------------------------------------------

        #Left Justifie the var and than right shitfs 64 bits by writing the result in the low word.  
        justified_var_ptr.contents[1] = in_var.contents[0] << ( 2 * 8 * ctypes.sizeof(ctypes.c_int64) - bits_per_sample_ - shift_left )

        #Right Shift the Previous result to align it with the Right Justifie result of the low word part. 
        justified_var_ptr.contents[1] = justified_var_ptr.contents[1] >> ( 8 * ctypes.sizeof(ctypes.c_int64) - bits_per_sample_ )



        #Processing of the Low word of the Input Variable
        #-------------------------------------------------

        #Right Justifie the Low word of the Input Variable 
        justified_var_ptr.contents[0] = in_var.contents[1] >> (shift_left)

        

        #Merging the Result of the High and Low Result
        #-------------------------------------------------
        justified_var_ptr.contents[1] = justified_var_ptr.contents[0] | justified_var_ptr.contents[1]

        

    #--------------------------------------------------------------------------------
    
    
    
    # Unpack Samples 
    #--------------------------------------------------------------------------------
        
    def unpack( self, unpack_in_ptr, offset, bits_per_sample_,unpack_out_ptr_):

        #print("Inside the Decode Function")
        #print('----------------------------------------------------------\n')
        
        #Calculates the Initial Shift
        shift_left = ( 2 * 8 * ctypes.sizeof(ctypes.c_int64) - bits_per_sample_)
        
        #Generetes the AND bitmask whith (bits_per_sample_ ) bits
        bitmask_    =  ( 0xFFFF >> ( 16 - bits_per_sample_ ) )
        #print( "bps: " + hex(bits_per_sample_) )
        #print( "Bitmask_: " + format(bitmask_, '#06X') )
                          
        #Iterates to extract 8 Samples
        for sample_number in range(8):
                
              # Left Shifts the bitmask
              self.left_shift_128b( bitmask_ , shift_left, bits_per_sample_, self.bitmask_ptr)

              #print( "Bitmask: 0x " + format(self.bitmask_ptr.contents[0], '#018X')[2:] + ' ' + format(self.bitmask_ptr.contents[1], '#018X')[2:] )
              #print( "Bitmask: " + hex(bitmask_ptr.contents[0]) + hex(bitmask_ptr.contents[1]) )

              # Extracts a Sample from the Input Buffer
              self.shifted_var[0] = self.bitmask_ptr.contents[0] & unpack_in_ptr.contents[0]
              self.shifted_var[1] = self.bitmask_ptr.contents[1] & unpack_in_ptr.contents[1]

              # Right Justifie the Extracted Sample 
              self.right_justifie( self.shifted_var_ptr, shift_left , bits_per_sample_, self.justified_var_ptr)

              # Write the Extracted Sample Into the Output Buffer
              unpack_out_ptr_.contents[sample_number] = self.justified_var_ptr.contents[1]
                            
              self.decoded_pkt.append( int( self.justified_var_ptr.contents[1] ) )
              
              # Update the New Left Shift
              shift_left = shift_left - bits_per_sample_
        # print('\n----------------------------------------------------------\n')
        #print("Outside the Decode Function")    
    
    

    def unpack_pkt(self, packed_pkt):
        
        self.decoded_pkt = []
        
        # Store Number of Samples per Packet in Settings in the future.
        
        # != Number of Iterations         = Number of Samples per Packet / 8 Samples. Optimizing: Number of Iterations = Samples per Packet >> 3
        # Number of Iterations         = Number of Samples per Packet / 8 Samples. Optimizing: Number of Iterations = Samples per Packet >> 3
        # Number of Samples per Packet = Number of Instants * Number of Boards * Number of Channels per Board 
        # Number of Instants           = floor (  Number of Bytes in a Packet / ( Number of Boards * Number of Channels per Board * Number of bits per Sample / 8 bits )  )

        
        self.num_instants = int(  ( 8 * self.settings.getPktSize() ) /   (  self.settings.getNBoards() * self.settings.getChannelsPerBoard() * self.settings.getBitsPerSample() )   )
          
        #num_instants = 1  
        #print('Number of Instants: ' + str(self.num_instants) )
        
        samples_per_pkt = self.num_instants * self.settings.getNBoards() * self.settings.getChannelsPerBoard() 
        #print('Number of Samples per Packet: ' + str(samples_per_pkt) )
        
        
        # Calculate the number of bytes of the payload of packet.
        num_bytes_data = ( samples_per_pkt * self.bits_per_sample ) >> 3
        
        # If there is a fractionary number of Bytes, round to up.
        if( ( samples_per_pkt * self.bits_per_sample ) % 8 ): 
            num_bytes_data =  num_bytes_data + 1
        #print('Number of Bytes of Data: ' + str(num_bytes_data) )
        
          
        
        # Number of Iterations = Number of Samples per Packet / 8 Samples. 
        num_iterations = samples_per_pkt >> 3
        
        # If there is a fractionary number of Iterations, round to up.
        if( samples_per_pkt % 8 ):            
            num_iterations = num_iterations + 1
            
        #print('Number of Iterations: ' + str(num_iterations) )

        
        
        self.bits_per_sample = self.settings.getBitsPerSample()
        #print("Bits per Sample: " + str(self.bits_per_sample) )
        
        
        # Calculate the number of Bytes inside one Iteration.
        if ( num_bytes_data  >= self.bits_per_sample):
            
            num_bytes_per_iteration = self.bits_per_sample 
        else:
            
            num_bytes_per_iteration = num_bytes_data
            
        #print('Number of Bytes per Iteration: ' + str(num_bytes_per_iteration) )
        
        # Init Offset in the Packed Packet
        offset = 0
        
        
        
        for iterator_couter in range( num_iterations ):          
        
            #print('####################################################')
            #print('################## Iteration ' + str(iterator_couter) +' #####################')
            #print('####################################################')
            
            ''' No Use for Now
            # 16 Bytes or More to Process   
            if  ( num_bytes_to_process >= 16 ):
        
                # Load the High Word to Process
                temp_word          = packed_pkt[ offset      : offset +  8                   ]    
                self.unpack_in[0]  = ( struct.unpack( '>Q' ,  temp_word ) )[0] 
            
                # Load the Low Word to Process
                temp_word          = packed_pkt[ offset + 8  : offset + 16                  ]     
                self.unpack_in[1]  = ( struct.unpack( '>Q' ,  temp_word ) )[0] 
            
                # Update the Number of Bytes ti Process
                num_bytes_to_process = num_bytes_to_process - 16 
                
                print('More or Equal to 16 Bytes')
                print("High Word: "  + format(self.unpack_in[0],'#018x') )
                print("Low  Word: "  + format(self.unpack_in[1],'#018x') )
            '''
            
            # Less than 16 and More than 8 Bytes to Process   
            if ( num_bytes_per_iteration >= 8 ):
            
                # Load the High Word to Process
                temp_word          = packed_pkt[ offset      : offset + 8                    ] 
                self.unpack_in[0]  = ( struct.unpack( '>Q' ,  temp_word ) )[0] 
        
                # Load the Low Word to Process and Fill the Rest of Bytes
                temp_word          = packed_pkt[ offset + 8 : offset + num_bytes_per_iteration ]  + (16 - num_bytes_per_iteration ) * b'\x00'
                self.unpack_in[1]  = ( struct.unpack( '>Q' ,  temp_word ) )[0]  
             
                
                #print('More or Equal to 8 Bytes')
                #print("High Word: "  + format(self.unpack_in[0],'#018x') )
                #print("Low  Word: "  + format(self.unpack_in[1],'#018x') )
            
            
            # Less than 8 Bytes to Process   
            else:    
                            
                # Load the High Word to Process and Fill the Rest of Bytes
                temp_word          = packed_pkt[ offset      : offset + num_bytes_per_iteration ] + ( 8 - num_bytes_per_iteration ) * b'\x00'                
                self.unpack_in[0]  = ( struct.unpack( '>Q' ,  temp_word ) )[0] 
                
                # Fill the Rest of Bytes
                temp_word          =  8 * b'\x00'
                self.unpack_in[1]  = ( struct.unpack( '>Q' ,  temp_word ) )[0] 
                
                
                # No need to update "num_bytes_to_process". Last Iteration.
                #print('Less than 8 Bytes')
                #print("High Word: "  + format(self.unpack_in[0],'#018x') )
                #print("Low  Word: "  + format(self.unpack_in[1],'#018x') )
                
            # Call the Unpack Method    
            self.unpack( self.unpack_in_ptr, 0, self.bits_per_sample, self.unpack_out_ptr)
            #print(self.decoded_pkt)
            
            # Update the Offset in the Packed Packet
            offset = offset + num_bytes_per_iteration
            #print('Offset: ' + str(offset))
            
        
            # Update the number of Bytes inside one Iteration.
            if ( (num_bytes_data - offset)  >= self.bits_per_sample):
                
                num_bytes_per_iteration = self.bits_per_sample 
            else:
                
                num_bytes_per_iteration = num_bytes_data - offset

            #print('Number of Bytes per Iteration: ' + str(num_bytes_per_iteration) )
            
        
        # End of for Loop
        
        
          
        return self.decoded_pkt
            
    
    def print_out_buffer_hex(self):

        # Print the Output Buffer as Hexadecimal.
        
        print()
        print("--------------- Output Buffer as Hexadecimal  ---------------------------")
        print()
        
        print("Output(hex)")
        for sample_number in range(8):
             
                print("Sample" + str(sample_number) + ": " + format(self.unpack_out[sample_number],'#06x') )
                
        print()
        
        