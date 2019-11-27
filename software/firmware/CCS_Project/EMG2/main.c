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
#include "driverlib/adc.h"
#include "function_gen.h" // New module


#define LENGTH_DATA 9
#define LENGTH_CMDIN 30
#define LENGTH_CMDOUT 50
#define SHIFT 60
#define MAX_CONV 64
#define START "start\n"
#define STOP "stop\n"


int num_channels = 4, index_channel = 0, samplerate = 2000;
char cmd_in[LENGTH_CMDIN], cmd_out[LENGTH_CMDOUT], data[LENGTH_DATA];
uint32_t adc_values[1];
uint8_t channels[] = {0, GPIO_PIN_1, GPIO_PIN_2, GPIO_PIN_1 | GPIO_PIN_2};

uint32_t period_Func_Gen;
enum { ADC_ACQUISITION = 0, FUNC_GEN_ACQUISITION } acquition_mode = FUNC_GEN_ACQUISITION;                                                // Mode of Acquisition of the Samples.
uint32_t timestamp = 0;

// Function Generator Variables

uint8_t  wave_form = Sawtooth_Wave;
uint32_t func_gen_frequence = Default_Func_Gen_Freq;

//Function to Print a uint32_t variable trough the UART0 Previously Set Up.
void print_uint32 (uint32_t to_be_print)
{
    UARTCharPut(UART0_BASE, to_be_print / (256 * 256 * 256));
    UARTCharPut(UART0_BASE, ( ( to_be_print % ( 256 * 256 * 256 ) ) / ( 256 * 256 ) ) );
    UARTCharPut(UART0_BASE, ( ( to_be_print % ( 256 * 256 ) ) / ( 256 ) ) );
    UARTCharPut(UART0_BASE, to_be_print % 256 );
}

void uintToStr(int index, uint32_t num, char* str)
{
    int pos = index * 2;
    str[pos] = (num / MAX_CONV) + SHIFT;
    str[pos + 1] = (num % MAX_CONV) + SHIFT;
}

void clearStr(char *str, int length)
{
    int i;
    for(i = 0; i < length; i++) str[i] = ' ';
}

int lengthStr(char* str)
{
    int i = 0;
    while(str[i] != '\n') i++;
    return i + 1;
}

unsigned char compareStr(char* str1, char* str2)
{
    int i = 0;
    int length_str1 = lengthStr(str1);
    int length_str2 = lengthStr(str2);

    if(length_str1 == length_str2)
        while(str1[i] != '\n')
        {
            if(str1[i] != str2[i]) return 0;
            i++;
        }
    else return 0;
    return 1;
}

void uartSend(char *str, int length)
{
    while(length--) UARTCharPut(UART0_BASE, *str++);
}

void timer0AInterrupt(void)
{

    TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);


    if(acquition_mode == ADC_ACQUISITION){

        ADCProcessorTrigger(ADC0_BASE, 3);
        while(!ADCIntStatus(ADC0_BASE, 3, false));
        ADCIntClear(ADC0_BASE, 3);
        ADCSequenceDataGet(ADC0_BASE, 3, adc_values);
    }

    if(acquition_mode == FUNC_GEN_ACQUISITION){

        timestamp = ( period_Func_Gen - TimerValueGet(TIMER1_BASE, TIMER_A) );
        adc_values[0] = function_gen(wave_form, timestamp, func_gen_frequence);

    }


    uintToStr(index_channel, adc_values[0], data);
    index_channel++;
    if(index_channel == num_channels)
    {
        index_channel = 0;
        data[LENGTH_DATA - 1] = '\n';
        uartSend(data, LENGTH_DATA);
    }
    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1 | GPIO_PIN_2, channels[index_channel]);


}

void uart0Interrupt(void)
{
    UARTIntClear(UART0_BASE, UART_INT_RX | UART_INT_RT);

    int i = 0;

    while(UARTCharsAvail(UART0_BASE)) cmd_in[i++] = (char)UARTCharGetNonBlocking(UART0_BASE);

    if(compareStr(cmd_in, START))
    {
        TimerEnable(TIMER0_BASE, TIMER_A);
        IntEnable(INT_TIMER0A);
    }
    else if(compareStr(cmd_in, STOP))
    {
        TimerDisable(TIMER0_BASE, TIMER_A);
        IntDisable(INT_TIMER0A);
        GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1 | GPIO_PIN_2, channels[0]);
    }
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

void configureTimer(float samplerate)
{
    uint32_t period;

    // Timer 0A Configuration
    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

    period = SysCtlClockGet() / samplerate;

    TimerLoadSet(TIMER0_BASE, TIMER_A, period - 1);
    TimerControlTrigger(TIMER0_BASE, TIMER_A, false);   // Make the Timer 0 NOT to trigger a Capture in ADC.

    TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    TimerEnable(TIMER0_BASE, TIMER_A);

    // Timer 1A Configuration. Timer used to generate time reference to the Function Generator

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER1);               // Activate the Timer1 Peripheral
    TimerConfigure(TIMER1_BASE, TIMER_CFG_PERIODIC);            // Configures the Timer 1 as Counting Down Timer with a 32bits Register (Full Width)
    period_Func_Gen = SysCtlClockGet() / Default_Func_Gen_Freq; // Calculates the Period of the Function Generator in terms of multiples of the System Period.
    TimerLoadSet(TIMER1_BASE, TIMER_A, period_Func_Gen - 1);    // Load the Period of the Signal to be generated by the Function Generator.
    TimerControlTrigger(TIMER1_BASE, TIMER_A, false);           // Make the Timer 1 NOT to trigger a Capture in ADC.
    TimerEnable(TIMER1_BASE, TIMER_A);                          // Enable the Timer1.

}

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

    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1 | GPIO_PIN_2, channels[0]);
}

void configurations()
{
    int samplerate_mux = samplerate * num_channels;
    int baudrate = 921600;//115200;

    SysCtlClockSet(SYSCTL_SYSDIV_5 | SYSCTL_USE_PLL | SYSCTL_XTAL_16MHZ | SYSCTL_OSC_MAIN);
    IntMasterEnable();

    configureUART(baudrate);
    configureTimer(samplerate_mux);

    configureSelectPins();
    configureADC();
    clearStr(data, LENGTH_DATA);
}

void main(void)
{
    configurations();

    //TimerEnable(TIMER0_BASE, TIMER_A);
    //IntEnable(INT_TIMER0A);

    while(1);
}
