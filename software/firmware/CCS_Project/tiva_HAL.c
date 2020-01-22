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

        tiva_actual_status->period_Func_Gen          = SysCtlClockGet() / Default_Func_Gen_Freq;  // Calculates the Period of the Function Generator in terms of multiples of the System Period;   // change always that a set frequence is received.
        tiva_actual_status->func_gen_frequence       = Default_Func_Gen_Freq                   ;  // Starts with the Default Function Generator Frequence.
        tiva_actual_status->timestamp                = 0                                       ;  // Starts from the Begining of the Wave Form.
        tiva_actual_status->wave_form                = ADC_Acquisition                         ;  // Starts Transmitting from the ADC.
        tiva_actual_status->bits_per_sample          = DEFAULT_BITS_PER_SAMPLE                 ;  // Sets the Default bits per Sample.
        tiva_actual_status->num_channels_per_board   = DEFAULT_NUM_CHANNELS_PER_BOARD          ;
        tiva_actual_status->nums_of_acquis_boards    = DEFAULT_NUM_ACQUISITION_BOARDS          ;
        tiva_actual_status->samplerate               = DEFAULT_SAMPLERATE                      ;
        tiva_actual_status->num_samples_per_chn_buf  = DEFAULT_NUM_SAMPLES_PER_CHANNEL         ;
        tiva_actual_status->baudrate                 = DEFAULT_BAUDRATE                        ;
}


// Configuration Functions ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void configureADC(void)
{
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0);

    GPIOPinTypeADC(GPIO_PORTD_BASE, GPIO_PIN_0);

    ADCReferenceSet(ADC0_BASE, ADC_REF_INT);

    ADCSequenceConfigure(ADC0_BASE, 3, ADC_TRIGGER_PROCESSOR, 0);
    ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH7 | ADC_CTL_END | ADC_CTL_IE);
    ADCSequenceEnable(ADC0_BASE, 3);

    ADCIntClear(ADC0_BASE, 3);
}


void configureSelectPins()
{
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE, GPIO_PIN_1 | GPIO_PIN_2);
    GPIOPadConfigSet(GPIO_PORTE_BASE, GPIO_PIN_1 | GPIO_PIN_2, GPIO_STRENGTH_8MA, GPIO_PIN_TYPE_OD);

    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1 | GPIO_PIN_2, 0);
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
    (*tiva_actual_status).period_Func_Gen = SysCtlClockGet() / (*tiva_actual_status).func_gen_frequence;  // Calculates the Period of the Function Generator in terms of multiples of the System Period.
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


