/*
 * comunication_protocol.c
 *
 *  Created on: 9 de dez de 2019
 *      Author: Lar00
 */

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

#include "function_gen.h"           // New module
#include "comunication_protocol.h"  // New module
#include "tiva_HAL.h"

// Prototypes

void start_trasmission ();
void acknowledgment    ();
void not_acknowledgment();
void set_func_gen_frequence( uint32_t frequence, tiva_status *tiva_actual_state);
void set_sample_rate       (tiva_status*  tiva_actual_status, int sample_rate  );
void set_number_of_channels(tiva_status*  tiva_actual_status, int num_channels );
void set_number_of_acquis_boards (tiva_status*  tiva_actual_status, int num_acquis_boards );
void set_number_of_bytes_in_packet (tiva_status*  tiva_actual_status, int num_bytes_in_pkt );
void set_bits_per_sample (tiva_status*  tiva_actual_status, int bits_per_sample );
void get_sample_rate (tiva_status*  tiva_actual_status );
void get_number_of_channels (tiva_status*  tiva_actual_status );
void get_number_of_boards (tiva_status*  tiva_actual_status );
void get_number_of_bytes_in_packet (tiva_status*  tiva_actual_status );
void get_bits_per_sample (tiva_status*  tiva_actual_status );

void command_handler(comunication_packet *pkt_received, tiva_status *tiva_actual_state){


    switch(pkt_received->uint32_param_pkt.command){                                // Checks the command in the received packet

        // Flow Control Commands
        case START_TRANSMISSION         :    start_trasmission();                                                                             acknowledgment();      break;

        case STOP_TRANSMISSION          :    stop_trasmission();                                                                              acknowledgment();      break;


        // Set Parameters of the Transmission

        case SET_SAMPLE_RATE           :    set_sample_rate (tiva_actual_state, pkt_received->uint32_param_pkt.uint32_operand);               acknowledgment();      break;

        case SET_NUMBER_CHANNELS       :    set_number_of_channels (tiva_actual_state, pkt_received->uint32_param_pkt.uint32_operand);        acknowledgment();      break;

        case SET_NUMBER_BOARDS         :    set_number_of_acquis_boards (tiva_actual_state, pkt_received->uint32_param_pkt.uint32_operand);   acknowledgment();      break;

        case SET_NUMBER_BYTES_IN_PACKET:    set_number_of_bytes_in_packet (tiva_actual_state, pkt_received->uint32_param_pkt.uint32_operand); acknowledgment();      break;

        case SET_BITS_PER_SAMPLE       :    set_bits_per_sample (tiva_actual_state, pkt_received->uint32_param_pkt.uint32_operand);           acknowledgment();      break;


        // Set Acquisition Mode

        case SET_ADC_ACQUISITION       :    tiva_actual_state->wave_form = ADC_Acquisition  ;                                                 acknowledgment();      break;


        // Get Parameters of the Transmission

        case GET_SAMPLE_RATE           :    get_sample_rate (tiva_actual_state);                                                               acknowledgment();      break;

        case GET_NUMBER_CHANNELS       :    get_number_of_channels (tiva_actual_state);                                                        acknowledgment();      break;

        case GET_NUMBER_BOARDS         :    get_number_of_boards (tiva_actual_state);                                                          acknowledgment();      break;

        case GET_NUMBER_BYTES_IN_PACKET:    get_number_of_bytes_in_packet (tiva_actual_state);                                                 acknowledgment();      break;

        case GET_BITS_PER_SAMPLE       :    get_bits_per_sample (tiva_actual_state);                                                           acknowledgment();      break;


        // Acknowledgment by the Interface

        case ACK                       :                                                                                                                              break;

        case NAK                       :                                                                                                                              break;


        // Function Generator

        case SET_FUNC_GEN_FREQUENCE    :       {
                                               tiva_actual_state->func_gen_frequence  =  pkt_received->uint32_param_pkt.uint32_operand ;
                                               tiva_actual_state->period_Func_Gen      =  SysCtlClockGet() / tiva_actual_state->func_gen_frequence;      // Calculates the Period of the Function Generator in terms of multiples of the System Period.
                                               TimerLoadSet(TIMER1_BASE, TIMER_A, tiva_actual_state->period_Func_Gen - 1);                               // Load the Period of the Signal to be generated by the Function Generator.
                                               acknowledgment()   ;   }


                                                                                                                                                                      break;

        case SET_FUNC_GEN_SQUARE_WAVE  :       tiva_actual_state->wave_form = Square_Wave  ;                                                   acknowledgment();      break;

        case SET_FUNC_GEN_SAWTOOTH_WAVE:       tiva_actual_state->wave_form = Sawtooth_Wave;                                                   acknowledgment();      break;

        case SET_FUNC_GEN_SIN_WAVE     :       tiva_actual_state->wave_form = Sine_Wave    ;                                                   acknowledgment();      break;


        case GET_FUNC_GEN_WAVE_FORM    :                                                                                                       acknowledgment();      break;


        default:                               not_acknowledgment();

    }

}


// Sends a uint32 Parameter Packet

void send_packet(comunication_packet *pkt_to_send){

        // Sends Command

        UARTCharPut(UART0_BASE, pkt_to_send->bytes[ OFFSET_COMMAND  + ( SIZE_COMMAND - 1 ) ] );
        UARTCharPut(UART0_BASE, pkt_to_send->bytes[ OFFSET_COMMAND  + ( SIZE_COMMAND - 2 ) ] );

        // Sends uint32 Parameter

        UARTCharPut(UART0_BASE, pkt_to_send->bytes[ OFFSET_OPERAND  + ( SIZE_OPERAND - 1 ) ] );
        UARTCharPut(UART0_BASE, pkt_to_send->bytes[ OFFSET_OPERAND  + ( SIZE_OPERAND - 2 ) ] );
        UARTCharPut(UART0_BASE, pkt_to_send->bytes[ OFFSET_OPERAND  + ( SIZE_OPERAND - 3 ) ] );
        UARTCharPut(UART0_BASE, pkt_to_send->bytes[ OFFSET_OPERAND  + ( SIZE_OPERAND - 4 ) ] );

}


void recieve_packet(comunication_packet* pkt_to_be_received){

        uint8_t buffer_in[LENGTH_BUFFER_IN];

        // Reads the Serial Buffer
        int i = 0;    while(UARTCharsAvail(UART0_BASE)) buffer_in[i++] = (char)UARTCharGetNonBlocking(UART0_BASE);


        // Receives a Packet

        // Receives a Command
        pkt_to_be_received->bytes[ OFFSET_COMMAND  + ( SIZE_COMMAND - 1 ) ]  =  buffer_in[0] ;
        pkt_to_be_received->bytes[ OFFSET_COMMAND  + ( SIZE_COMMAND - 2 ) ]  =  buffer_in[1] ;

        // Receives uint32 or float32 Parameter
        pkt_to_be_received->bytes[ OFFSET_OPERAND  + ( SIZE_OPERAND - 1 ) ]  =  buffer_in[2] ;
        pkt_to_be_received->bytes[ OFFSET_OPERAND  + ( SIZE_OPERAND - 2 ) ]  =  buffer_in[3] ;
        pkt_to_be_received->bytes[ OFFSET_OPERAND  + ( SIZE_OPERAND - 3 ) ]  =  buffer_in[4] ;
        pkt_to_be_received->bytes[ OFFSET_OPERAND  + ( SIZE_OPERAND - 4 ) ]  =  buffer_in[5] ;

}




void start_trasmission(){

    TimerEnable(TIMER0_BASE, TIMER_A);
    IntEnable(INT_TIMER0A);

}

void stop_trasmission(){

    TimerDisable(TIMER0_BASE, TIMER_A);
    IntDisable(INT_TIMER0A);
    GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_1 | GPIO_PIN_2, 0);

}

void acknowledgment(){

    comunication_packet pkt_send;
    pkt_send.uint32_param_pkt.command        = ACK   ;
    pkt_send.uint32_param_pkt.uint32_operand = 0x0000;
    send_packet(&pkt_send);

}


void not_acknowledgment(){

    comunication_packet pkt_send;
    pkt_send.uint32_param_pkt.command        = NAK   ;
    pkt_send.uint32_param_pkt.uint32_operand = 0x0000;
    send_packet(&pkt_send);

}

void set_func_gen_frequence( uint32_t frequence, tiva_status *tiva_actual_state_){

    tiva_actual_state_->func_gen_frequence  =  frequence                   ;
    tiva_actual_state_->period_Func_Gen     =  SysCtlClockGet() / frequence;              // Calculates the Period of the Function Generator in terms of multiples of the System Period.
    TimerLoadSet(TIMER1_BASE, TIMER_A, tiva_actual_state_->period_Func_Gen - 1);          // Load the Period of the Signal to be generated by the Function Generator.

}


void set_sample_rate (tiva_status*  tiva_actual_status, int sample_rate ){

   (*tiva_actual_status).samplerate =  sample_rate;

   int samplerate_mux = ( (*tiva_actual_status).samplerate ) * ( (*tiva_actual_status).num_channels_per_board );
   int period = SysCtlClockGet() / samplerate_mux;

   TimerLoadSet(TIMER0_BASE, TIMER_A, period - 1);

}

void set_number_of_channels (tiva_status*  tiva_actual_status, int num_channels ){

   (*tiva_actual_status).num_channels_per_board =  num_channels;


}

void set_number_of_acquis_boards (tiva_status*  tiva_actual_status, int num_acquis_boards ){

   (*tiva_actual_status).nums_of_acquis_boards =  num_acquis_boards;


}

void set_number_of_bytes_in_packet (tiva_status*  tiva_actual_status, int num_bytes_in_pkt ){

   // Create the var
   //(*tiva_actual_status). =  num_bytes_in_pkt;

}


void set_bits_per_sample (tiva_status*  tiva_actual_status, int bits_per_sample ){

   (*tiva_actual_status).bits_per_sample =  bits_per_sample;


}


void get_sample_rate (tiva_status*  tiva_actual_status ){

   comunication_packet pkt_send;
   pkt_send.uint32_param_pkt.command        = INT_VALUE;
   pkt_send.uint32_param_pkt.uint32_operand = (*tiva_actual_status).samplerate;
   send_packet(&pkt_send);

}


void get_number_of_channels (tiva_status*  tiva_actual_status ){

   comunication_packet pkt_send;
   pkt_send.uint32_param_pkt.command        = INT_VALUE;
   pkt_send.uint32_param_pkt.uint32_operand = (*tiva_actual_status).num_channels_per_board;
   send_packet(&pkt_send);

}


void get_number_of_boards (tiva_status*  tiva_actual_status ){

   comunication_packet pkt_send;
   pkt_send.uint32_param_pkt.command        = INT_VALUE;
   pkt_send.uint32_param_pkt.uint32_operand = (*tiva_actual_status).nums_of_acquis_boards;
   send_packet(&pkt_send);

}


void get_number_of_bytes_in_packet (tiva_status*  tiva_actual_status ){

   /* Create the var
   comunication_packet pkt_send;
   pkt_send.uint32_param_pkt.command        = INT_VALUE;
   pkt_send.uint32_param_pkt.uint32_operand = (*tiva_actual_status).;
   send_packet(&pkt_send);
   */

}


void get_bits_per_sample (tiva_status*  tiva_actual_status ){

   comunication_packet pkt_send;
   pkt_send.uint32_param_pkt.command        = INT_VALUE;
   pkt_send.uint32_param_pkt.uint32_operand = (*tiva_actual_status).bits_per_sample;
   send_packet(&pkt_send);

}
