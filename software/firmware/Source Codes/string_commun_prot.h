/*
 * string_commun_prot.h
 *
 *  Created on: 8 de jan de 2020
 *      Author: asaph
 */

#ifndef STRING_COMMUN_PROT_H_
#define STRING_COMMUN_PROT_H_



// Constants ////////////////////////////////////////////////////////////////////////////////////////////////

#define LENGTH_STRING_STREAMING_BUFFER 9

#define SHIFT 60
#define MAX_CONV 64



// Function Prototypes //////////////////////////////////////////////////////////////////////////////////////

void uintToStr(int index, uint32_t num, char* str);
void clearStr(char *str, int length);
int lengthStr(char* str);
unsigned char compareStr(char* str1, char* str2);
void uartSend(char *str, int length);




#endif /* STRING_COMMUN_PROT_H_ */
