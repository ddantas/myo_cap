/*
 * streaming_prot.h
 *
 *  Created on: 16 de jan de 2020
 *      Author: Zero_Desktop
 */

// Includes /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Standard Libraries
#include <stdint.h>

// Address and Names for Tiva
#include "tiva_HAL.h"

#ifndef STREAMING_PROTOCOL_H_
#define STREAMING_PROTOCOL_H_

// Constants  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// State of Transmit Packet

#define TRANSMITTED       0
#define PENDING           1
#define TRANSMITTING      2

// State of Packing Process

#define PROCESSED         0
#define PENDING           1
#define PROCESSING        2

#define SAMPLES_STEP      8

// Unions  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

typedef union{

    uint64_t buff_uint64[ NUM_MAX_BYTES_BUFFER / 8  ] ;
    uint8_t  buff_uint8 [ NUM_MAX_BYTES_BUFFER      ] ;

} streaming_buffer;

typedef union{

    uint64_t uint64[ 2];
    uint8_t  uint8 [16];

} uint64_as_uint8;


// Function Prototypes ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void     pack_samples_buffer      (volatile uint16_t*          samples_buffer     , uint8_t           num_acquis_boards      , uint8_t           num_channels_per_board        , uint16_t     num_samples_per_channel, uint8_t     bits_per_sample_, volatile streaming_buffer* packing_buffer_out_ );
uint64_t pack_samples_            (volatile uint16_t*          samples            , unsigned char     num_samples            , unsigned char     bits_per_sample_                                                                                                                                   );
void     pack_samples             (volatile uint16_t*          samples            , uint16_t          start_sample_index     , uint8_t           num_samples                   , uint8_t      bits_per_sample_       , uint64_t*   packed_samples                                                   );
void     copy_streaming_buffer    (streaming_buffer*           in_buffer          , uint16_t          num_bytes_in_buf       , streaming_buffer* out_buffer                                                                                                                                         );
void     send_stream_packet       (volatile streaming_buffer*  transmit_buffer_   , volatile uint8_t* state_of_tx_pkt_       , tiva_status*      tiva_state_                                                                                                                                        );
uint16_t num_samples_in_buffer    (tiva_status*                tiva_actual_status                                                                                                                                                                                                                   );
uint16_t num_bytes_in_buffer      (tiva_status*                tiva_actual_status                                                                                                                                                                                                                   );
void     clear_streaming_buffer   (streaming_buffer*           streaming_buffer_  , uint16_t          num_bytes_in_buf                                                                                                                                                                              );
void     clear_acquisition_buffer (uint16_t*                   acquisition_buffer_, uint16_t          num_samples_in_buf                                                                                                                                                                            );

// Macros /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#define  SIZE_IN_BYTE__BUFFER  (uint16_t) (  * NUM_MAX_CHANNELS_PER_BOARD * NUM_MAX_SAMPLES_PER_CHANNEL * NUM_MAX_BITS_PER_SAMPLE )


#endif /* STREAMING_PROTOCOL_H_ */
