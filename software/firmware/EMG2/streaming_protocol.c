/*
 * streaming_protocol.c
 *
 *  Created on: 16 de jan de 2020
 *      Author: Zero_Desktop
 */

// Includes /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Standard Libraries
#include <stdint.h>
#include <stdbool.h>

// Address and Names for Tiva
#include "inc/hw_memmap.h"

// Drivers for Tiva Hardware
#include "driverlib/uart.h"

// Project Modules
#include "streaming_protocol.h"
#include "tiva_HAL.h"


////////  Pack the samples in the Samples Buffer  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void     pack_samples_buffer(uint16_t* samples_buffer, uint8_t num_acquis_boards , uint8_t num_channels_per_board, uint16_t num_samples_per_channel, uint8_t bits_per_sample_, streaming_buffer* packing_buffer_out_){

        // Variable to have Access as Byte or as Word in the Packing Partial Result.
        uint64_as_uint8  aux_var;
        aux_var.uint64[0] = 0;
        aux_var.uint64[1] = 0;

        // Indexes for go through the Input Buffer, Auxiliary Variable and Output Buffer.
        uint8_t          aux_index    = 0;
        uint16_t         input_index  = 0;
        uint16_t         output_index = 0;

        // Calculates the Number of Samples in the Input Buffer.
        uint16_t         num_samples  = ( num_acquis_boards * num_channels_per_board * num_samples_per_channel );

        // Goes through the Input Buffer Calling the pack_samples Function for Each SAMPLES_STEP(= 8 Samples).
        for( input_index = 0 ; input_index < num_samples ; input_index = (input_index + SAMPLES_STEP) ){


            pack_samples( samples_buffer, input_index, SAMPLES_STEP, bits_per_sample_, aux_var.uint64 );

            // Writes Each Partial Result of the Packing into the Output Buffer.
            // The Catch Up : There is x Bytes, for Each 8 Samples of the x bits.
            for( aux_index = 0 ; aux_index < bits_per_sample_ ; aux_index++ ){

                (*packing_buffer_out_).buff_uint8[output_index] = aux_var.uint8[aux_index];     output_index++;

            }


        }

}

////////  Copy a Streaming Buffer //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void     copy_streaming_buffer (streaming_buffer* in_buffer , uint16_t num_bytes_in_buf, streaming_buffer* out_buffer ){


    uint8_t  index;
    uint16_t num_words        = ( num_bytes_in_buf / 8 );                            // Each Word have 64bits.
    uint16_t restant_bytes    = ( num_bytes_in_buf % 8 );                            // For sizes non multiples of 8 Bytes.

    for(index = 0; index <  num_words     ; index++)      (*in_buffer).buff_uint64[index] = (*out_buffer).buff_uint64[index];
    for(index = 0; index <  restant_bytes ; index++)      (*in_buffer).buff_uint8 [index] = (*out_buffer).buff_uint64[index];

}

////////  Calculates the Number of Samples in the Buffer ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

uint16_t  num_samples_in_buffer  (tiva_status*  tiva_actual_status ){

    return ( ( (*tiva_actual_status).nums_of_acquis_boards ) * ( (*tiva_actual_status).num_channels_per_board ) * ( (*tiva_actual_status).num_samples_per_chn_buf ) ) ;

}


////////  Calculates the Number of Bytes in the Buffer ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

uint16_t  num_bytes_in_buffer  (tiva_status*  tiva_actual_status ){

    return ( ( (*tiva_actual_status).nums_of_acquis_boards ) * ( (*tiva_actual_status).num_channels_per_board ) * ( (*tiva_actual_status).num_samples_per_chn_buf ) * ( (*tiva_actual_status).bits_per_sample ) ) / 8 ;

}


////////  Left Shifts a 16 bit sample as a uint128_t   /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void left_shift_sample_as_uint128(uint16_t sample, uint8_t shift, uint8_t bits_per_Sample_,uint64_t* shifted_sample){

    shifted_sample[0] = sample;                                                                         // High Word
    shifted_sample[0] = shifted_sample[0] << (     8 * sizeof(uint64_t) - bits_per_Sample_);            // Put the Sample as much left as possible.
    shifted_sample[0] = shifted_sample[0] >> ( 2 * 8 * sizeof(uint64_t) - bits_per_Sample_ - shift);    // Shift Right Reverse with bits_per_Sample_ of offset

    shifted_sample[1] = sample;                                                                         //  Low Word
    shifted_sample[1] = shifted_sample[1] << shift;                                                     //  Shift the Low Word to the Left.

}

//////// Pack Samples. Bits_per_sample range: 1-12 bits (except for 9 and 11 bits)  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

uint64_t pack_samples_(uint16_t* samples, unsigned char num_samples, unsigned char bits_per_sample_ ){                      //change the return type to uint64_t* (to receive two uint64_t, high and low)

    uint64_t packed_samples = 0;
    uint8_t  shift_left = ( 8 * sizeof(uint64_t) ) - bits_per_sample_;                                                      // Put the Sample as much left as possible.
    uint8_t  sample_index;


    for(sample_index = 0; sample_index < num_samples; sample_index++){

        packed_samples = packed_samples | ( ( (uint64_t) samples[sample_index] )  << shift_left );
        shift_left = shift_left - sample_index;

    }

    return packed_samples;

}

//////// Pack Samples. Bits_per_sample range: 1-12 bits   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// This Function receives a Buffer with Samples and Returns that samples Packed, Left Justified, in a vector of uint64_t with two places ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void pack_samples(uint16_t* samples, uint16_t start_sample_index, uint8_t num_samples, uint8_t bits_per_sample_,  uint64_t* packed_samples ){

    packed_samples[0] = 0;
    packed_samples[1] = 0;
    uint8_t shift_left = ( 2 * 8 * sizeof(uint64_t) ) - bits_per_sample_;                            // Put the Sample as much left as possible.
    uint8_t sample_index;

    uint64_t shifted_Sample[2];

    for(sample_index = 0; sample_index < num_samples; sample_index++){

        left_shift_sample_as_uint128(samples[ start_sample_index + sample_index ], shift_left, bits_per_sample_, shifted_Sample);

        packed_samples[0] = packed_samples[0] | shifted_Sample[0];
        packed_samples[1] = packed_samples[1] | shifted_Sample[1];

        shift_left = shift_left - sample_index;

    }

}


///////// Send a Packet when there is a Pending Packet. Waits until TX UART Buffer have space to Append a Byte in the Buffer /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void send_stream_packet(streaming_buffer* transmit_buffer_ , uint8_t* state_of_tx_pkt_ , tiva_status* tiva_state_ ){

    if(*state_of_tx_pkt_){                                                    // Checks if "state_of_tx_pkt" is Pending or TRANSMITTED.

        uint16_t num_bytes_to_transmit = num_bytes_in_buffer (tiva_state_);

        (*state_of_tx_pkt_) = TRANSMITTING;                                   // Sets "state_of_tx_pkt" to TRANSMITTING.

        uint8_t byte_index;
        for(byte_index = 0; byte_index <  num_bytes_to_transmit ; byte_index++)      UARTCharPut(UART0_BASE, transmit_buffer_->buff_uint8[byte_index]);

        (*state_of_tx_pkt_) = TRANSMITTED;                                    // Change "state_of_tx_pkt" to TRANSMITTED
    }
}


void clear_streaming_buffer(streaming_buffer* streaming_buffer_, uint16_t num_bytes_in_buf){

    uint8_t  index;
    uint16_t num_words        = ( num_bytes_in_buf / 8 );                            // Each Word have 64bits.
    uint16_t restant_bytes    = ( num_bytes_in_buf % 8 );                            // For sizes non multiples of 8 Bytes.

    for(index = 0; index <  num_words     ; index++)      (*streaming_buffer_).buff_uint64[index] = 0;
    for(index = 0; index <  restant_bytes ; index++)      (*streaming_buffer_).buff_uint8 [index] = 0;

}

void clear_acquisition_buffer(uint16_t* acquisition_buffer_, uint16_t num_samples_in_buf){

    uint8_t  index;

    for(index = 0; index <  num_samples_in_buf; index++)      acquisition_buffer_[index] = 0;

}
