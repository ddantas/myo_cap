/*
 * debug.c
 *
 *  Created on: 8 de jan de 2020
 *      Author: asaph
 *
 *  - Set of Helpful Functions to Test the Tiva and Tiva Applications.
 *
 */

// #include "driverlib/pin_map.h"
// #include "inc/hw_types.h"

#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/uart.h"

//Function to Print a uint32_t variable trough the UART0 Previously Set Up.
void print_uint32 (uint32_t to_be_print)
{
    UARTCharPut(UART0_BASE, to_be_print / (256 * 256 * 256));
    UARTCharPut(UART0_BASE, ( ( to_be_print % ( 256 * 256 * 256 ) ) / ( 256 * 256 ) ) );
    UARTCharPut(UART0_BASE, ( ( to_be_print % ( 256 * 256 ) ) / ( 256 ) ) );
    UARTCharPut(UART0_BASE, to_be_print % 256 );
}


void write_packed_samples_to_buffer(){

}
