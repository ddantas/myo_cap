/*
 * tiva_HAL.c
 *
 *  Created on: 8 de jan de 2020
 *      Author: asaph
 */

// Includes /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Standard Libraries
#include <stdint.h>
#include <stdbool.h>

// Address and Names for Tiva
#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"

// Drivers for Tiva Hardware
#include "driverlib/uart.h"
#include "driverlib/pin_map.h"
#include "driverlib/interrupt.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/adc.h"
#include "driverlib/timer.h"
#include "driverlib/sysctl.h"

// Project Modules
#include "function_gen.h"
#include "tiva_HAL.h"



// Structures  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


void tiva_actual_state_init( tiva_status* tiva_actual_status )
{

        tiva_actual_status->period_Func_Gen          = SysCtlClockGet() / Default_Func_Gen_Freq;  // Calculates the Period of the Function Generator in terms of multiples of the System Period;   // change always that a set frequency is received.
        tiva_actual_status->func_gen_frequency       = Default_Func_Gen_Freq                   ;  // Starts with the Default Function Generator Frequency.
        tiva_actual_status->timestamp                = 0                                       ;  // Starts from the Beginning of the Wave Form.
        tiva_actual_status->wave_form                = ADC_Acquisition                         ;  // Starts Transmitting from the ADC.


        tiva_actual_status->bits_per_sample          = DEFAULT_BITS_PER_SAMPLE                 ;  // Sets the Default bits per Sample.
        tiva_actual_status->num_channels_per_board   = DEFAULT_NUM_CHANNELS_PER_BOARD          ;
        tiva_actual_status->nums_of_acquis_boards    = DEFAULT_NUM_ACQUISITION_BOARDS          ;
        tiva_actual_status->samplerate               = DEFAULT_SAMPLERATE                      ;
        tiva_actual_status->num_samples_per_chn_buf  = DEFAULT_NUM_SAMPLES_PER_CHANNEL         ;
        tiva_actual_status->num_bytes_in_packet      = DEFAULT_NUM_BYTES_IN_PACKET             ;
        tiva_actual_status->baudrate                 = DEFAULT_BAUDRATE                        ;
        tiva_actual_status->type_of_transmission     = DEFAULT_TYPE_OF_TRANSMISSION            ;
}


// Configuration Functions ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void configureADC(void)
{
    // Enable the peripherals
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0);

    // Configures the GPIO pins used in the ADC
    GPIOPinTypeADC(GPIO_PORTD_BASE, GPIO_PIN_3);
    GPIOPinTypeADC(GPIO_PORTE_BASE, GPIO_PIN_1);

    // Regular ADC tiva pins for A0 and A1.
    #ifndef USE_ADC_ALTERNATIVE_PINS
    GPIOPinTypeADC(GPIO_PORTE_BASE, GPIO_PIN_2);
    GPIOPinTypeADC(GPIO_PORTE_BASE, GPIO_PIN_3);
    #endif

    // Alternative ADC tiva pins for A0 and A1.
    #ifdef USE_ADC_ALTERNATIVE_PINS
    GPIOPinTypeADC(GPIO_PORTD_BASE, GPIO_PIN_1);    // Alternative ADC tiva pin PD1
    GPIOPinTypeADC(GPIO_PORTD_BASE, GPIO_PIN_2);    // Alternative ADC tiva pin PD2
    #endif

    // Choose the reference voltage for the ADC
    ADCReferenceSet(ADC0_BASE, ADC_REF_INT);

    // Configures the Sample Sequencer 3 of the ADC0
    ADCSequenceConfigure(ADC0_BASE, 3, ADC_TRIGGER_PROCESSOR, 0);

    // Sets the channel for the Sample Sequencer 3 of the ADC0 of the Tiva
    adc_set_acq_board(ACQUISITION_BOARD_0);

    // Enables the Sample Sequencer 3 of the ADC0
    ADCSequenceEnable(ADC0_BASE, 3);

    // Clear the interruption flag
    ADCIntClear(ADC0_BASE, 3);
}


void configureSelectPins()
{
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    //                        Myocap Bus Pins: ENABLE       S0           S1
    GPIOPinTypeGPIOOutput(GPIO_PORTB_BASE, GPIO_PIN_5 | GPIO_PIN_0 | GPIO_PIN_1);
    GPIOPadConfigSet(GPIO_PORTB_BASE,  GPIO_PIN_5 | GPIO_PIN_0 | GPIO_PIN_1, GPIO_STRENGTH_8MA, GPIO_PIN_TYPE_OD);

    GPIOPinWrite(GPIO_PORTB_BASE, GPIO_PIN_5 | GPIO_PIN_0 | GPIO_PIN_1, 0);
}


void configureUART(int baudrate)
{
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);
    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    UARTConfigSetExpClk(UART0_BASE, SysCtlClockGet(), baudrate, (UART_CONFIG_WLEN_8 | UART_CONFIG_STOP_ONE | UART_CONFIG_PAR_NONE));
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);
    IntPrioritySet(INT_UART0, 0);
    IntEnable(INT_UART0);
}

void configureTimer(tiva_status* tiva_actual_status)
{
    uint32_t period;

    // Timer 0A Configuration
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

    int samplerate_mux = ( (*tiva_actual_status).samplerate ) * ( (*tiva_actual_status).num_channels_per_board );
    period = SysCtlClockGet() / samplerate_mux;

    TimerLoadSet(TIMER0_BASE, TIMER_A, period - 1);
    TimerControlTrigger(TIMER0_BASE, TIMER_A, false);                                                               // Make the Timer 0 NOT to trigger a Capture in ADC.

    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    TimerEnable(TIMER0_BASE, TIMER_A);

    // Timer 1A Configuration. Timer used to generate time reference to the Function Generator

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);                                                         // Activate the Timer1 Peripheral
    TimerConfigure(TIMER1_BASE, TIMER_CFG_PERIODIC);                                                      // Configures the Timer 1 as Counting Down Timer with a 32bits Register (Full Width)
    (*tiva_actual_status).period_Func_Gen = SysCtlClockGet() / (*tiva_actual_status).func_gen_frequency;  // Calculates the Period of the Function Generator in terms of multiples of the System Period.
    TimerLoadSet(TIMER1_BASE, TIMER_A, (*tiva_actual_status).period_Func_Gen - 1);                        // Load the Period of the Signal to be generated by the Function Generator.
    TimerControlTrigger(TIMER1_BASE, TIMER_A, false);                                                     // Make the Timer 1 NOT to trigger a Capture in ADC.
    TimerEnable(TIMER1_BASE, TIMER_A);                                                                    // Enable the Timer1.

}

uint16_t adc_sample_acquisition(){

    uint32_t acquired_sample_ = 0;
    ADCProcessorTrigger(ADC0_BASE, 3);
    while(!ADCIntStatus(ADC0_BASE, 3, false));
    ADCIntClear(ADC0_BASE, 3);
    ADCSequenceDataGet(ADC0_BASE, 3, &acquired_sample_);
    return (uint16_t)acquired_sample_;

}

void adc_set_acq_board(uint8_t acquisition_board){


    switch(acquisition_board){


        // Sets the ADC0 channel for the Sample Sequencer 3 in the Tiva

        case ACQUISITION_BOARD_0       :    //  Myocap  Pin: A0 . Tiva Pin: PE3 . ADC Channel 0
                                            #ifndef USE_ADC_ALTERNATIVE_PINS
                                            ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH0 | ADC_CTL_END | ADC_CTL_IE);          break;
                                            #endif

                                            //  Myocap  Pin: jumper . Tiva Pin: PD2 . ADC Channel 5. A0 -> PD2
                                            #ifdef USE_ADC_ALTERNATIVE_PINS
                                            ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH5 | ADC_CTL_END | ADC_CTL_IE);          break;  // Alternative ADC tiva pin PD2
                                            #endif


        case ACQUISITION_BOARD_1       :    //  Myocap  Pin: A1 . Tiva Pin: PE2 . ADC Channel 1
                                            #ifndef USE_ADC_ALTERNATIVE_PINS
                                            ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH1 | ADC_CTL_END | ADC_CTL_IE);          break;
                                            #endif

                                            //  Myocap  Pin: jumper . Tiva Pin: PD1 . ADC Channel 6. A1 -> PD1
                                            #ifdef USE_ADC_ALTERNATIVE_PINS
                                            ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH6 | ADC_CTL_END | ADC_CTL_IE);          break;  // Alternative ADC tiva pin PD1
                                            #endif


        case ACQUISITION_BOARD_2       :    //  Myocap  Pin: A2 . Tiva Pin: PE1 . ADC Channel 2
                                            ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH2 | ADC_CTL_END | ADC_CTL_IE);          break;


        case ACQUISITION_BOARD_3       :    //  Myocap  Pin: A3 . Tiva Pin: PD3 . ADC Channel 4
                                            ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH4 | ADC_CTL_END | ADC_CTL_IE);          break;


        default                        :    //  Board not Recognized
                                                                                                                                        break;

    }


}


