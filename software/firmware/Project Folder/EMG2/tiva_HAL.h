/*
 * tiva_HAL.h
 *
 *  Created on: 8 de jan de 2020
 *      Author: asaph
 */

#ifndef TIVA_HAL_H_
#define TIVA_HAL_H_


// Constants ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Preprocessor

// Uncomment the next line to use alternative ADC pins
// #define USE_ADC_ALTERNATIVE_PINS                // Uses PD1, PD2, PD3 and PE1 rather than PD3, PE1, PE2 and PE3 for ADC pins.

// Multiplexer Channels

#define MUX_CHANNEL_0                         0  // GPIO_PIN_0 = 0 ; GPIO_PIN_5 = 0
#define MUX_CHANNEL_1                GPIO_PIN_5  // GPIO_PIN_0 = 0 ; GPIO_PIN_5 = 1
#define MUX_CHANNEL_2                GPIO_PIN_0  // GPIO_PIN_0 = 1 ; GPIO_PIN_5 = 0
#define MUX_CHANNEL_3   GPIO_PIN_5 | GPIO_PIN_0  // GPIO_PIN_0 = 1 ; GPIO_PIN_5 = 1


// Acquisition Boards

#define ACQUISITION_BOARD_0                   0  // Myocap  Pin: A0 . Tiva Pin: PE3 . ADC Channel 0
#define ACQUISITION_BOARD_1                   1  // Myocap  Pin: A1 . Tiva Pin: PE2 . ADC Channel 1
#define ACQUISITION_BOARD_2                   2  // Myocap  Pin: A2 . Tiva Pin: PE1 . ADC Channel 2
#define ACQUISITION_BOARD_3                   3  // Myocap  Pin: A3 . Tiva Pin: PD3 . ADC Channel 4



// Wave Forms Modes

#define ADC_Acquisition                       0  // ADC Acquisition Mode.
#define Sine_Wave                             1  // Type of Waveform that can be used by the Function Generator.
#define Square_Wave                           2  // Type of Waveform that can be used by the Function Generator.
#define Sawtooth_Wave                         3  // Type of Waveform that can be used by the Function Generator.


// Type of Transmission;

#define UNPACKED                              0
#define PACKED                                1


// Defaults Values for Tiva Parameters

#define DEFAULT_NUM_ACQUISITION_BOARDS        1
#define DEFAULT_NUM_CHANNELS_PER_BOARD        4
#define DEFAULT_NUM_SAMPLES_PER_CHANNEL       1  // Choose Number of Samples multiple of 64. Each Call to the Packing Function Needs a place with 64 bits of size to store the result.
#define DEFAULT_BITS_PER_SAMPLE               5
#define DEFAULT_SAMPLERATE                 1000
#define DEFAULT_NUM_BYTES_IN_PACKET          16

#define DEFAULT_BAUDRATE                 921600
#define DEFAULT_TYPE_OF_TRANSMISSION     PACKED

//------------------------------------------------------
// Maximum Values for Tiva Parameters
//------------------------------------------------------


#define NUM_MAX_ACQUISITION_BOARDS            4
#define NUM_MAX_CHANNELS_PER_BOARD            6
#define NUM_MAX_SAMPLES_PER_CHANNEL         128  // Maximum Number of Instants. Considering the Use of:  4 Acquisitions Boards; 4 Channels per Board; 12 bits per Sample.
#define NUM_MAX_BITS_PER_SAMPLE              12
#define NUM_MAX_NUM_BYTES_IN_PACKET        3072  // Considering the Use of:  4 Acquisitions Boards; 4 Channels per Board; 12 bits per Sample. Less will be available if conditions different of the case 2 are used.
#define ADC_MAX_SAMPLING_RATE           1000000  // 1MHz. The Limit of Sampling Rate that can be achieve by using only One Channel.
#define LENGTH_MAX_STRING_STREAM_BUFFER (NUM_MAX_ACQUISITION_BOARDS * NUM_MAX_CHANNELS_PER_BOARD) * 2


// Case 1:
// For 4 Boards ; 4 Channels ; 192 Samples ; 12 bits:
// Two Acquisition Buffers occupy 12K of RAM
// Two Streaming   Buffers occupy  9K of RAM

// Case 2:
// For 4 Boards ; 4 Channels ; 128 Samples ; 12 bits:
// Two Acquisition Buffers occupy 8K of RAM
// Two Streaming   Buffers occupy 6K of RAM

// Case 3:
// For 4 Boards ; 4 Channels ; 64 Samples ; 12 bits:
// Two Acquisition Buffers occupy 4K of RAM
// Two Streaming   Buffers occupy 3K of RAM

//------------------------------------------------------
// Minimum Values for Tiva Parameters
//------------------------------------------------------

#define NUM_MIN_ACQUISITION_BOARDS            1
#define NUM_MIN_CHANNELS_PER_BOARD            1
#define NUM_MIN_SAMPLES_PER_CHANNEL           1
#define NUM_MIN_BITS_PER_SAMPLE               1
#define ADC_MIN_SAMPLING_RATE                 1

//------------------------------------------------------



// Structures /////////////////////////////////////////////////////////////////////////////


typedef struct {

    uint8_t  nums_of_acquis_boards   ;
    uint8_t  num_channels_per_board  ;
    uint16_t num_samples_per_chn_buf ;
    uint8_t  bits_per_sample         ;
    uint16_t samplerate              ;
    uint16_t num_bytes_in_packet     ;

    uint32_t timestamp               ;
    uint32_t period_Func_Gen         ;
    uint8_t  wave_form               ;
    uint32_t func_gen_frequency      ;

    uint32_t baudrate                ;
    uint8_t  type_of_transmission    ;

} tiva_status;




// Function Prototypes ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


void     tiva_actual_state_init( tiva_status* tiva_actual_status );
void     configureADC(void);
void     configureSelectPins();
void     configureUART(int baudrate);
void     configureTimer(tiva_status* tiva_actual_status);
void     adc_set_acq_board(uint8_t acquisition_board);
uint16_t adc_sample_acquisition();

// Macros ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


                                                   // Change the value of the Mux Selection Pins.
// Change the value of the Mux Selection Pins.
#define set_mux_channel(channel)  GPIOPinWrite(GPIO_PORTB_BASE, GPIO_PIN_0 | GPIO_PIN_5, channel)

#define NUM_MAX_SAMPLES_BUFFER          (uint16_t) (   NUM_MAX_ACQUISITION_BOARDS * NUM_MAX_CHANNELS_PER_BOARD * NUM_MAX_SAMPLES_PER_CHANNEL                                )
#define NUM_MAX_BYTES_BUFFER            (uint16_t) ( ( NUM_MAX_ACQUISITION_BOARDS * NUM_MAX_CHANNELS_PER_BOARD * NUM_MAX_SAMPLES_PER_CHANNEL * NUM_MAX_BITS_PER_SAMPLE) / 8 )

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#endif /* TIVA_HAL_H_ */
