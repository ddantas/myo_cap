#include <stdbool.h>
#include <stdint.h>
#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"

#include "STELLARIS_AD9850.h"

/* Starts AD9850 operation changing its value to "all zeros".
 * Refreshes previous status from the microcontroller.
 * */
void AD9850_Init(void){
	GPIOPinWrite(PORT, W_CLK | FQ_UD | DATA | RESET, 0x00);
}

/* Reset operation for the AD9850. This function must be called before using AD9850_Osc
 * first time in the execution (check page 12 on datasheet)
 * */
void AD9850_Reset(void){
	GPIOPinWrite(PORT, W_CLK, 0x00);
	GPIOPinWrite(PORT, W_CLK, W_CLK);
	GPIOPinWrite(PORT, W_CLK, 0x00);

	GPIOPinWrite(PORT, RESET, 0x00);
	GPIOPinWrite(PORT, RESET, RESET);
	GPIOPinWrite(PORT, RESET, 0x00);

	GPIOPinWrite(PORT, FQ_UD, 0x00);
	GPIOPinWrite(PORT, FQ_UD, FQ_UD);
	GPIOPinWrite(PORT, FQ_UD, 0x00);

	AD9850_Osc(0, 0);

}

/* Sets the DDS sine and square oscillator to the detailed "frequency" and "phase" variables.
 * "frequency" will be turned into a 32 bit word, so the frequency will have a resolution of 0.0291 Hz
 * with a 125 MHz reference clock. "phase" will be a 5 bit word instead so the resolution is
 * 11.5 degrees, or pi/32 radians.
 */
void AD9850_Osc(double frequency, double phase){
	int i;
	long y;

	y = (long) frequency * FREQ_FACTOR / XTAL_MHZ;
	while(phase > 360)
		phase -= 360;
	long z = phase / 11.5;

	//Frequency 32-bit word
	for (i = 0; i < 32; i++){
		if((y >> i) & 0x01)
			GPIOPinWrite(PORT, DATA , DATA);
		else
			GPIOPinWrite(PORT, DATA , 0x00);
		GPIOPinWrite(PORT, W_CLK ,W_CLK);
		GPIOPinWrite(PORT, W_CLK ,0x00);
	}

	//control bit #1, control bit #2 and Power off, all to low
	GPIOPinWrite(PORT, DATA , 0x00);
	GPIOPinWrite(PORT, W_CLK ,W_CLK);
	GPIOPinWrite(PORT, W_CLK ,0x00);
	GPIOPinWrite(PORT, W_CLK ,W_CLK);
	GPIOPinWrite(PORT, W_CLK ,0x00);
	GPIOPinWrite(PORT, W_CLK ,W_CLK);
	GPIOPinWrite(PORT, W_CLK ,0x00);

	//phase 5-bit word
	for (i = 0; i < 5; i++){
		if((z >> i) & 0x01)
			GPIOPinWrite(PORT, DATA , DATA);
		else
			GPIOPinWrite(PORT, DATA , 0x00);
		GPIOPinWrite(PORT, W_CLK ,W_CLK);
		GPIOPinWrite(PORT, W_CLK ,0x00);
	}


	GPIOPinWrite(PORT, FQ_UD ,FQ_UD);
	GPIOPinWrite(PORT, FQ_UD ,0x00);
}


/* Enables power down mode. This method is used for a quick "all outputs" disable.
 * The effect is the same as AD9850_Osc(0,0), but it takes less clock cycles
 */
void AD9850_PowerDown(void){
	int PDword = 0x04;
	int i;
	GPIOPinWrite(PORT, FQ_UD ,FQ_UD);
	GPIOPinWrite(PORT, FQ_UD ,0x00);

	for (i = 0; i < 8; i++){
		if((PDword >> i) & 0x01)
			GPIOPinWrite(PORT, DATA , DATA);
		else
			GPIOPinWrite(PORT, DATA , 0x00);
		GPIOPinWrite(PORT, W_CLK ,W_CLK);
		GPIOPinWrite(PORT, W_CLK ,0x00);
	}

	GPIOPinWrite(PORT, FQ_UD ,FQ_UD);
	GPIOPinWrite(PORT, FQ_UD ,0x00);

}


/* Performs a frequency sweep increased in "inc"Hz steps. The frequency order is from low to high
 * and resets to the lower frequency when maximum frequency is reached.
 */
void AD9850_Sweep_Up(double minFreq, double maxFreq, double inc, int cyclesPerDelay){
	double f = minFreq;
	while (1){
		AD9850_Osc(f, 0);
		f += inc;
		if (f > maxFreq)
			f = minFreq;
		SysCtlDelay(cyclesPerDelay);
	}
}

/* Performs a frequency sweep decreased in "inc"Hz steps. The frequency order is from high to low
 * and resets to the higher frequency when minimum frequency is reached.
 */
void AD9850_Sweep_Down(double minFreq, double maxFreq, double inc, int cyclesPerDelay){
	double f = maxFreq;
	while (1){
		AD9850_Osc(f, 0);
		f -= inc;
		if (f < minFreq)
			f = maxFreq;
		SysCtlDelay(cyclesPerDelay);
	}
}

/* Performs a frequency sweep increased in "inc"Hz steps. The frequency order is from low to high,
 * but it changes to from high to low when the maximum frequency is reached and so on.
 */
void AD9850_Sweep_Loop(double minFreq, double maxFreq, double inc, int cyclesPerDelay){
	double f = minFreq;
	while (1){
		AD9850_Osc(f, 0);
		f += inc;
		if (f > maxFreq || f<minFreq)
			inc =- inc;
		SysCtlDelay(cyclesPerDelay);
	}
}
