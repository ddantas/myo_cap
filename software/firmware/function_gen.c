/*
 * function_gen.c
 *
 */


#include <stdint.h>
#include "function_gen.h"
#include "math.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/uart.h"
#include "driverlib/pin_map.h"
#include "utils/uartstdio.h"
#include "driverlib/interrupt.h"
#include "inc/hw_ints.h"
#include "driverlib/timer.h"
#include "inc/hw_timer.h"

// Variables

enum { Sine_Wave = 0,                                                  // Type of Waveform that can be used by the Function Generator. Sine wave it is the default value.
       Square_Wave  ,
       SawTooth_Wave} wave_form = Sine_Wave;

float pecent_of_period = 0;
float period_Func_Gen_ = 0;

//Function Prototypes

//uint16_t sin_wave_gen(uint32_t sample_number_)     ;
uint16_t square_wave_gen(float pecent_of_period_)  ;
//uint16_t sawtooth_wave_gen(uint32_t sample_number_);


// Function to be called to deliver a Sample of the Function Generator.

uint16_t function_gen(uint8_t wave_form_, uint32_t timestamp_){                            // Transforms the time in miliseconds of the timestamp_ into the percentage of the period of the waveform generated.


    period_Func_Gen_ = SysCtlClockGet() / Default_Func_Gen_Freq;

    pecent_of_period = timestamp_ / period_Func_Gen_;

    switch(wave_form_){

    //case Sine_Wave    : return sin_wave_gen(sample_number);

    case Square_Wave  : return square_wave_gen(pecent_of_period);

    //case SawTooth_Wave: return sawtooth_wave_gen(sample_number);

    default           : return square_wave_gen(pecent_of_period);

    }
}

/*

// Function called by function_gen to Generate a Sample of a Sine Waveform.
// Note 1: M_PI is the Pi value defined in "math.h".
// Note 2: (float)signal_freq conversion is necessary to make the result of the division right because "signal_freq" and "samplerate" both are int type variables.
// Note 3: ( sin(x) + 1) / 2 ) goes from 0 to 1. Than ( 4095 * round( ( sin(x) + 1) / 2 ) ) goes from 0 to 4095.
// Note 4: ( sin(x) + 1) is always a double type, than (sin(x) + 1) / 2) will be a double type too.

uint16_t sin_wave_gen(uint32_t sample_number_)     {                                        // The argument to Sine function it is the sample number inside of a period of the function.

    double sin_argument = sample_number_ * ( (float)signal_freq / samplerate) * 2 * M_PI;   //  The angle of Sine Function will be a integer Multiple of a slice of 2 * Pi.
                                                                                           //  "signal_freq" divided by "samplerate" is the size of the slice. See Note 1 and 2.

    return (uint_16_t) round( Highest_16b_Num * ( (sin( sin_argument ) + 1) / 2) ) ;                 //  Shifts the Sine value by 1 than divide the result by 2  to make the the value
                                                                                           //  goes from 0 to 1. Than multiply the last result by 65535 to make the value range from 0 to 65535.
                                                                                           //  Rounds the 0 to 65535 value to the closest integer. Than converts the result of the conversion
                                                                                           //  to a uint16_t type. See Note 3 and 4.
}


// Function called by function_gen to Generate a Sample of a Square Waveform.
// Note 1: (float)2 conversion is necessary because (samplerate/(float)2)
// Note 2: M_PI is the Pi value defined in "math.h".
 * */

uint16_t square_wave_gen(float pecent_of_period)  {                                          // The argument to Square function it is the sample number inside of a period of the function.

    return (uint16_t) ( Highest_12b_Num * (pecent_of_period < 0.5) );
}


/*

// Function called by function_gen to Generate a Sample of a Sawtooth Waveform.

uint16_t sawtooth_wave_gen(uint32_t sample_number_){                                          // The argument to SawTooth function it is the sample number inside of a period of the function.


    uint16_t sample = 0;
    return sample;

}

*/
