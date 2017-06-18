/*	Library for Stellaris launchpad and compatible devices.
 *
 * 	This library contains several functions for using with a DDS generator
 * 	AD9850 module. All the functions are intended to work with this device
 * 	in SERIAL mode, so you need to connect the parallel pins D0 and D1 to VCC
 * 	and D2 GND, as written in the AD9850 datasheet. For further information
 * 	check the Analog Devices website.
 *
 * 	Don't forget to check the "add dir to #include search path" under
 * 	build>arm compiler>include options AND "Include library file or command
 * 	file as input" on build>arm linker. Link your StellarisWare folder and
 * 	\StellarisWare\driverlib\ccs-cm4f\Debug\driverlib-cm4f.lib respectively.
 *
 * 	Coded by Gonzalo Recio
 */

#ifndef STELLARIS_AD9850_H
	#define STELLARIS_AD9850_H

	//Interchangeable pins. Port D and GPIO pins 0, 1, 2 and 3
	#define W_CLK  GPIO_PIN_0
	#define FQ_UD  GPIO_PIN_1
	#define DATA   GPIO_PIN_2
	#define RESET  GPIO_PIN_3
	#define PORT GPIO_PORTD_BASE
	#define PORT_ENABLE SYSCTL_PERIPH_GPIOD

	//Frequency of your crystal oscillator (CLKIN input pin 9 in datasheet), measured in MHz.
	// This reference frequency must be higher than 1MHz.
	#define XTAL_MHZ 125

	//Relationship value between actual frequency and 32-bit word sent in the serial streaming
	#define FREQ_FACTOR 4294.967295

	//function prototypes
	void AD9850_Init(void);
	void AD9850_Reset(void);
	void AD9850_Osc(double frequency, double phase);
	void AD9850_Sweep_Up(double minFreq, double maxFreq, double inc, int cyclesPerDelay);
	void AD9850_Sweep_Down(double minFreq, double maxFreq, double inc, int cyclesPerDelay);
	void AD9850_Sweep_Loop(double minFreq, double maxFreq, double inc, int cyclesPerDelay);
	void AD9850_PowerDown(void);

#endif
