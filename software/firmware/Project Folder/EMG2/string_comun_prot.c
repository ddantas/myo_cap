/*
 * string_comun_prot.c
 *
 *  Created on: 8 de jan de 2020
 *      Author: asaph
 */


#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/uart.h"
#include "string_commun_prot.h"


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


