/*
 * tiva_HAL.h
 *
 *  Created on: 8 de jan de 2020
 *      Author: asaph
 */

#ifndef TIVA_HAL_H_
#define TIVA_HAL_H_


// Constants ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// Multiplexer Channels

#define MUX_CHANNEL_0                         0  // GPIO_PIN_2 = 0 ; GPIO_PIN_1 = 0
#define MUX_CHANNEL_1                         2  // GPIO_PIN_2 = 0 ; GPIO_PIN_1 = 1
#define MUX_CHANNEL_2                         4  // GPIO_PIN_2 = 1 ; GPIO_PIN_1 = 0
#define MUX_CHANNEL_3                         6  // GPIO_PIN_2 = 1 ; GPIO_PIN_1 = 1


// Acquisition Mode

#define ADC_ACQUISITION                       0
#define FUNC_GEN_ACQUISITION                  1


// Type of Transmission;

#define UNPACKED                              0
#define PACKED                                1


// Defaults Values for Tiva Parameters

#define DEFAULT_NUM_ACQUISITION_BOARDS        1
#define DEFAULT_NUM_CHANNELS_PER_BOARD        4
#define DEFAULT_NUM_SAMPLES_PER_CHANNEL      64  // Choose Number of Samples multiple of 64. Each Call to the Packing Function Needs a place with 64 bits of size to store the result.
#define DEFAULT_BITS_PER_SAMPLE              12


// Maximum Values for Tiva Parameters
//------------------------------------------------------

#define NUM_MAX_ACQUISITION_BOARDS            4
#define NUM_MAX_CHANNELS_PER_BOARD            4
#define NUM_MAX_SAMPLES_PER_CHANNEL          64
#define NUM_MAX_BITS_PER_SAMPLE              12

// For 4 Boards ; 4 Channels ; 64 Samples ; 12 bits:
// Two Acquisition Buffers occupy 4K of RAM
// Two Streaming   Buffers occupy 3K of RAM

//------------------------------------------------------
#define DEFAULT_SAMPLERATE                 2000

#define DEFAULT_BAUDRATE                 921600


// Structures /////////////////////////////////////////////////////////////////////////////


typedef struct {

    uint32_t timestamp               ;
    uint32_t period_Func_Gen         ;        // Byte[x-x] ; Size =   bytes ; Byte Offset =
    uint8_t  wave_form               ;
    uint32_t func_gen_frequence      ;

    uint8_t  nums_of_acquis_boards   ;
    uint8_t  num_channels_per_board  ;
    uint16_t num_samples_per_chn_buf ;
    uint8_t  bits_per_sample         ;

    uint16_t samplerate              ;

    uint32_t baudrate                ;

} tiva_status;




// Function Prototypes ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


void     tiva_actual_state_init( tiva_status* tiva_actual_status );
void     configureADC(void);
void     configureSelectPins();
void     configureUART(int baudrate);
void     configureTimer(tiva_status* tiva_actual_status);

uint16_t adc_sample_acquisition();


// Macros ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#define set_mux_channel(index_channel)  GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1 | GPIO_PIN_2, mux_channel[index_channel])                                                    // Change the value of the Mux Selection Pins.

#define NUM_MAX_SAMPLES_BUFFER          (uint16_t) (   NUM_MAX_ACQUISITION_BOARDS * NUM_MAX_CHANNELS_PER_BOARD * NUM_MAX_SAMPLES_PER_CHANNEL                                )
#define NUM_MAX_BYTES_BUFFER            (uint16_t) ( ( NUM_MAX_ACQUISITION_BOARDS * NUM_MAX_CHANNELS_PER_BOARD * NUM_MAX_SAMPLES_PER_CHANNEL * NUM_MAX_BITS_PER_SAMPLE) / 8 )


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


#endif /* TIVA_HAL_H_ */
