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

float pecent_of_period = 0;
float period_Func_Gen_ = 0;

//Function Prototypes

uint16_t sin_wave_gen(float pecent_of_period)     ;
uint16_t square_wave_gen(float pecent_of_period)  ;
uint16_t sawtooth_wave_gen(float pecent_of_period);


// Function to be called to deliver a Sample of the Function Generator.

uint16_t function_gen(uint8_t wave_form_, uint32_t timestamp_, uint32_t func_gen_frequence_){       // Transforms the time in miliseconds of the timestamp_ into the percentage of the period of the waveform generated.


    period_Func_Gen_ = SysCtlClockGet() / func_gen_frequence_;                                      // Calculates the Period of the Function Generator in terms of multiples of the System Period.

    pecent_of_period = timestamp_ / period_Func_Gen_;

    switch(wave_form_){

    case Sine_Wave    : return sin_wave_gen(pecent_of_period);

    case Square_Wave  : return square_wave_gen(pecent_of_period);

    case Sawtooth_Wave: return sawtooth_wave_gen(pecent_of_period);

    default           : return square_wave_gen(pecent_of_period);

    }
}



// Function called by function_gen to Generate a Sample of a Sine Waveform.
// Note 1: M_PI is the Pi value defined in "math.h".
// Note 2: ( sin(x) + 1) / 2 ) goes from 0 to 1. Than ( 4095 * round( ( sin(x) + 1) / 2 ) ) goes from 0 to 4095.
// Note 3: ( sin(x) + 1) is always a double type, than (sin(x) + 1) / 2) will be a double type too.

uint16_t sin_wave_gen(float pecent_of_period_)     {                                       // The argument to Sine function it is the sample number inside of a period of the function.

    double sin_argument = pecent_of_period_ * 2 * M_PI;                                    //  The angle of Sine Function will be a percentage of 2 * Pi.
                                                                                           //  See Note 1.

    return (uint16_t) round( Highest_12b_Num * ( (sin( sin_argument ) + 1) / 2) ) ;        //  Shifts the Sine value by 1 than divide the result by 2  to make the the value
                                                                                           //  goes from 0 to 1. Than multiply the last result by "Highest_12b_Num" to make the value range from 0 to "Highest_12b_Num".
                                                                                           //  Rounds the 0 to "Highest_12b_Num" value to the closest integer. Than converts the result of the conversion
                                                                                           //  to a uint16_t type. See Note 2 and 3.
}


// Function called by function_gen to Generate a Sample of a Square Waveform.

uint16_t square_wave_gen(float pecent_of_period_)  {                                        // The argument to Square function it is the percentage of the period of the waveform generated.

    return (uint16_t) ( Highest_12b_Num * (pecent_of_period_ < 0.5) );                      // If percentage of the period is less than 50%, than the generated value will be "Highest_12b_Num". Otherwise will be 0.
}




// Function called by function_gen to Generate a Sample of a Sawtooth Waveform.

uint16_t sawtooth_wave_gen(float pecent_of_period_){                                       // The argument to SawTooth function it is the percentage of the period of the waveform generated.


    return (uint16_t) ( Highest_12b_Num * pecent_of_period_ );                             // Multiplies the percentage of the period by the "Highest_12b_Num" to create a Positive Ramp that goes from the 0 to the
                                                                                           // "Highest_12b_Num" in a period.

}


