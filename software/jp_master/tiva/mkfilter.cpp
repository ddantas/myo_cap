
//Tem que colocar .cpp pq se colocar como c, compila como c e tem q ser como cpp
//Esta funcionando perfeitamente os filtros, só deu uma pequena alteração nos valores
//troquei o tamanho do vetor MAXPZ para 256 para tentar aliviar a memória na placa tiva
//aliviou mas pegou 97 %
//a função esta calculando o filtro com o valor de entrada adicionado
//Para a função printf funcionar, o Heap size para alocacao dinamica tem que ser 512 ou mais

//Testando um novo método, passa-se o filtro, a entrada é lida pelo adc e calculada ponto por ponto
//não é necessário esperar carregar todos os pontos.
//Tempo real

#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "inc/hw_gpio.h"
#include "inc/hw_sysctl.h"
#include "inc/hw_ints.h"
#include "inc/hw_nvic.h"
#include "inc/hw_uart.h"

#include "driverlib/adc.h"
#include "driverlib/debug.h"
#include "driverlib/fpu.h"
#include "driverlib/gpio.h"
#include "driverlib/rom.h"
#include "driverlib/sysctl.h"
#include "driverlib/pin_map.h"
#include "driverlib/uart.h"
#include "driverlib/interrupt.h"
#include "driverlib/timer.h"

#include "utils/uartstdio.h"

#include "mkfilter.h"
#include "complex.h"

#include "STELLARIS_AD9850.h"

#define tamanho_vetor 42 //(2 * order +1)*2 o tamanho maximo de order 10

uint16_t cont;
char texto[50]; //Texto recebido pela UART
uint16_t flag; // Flag que indica o recebimento de uma requisição de filtro válida
uint16_t flagEntrada; // Flag que indica o recebimento de uma entrada
uint16_t flagInterrupcao; // Flag que indica a entrada da interrupcao
static uint16_t ativaRecebimento; // Flag que ativa o recebimento da entrada de valores
int nEntrada; //contador de elementos da entrada

char bufferRequisicao[50]; //armazenar as partes da requisicao
bool parte1;
bool parte2;
bool parte3;
bool lp_hp;
bool bp_bs;

bool flag_gerador;
bool flag_freq_amostragem;

//////////////////////////////AD9850////////////////////////////////////////
int freq;
char vetFreq[20];




////////////////////////////////ADC////////
uint32_t pui32ADC0Value[1];
double doubleADC0Value[1];
volatile uint32_t leitura;

double freq_amostragem;
char vetFreq_amostragem[20];
///////////////////////////entrada no dev////////////

 double entrada_dev[2];

//*****************************************Delay******************

void delayMs(uint32_t ui32Ms) {

	// 1 clock cycle = 1 / SysCtlClockGet() second
	// 1 SysCtlDelay = 3 clock cycle = 3 / SysCtlClockGet() second
	// 1 second = SysCtlClockGet() / 3
	// 0.001 second = 1 ms = SysCtlClockGet() / 3 / 1000

	SysCtlDelay(ui32Ms * (SysCtlClockGet() / (3 * 1000)));
}

void delayUs(uint32_t ui32Us) {
	SysCtlDelay(ui32Us * (SysCtlClockGet() / 3 / 1000000));
}

//****************************************parte da tiva

void
InitConsole(void)
{

    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);

    GPIOPinConfigure(GPIO_PA0_U0RX);
    GPIOPinConfigure(GPIO_PA1_U0TX);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);

    UARTClockSourceSet(UART0_BASE, UART_CLOCK_PIOSC);

    GPIOPinTypeUART(GPIO_PORTA_BASE, GPIO_PIN_0 | GPIO_PIN_1);

    UARTStdioConfig(0, 115200, 16000000);
}




//////////////////////////////////////////////////////////////
int f_be = 0, f_bu = 0, f_ch = 0;
int f_lp = 0, f_hp = 0, f_bp = 0, f_bs = 0, f_ap = 0;
double alpha, alpha2;
static int order;

struct pzrep
  {
	Complex poles[MAXPZ], zeros[MAXPZ];
    int numpoles, numzeros;
  };

static pzrep splane, zplane;


static double raw_alpha1, raw_alpha2;
static Complex dc_gain, fc_gain, hf_gain;
static double warped_alpha1, warped_alpha2, chebrip;
static uint polemask = 0;
static double xcoeffs[MAXPZ+1], ycoeffs[MAXPZ+1];
static Complex gain;
static double final_gain;

static C_complex bessel_poles[] =
  { /* table produced by /usr/fisher/bessel --	N.B. only one member of each C.Conj. pair is listed */
    { -1.00000000000e+00, 0.00000000000e+00}, { -1.10160133059e+00, 6.36009824757e-01},
    { -1.32267579991e+00, 0.00000000000e+00}, { -1.04740916101e+00, 9.99264436281e-01},
    { -1.37006783055e+00, 4.10249717494e-01}, { -9.95208764350e-01, 1.25710573945e+00},
    { -1.50231627145e+00, 0.00000000000e+00}, { -1.38087732586e+00, 7.17909587627e-01},
    { -9.57676548563e-01, 1.47112432073e+00}, { -1.57149040362e+00, 3.20896374221e-01},
    { -1.38185809760e+00, 9.71471890712e-01}, { -9.30656522947e-01, 1.66186326894e+00},
    { -1.68436817927e+00, 0.00000000000e+00}, { -1.61203876622e+00, 5.89244506931e-01},
    { -1.37890321680e+00, 1.19156677780e+00}, { -9.09867780623e-01, 1.83645135304e+00},
    { -1.75740840040e+00, 2.72867575103e-01}, { -1.63693941813e+00, 8.22795625139e-01},
    { -1.37384121764e+00, 1.38835657588e+00}, { -8.92869718847e-01, 1.99832584364e+00},
    { -1.85660050123e+00, 0.00000000000e+00}, { -1.80717053496e+00, 5.12383730575e-01},
    { -1.65239648458e+00, 1.03138956698e+00}, { -1.36758830979e+00, 1.56773371224e+00},
    { -8.78399276161e-01, 2.14980052431e+00}, { -1.92761969145e+00, 2.41623471082e-01},
    { -1.84219624443e+00, 7.27257597722e-01}, { -1.66181024140e+00, 1.22110021857e+00},
    { -1.36069227838e+00, 1.73350574267e+00}, { -8.65756901707e-01, 2.29260483098e+00},
  };


static void compute_s(), choosepole(Complex), prewarp(), normalize();
static Complex blt(Complex);
static void compute_z_blt();

static void expandpoly(), expand(Complex[], int, Complex[]), multin(Complex, int, Complex[]);
static void printresults();
static void printcoeffs(char*, int, double[]);

//////////////////////////////////parte do gencode
static int margin, nxfacs, npoles_gen, nzeros_gen;
static double pbgain;
static enum { none, ansic, xyc, fifi } language;

static void usage();

static void compileclear(double*,double*);
static void comp_fir(double*), comp_iir(double*,double*), pr_shiftdown(const char*, int);
static void pr_xcoeffs(double*), pr_ycoeffs(double*), pr_xpart(const char*,double *), prxfac(double), pr_ypart(const char*,double*), prnl();
static void giveup(const char*, int = 0, int = 0);
static void formaterror(int);

////////////////////////////////////////parte filtro

static double coef_filtro[(tamanho_vetor+1)/2]; //coeficiente da parte x.

static double total_partx, total_party, incognita_filtro;
static double xv[tamanho_vetor+1], yv[tamanho_vetor+1]; //inicializo com zero? global?
static double next_input, next_output; //global?
static int parar, segunda_vez;

static void filtro();
static double parte_x();
static void prxfac_filtro(double, int);
static double parte_y();
////////////////////////////parte dtoa////////////////////////////

#define MAX_NUMBER_STRING_SIZE 32
static double PRECISION = 0.00000000000001;
static char s[MAX_NUMBER_STRING_SIZE];
char resultado_dtoa[MAX_NUMBER_STRING_SIZE];

char * dtoa(char*, double);
//static char resultadoFinal[tamanho_vetor+1];
//////////////////////////////////////////////////////////////

void calcula_coef() {

	polemask = 0;
	//printf("polemask %u \n", polemask);
	if (alpha!= 0){
		raw_alpha1 = alpha;
		if((f_bs == 1) || (f_bp == 1) ) raw_alpha2 = alpha2;
		else
			raw_alpha2 = raw_alpha1;
	}
	//Equivalente a função setdefaults()
	polemask = ~0;
	//printf("polemask %u \n", polemask);
	if(!(f_bp == 1 | f_bs == 1)) raw_alpha2 = raw_alpha1;
	compute_s();
	prewarp();
	normalize();
	compute_z_blt();
	expandpoly();
	printresults();
	gencode(final_gain,zplane.numzeros,xcoeffs,zplane.numpoles,ycoeffs);
}

static void compute_s() /* compute S-plane poles for prototype LP filter */
  {
	splane.numpoles = 0;
    if (f_be)
      { /* Bessel filter */
		int p = (order*order)/4; /* ptr into table */
		if (order & 1) choosepole(bessel_poles[p++]);
		for (int i = 0; i < order/2; i++)
		{   choosepole(bessel_poles[p]);
			choosepole(cconj(bessel_poles[p]));
			p++;
		}
      }

    if ( f_bu |f_ch)
      { /* Butterworth filter */
		for (int i = 0; i < 2*order; i++)
		  { double theta = (order & 1) ? (i*PI) / order : ((i+0.5)*PI) / order;
			choosepole(expj(theta));
		  }
      }

    if (f_ch)
      { /* modify for Chebyshev (p. 136 DeFatta et al.) */
		if (chebrip >= 0.0)
		  { printf("mkfilter: Chebyshev ripple is %g dB; must be .lt. 0.0\n", chebrip);
			exit(1);
		  }
		double rip = pow(10.0, -chebrip / 10.0);
		double eps = sqrt(rip - 1.0);
		//double y = asinh(1.0 / eps) / (double) order;
		double y = log((1.0 / eps) + sqrt(1.0 + sqr((1.0 / eps)))) / (double) order;
		if (y <= 0.0)
		  { printf( "mkfilter: bug: Chebyshev y=%g; must be .gt. 0.0\n", y);
			exit(1);
		  }
		for (int i = 0; i < splane.numpoles; i++)
		  {
			splane.poles[i].re *= sinh(y);
			splane.poles[i].im *= cosh(y);
		  }
      }
  }

static void choosepole(complex z)
{

	if (z.re < 0.0)
      {

		if (polemask & 1) splane.poles[splane.numpoles++] = z;
      	polemask >>= 1;
      }
}

static void prewarp()
  { /* for bilinear transform, perform pre-warp on alpha values */

    warped_alpha1 = tan(PI * raw_alpha1) / PI;
	warped_alpha2 = tan(PI * raw_alpha2) / PI;

  }

static void normalize()		/* called for trad, not for -Re or -Pi */
{

	double w1 = TWOPI * warped_alpha1;
    double w2 = TWOPI * warped_alpha2;
    /* transform prototype into appropriate filter type (lp/hp/bp/bs) */
    	if(f_lp)
		  {

			  for (int i = 0; i < splane.numpoles; i++) splane.poles[i] = splane.poles[i] * w1;

			  splane.numzeros = 0;

		  }

    	else if(f_hp)
		  {
			int i;
			for (i=0; i < splane.numpoles; i++) splane.poles[i] = w1 / splane.poles[i];
			for (i=0; i < splane.numpoles; i++) splane.zeros[i] = 0.0;	 /* also N zeros at (0,0) */
			splane.numzeros = splane.numpoles;

		  }

    	else if(f_bp)
		  {
			double w0 = sqrt(w1*w2), bw = w2-w1; int i;
			for (i=0; i < splane.numpoles; i++)
			  {
				complex hba = 0.5 * (splane.poles[i] * bw);
				complex temp = csqrt(1.0 - sqr(w0 / hba));
				splane.poles[i] = hba * (1.0 + temp);
				splane.poles[splane.numpoles+i] = hba * (1.0 - temp);
			  }
			for (i=0; i < splane.numpoles; i++) splane.zeros[i] = 0.0;	 /* also N zeros at (0,0) */
			splane.numzeros = splane.numpoles;
			splane.numpoles *= 2;

		  }

    	else if (f_bs)
		  {
			double w0 = sqrt(w1*w2), bw = w2-w1; int i;
			for (i=0; i < splane.numpoles; i++)
			  {
				complex hba = 0.5 * (bw / splane.poles[i]);
				complex temp = csqrt(1.0 - sqr(w0 / hba));
				splane.poles[i] = hba * (1.0 + temp);
				splane.poles[splane.numpoles+i] = hba * (1.0 - temp);
			  }
			for (i=0; i < splane.numpoles; i++)	   /* also 2N zeros at (0, +-w0) */
			  {
				splane.zeros[i] = complex(0.0, +w0);
				splane.zeros[splane.numpoles+i] = complex(0.0, -w0);
			  }
			splane.numpoles *= 2;
			splane.numzeros = splane.numpoles;

		  }

}

static void compute_z_blt() /* given S-plane poles & zeros, compute Z-plane poles & zeros, by bilinear transform */
 {

	int i;
    zplane.numpoles = splane.numpoles;
    zplane.numzeros = splane.numzeros;

    for (i=0; i < zplane.numpoles; i++) {

    	zplane.poles[i] = blt(splane.poles[i]);
    }
    for (i=0; i < zplane.numzeros; i++) {

    	zplane.zeros[i] = blt(splane.zeros[i]);
    }
    while (zplane.numzeros < zplane.numpoles)
    	zplane.zeros[zplane.numzeros++] = -1.0;

 }

static Complex blt(Complex pz)
  {

	return (2.0 + pz) / (2.0 - pz);
  }

static void expandpoly() /* given Z-plane poles & zeros, compute top & bot polynomials in Z, and then recurrence relation */
  {

	Complex topcoeffs[MAXPZ+1], botcoeffs[MAXPZ+1]; int i;
    expand(zplane.zeros, zplane.numzeros, topcoeffs);
    expand(zplane.poles, zplane.numpoles, botcoeffs);
    dc_gain = evaluate(topcoeffs, zplane.numzeros, botcoeffs, zplane.numpoles, 1.0);
    double theta = TWOPI * 0.5 * (raw_alpha1 + raw_alpha2); /* "jwT" for centre freq. */
    fc_gain = evaluate(topcoeffs, zplane.numzeros, botcoeffs, zplane.numpoles, expj(theta));
    hf_gain = evaluate(topcoeffs, zplane.numzeros, botcoeffs, zplane.numpoles, -1.0);
    for (i = 0; i <= zplane.numzeros; i++) xcoeffs[i] = +(topcoeffs[i].re / botcoeffs[zplane.numpoles].re);
    for (i = 0; i <= zplane.numpoles; i++) ycoeffs[i] = -(botcoeffs[i].re / botcoeffs[zplane.numpoles].re);
  }

static void expand(Complex pz[], int npz, Complex coeffs[])
  { /* compute product of poles or zeros as a polynomial of z */

	int i;
    coeffs[0] = 1.0;
    for (i=0; i < npz; i++) coeffs[i+1] = 0.0;
    for (i=0; i < npz; i++) multin(pz[i], npz, coeffs);
    /* check computed coeffs of z^k are all real */
    for (i=0; i < npz+1; i++)
      {
    	if (fabs(coeffs[i].im) > EPS)
		  {

    		printf("mkfilter: coeff of z^%d is not real; poles/zeros are not complex conjugates\n", i);
			exit(1);
		  }
      }
  }

static void multin(Complex w, int npz, Complex coeffs[])
  { /* multiply factor (z-w) into coeffs */

	Complex nw = -w;
    for (int i = npz; i >= 1; i=i-1) coeffs[i] = (nw * coeffs[i]) + coeffs[i-1];
    coeffs[0] = nw * coeffs[0];
  }

static void printresults()
  {
	//char conversao[20];
	printf("printresults\n");
	//Complex gain;
	if(f_lp == 1)  gain = dc_gain;
	else if (f_hp == 1)  gain = hf_gain;
	else if ((f_bp == 1) | (f_ap == 1))  gain = fc_gain;
	else if (f_bs == 1)  gain = csqrt(dc_gain * hf_gain);
	else gain = complex(1.0);
	//UARTprintf("o ganho.re antes eh = %s", conversao);
	//snprintf(conversao,20,"%f", gain.re);
	//UARTprintf("o ganho.re eh = %s", conversao);
	//printf("re %f im %f \n", gain.re, gain.im);
	final_gain = c_hypot(gain);
	//printf("G  = %.10e\n", final_gain);
	printcoeffs("NZ", zplane.numzeros, xcoeffs);
	printcoeffs("NP", zplane.numpoles, ycoeffs);

  }

static void printcoeffs(char *pz, int npz, double coeffs[])
  {
	printf("printcoef\n");
	//printf("%s = %d\n", pz, npz);
    //for (int i = 0; i <= npz; i++) printf("%18.10e\n", coeffs[i]);
  }



//////////////////////////////////parte do gencode//////////


void gencode(double &ganho, int &nzeros, double *xcoeffs, int &npoles, double *ycoeffs)
{

	language = ansic;

	pbgain = ganho;
	npoles_gen = npoles;
	nzeros_gen = nzeros;
	unless (ycoeffs[npoles_gen] == -1.0) formaterror(1);
	if (nzeros_gen >npoles_gen) formaterror(2);

	compileclear(xcoeffs,ycoeffs);
}



static void formaterror(int n)
{
	printf(" input format error (%d)\n", n);
	exit(1);
}

static void usage()
{
	printf("Gencode version from <fisher@minster.york.ac.uk>\n");
	printf("Usage: gencode [-ansic | -xyc | -f]\n");
	exit(1);
}



static void compileclear(double *xcoeffs, double *ycoeffs)
{
	int n = 0;
	while (n <npoles_gen && ycoeffs[n] == 0.0) n++;
	//if (n >=npoles_gen) comp_fir(xcoeffs); else comp_iir(xcoeffs,ycoeffs);

}


static void comp_fir(double *xcoeffs)
{
	printf("static float xv[nzeros_gen+1];\n\n");
	pr_xcoeffs(xcoeffs);
	printf("static void filterloop()\n");
	printf("  { for (;;)\n");
	printf("      { float sum; int i;\n");
	printf("        for (i = 0; i < nzeros_gen; i++) xv[i] = xv[i+1];\n");
	printf("        xv[nzeros_gen] = `next input value' / GAIN;\n");
	printf("        sum = 0.0;\n");
	printf("        for (i = 0; i <= nzeros_gen; i++) sum += (xcoeffs[i] * xv[i]);\n");
	printf("        `next output value' = sum;\n");
	printf("      }\n");
	printf("  }\n\n");
}


static void comp_iir(double *xcoeffs,double *ycoeffs)
{
	//printf("#define nzeros_gen %d\n", nzeros_gen);
	//printf("#define npoles_gen %d\n",npoles_gen);
	//UARTprintf("#define GAIN   %15.9e\n\n", pbgain);
	printf("#define GAIN   %s\n\n",dtoa(s,pbgain));
	printf("static float xv[nzeros_gen+1], yv[npoles_gen+1];\n\n");
	margin = 20;
	printf("static void filterloop()\n");
	printf("  { for (;;)\n");
	printf("      { "); pr_shiftdown("xv", nzeros_gen); putchar('\n');
	//printf("        xv[%d] = `next input value' / GAIN;\n", nzeros_gen);
	printf("        "); pr_shiftdown("yv",npoles_gen); putchar('\n');
	//printf("        yv[%d] =",npoles_gen);
	pr_xpart("xv",xcoeffs); pr_ypart("yv",ycoeffs); printf(";\n");
	//printf("        `next output value' = yv[%d];\n",npoles_gen);
	printf("      }\n");
	printf("  }\n\n");
}


static void pr_shiftdown(const char *vs, int n)
{
	for (int i = 0; i < n; i++) printf("pr_shiftdown");//printf("%s[%d] = %s[%d]; ", vs, i, vs, i+1);
}


static void pr_xcoeffs(double *xcoeffs)
{
	printf("static float xcoeffs[] =\n  {");
	for (int i=0; i <= nzeros_gen; i++)
	{
		if (i > 0 && i%4 == 0) printf("\n   ");
		//printf(" %+0.10f,\n", xcoeffs[i]);
	}
	printf("\n  };\n\n");
}


static void pr_ycoeffs(double *ycoeffs)
{
	printf("static float ycoeffs[] =\n  {");
	for (int i=0; i <npoles_gen; i++)
	{
		if (i > 0 && i%4 == 0) printf("\n   ");
		printf(" %+0.10f,", ycoeffs[i]);
	}
	printf("\n  };\n\n");
}

/* output contribution from X vec */

static void pr_xpart(const char *vs,double *xcoeffs)
{
	nxfacs = 0;
	for (int i=0; i < (nzeros_gen+1)/2; i++)
	{
		int j = nzeros_gen-i;
		double xi = xcoeffs[i], xj = xcoeffs[j];
		/* they should be paired, except for allpass resonator */
		if (xi == xj)
		{
			unless (xi == 0.0)
			{
				prxfac(xi); //printf("(%s[%d] + %s[%d])", vs, i, vs, j);
			}
		}
		else if (xi == -xj)
		{
			if (xi > 0.0)
			{
				prxfac(xi); //printf("(%s[%d] - %s[%d])", vs, i, vs, j);
			}
			else { prxfac(xj); //printf("(%s[%d] - %s[%d])", vs, j, vs, i);
			}
		}
		else
		{
			unless (xi == 0.0)
			{
				prxfac(xi); //printf("%s[%d]", vs, i);
			}
			unless (xj == 0.0) { prxfac(xj); //printf("%s[%d]", vs, j);
			}
		}
	}
	if ((nzeros_gen+1) & 1)
	{
		int j = nzeros_gen/2;
		double xj = xcoeffs[j];
		unless (xj == 0.0) { prxfac(xj); //printf("%s[%d]", vs, j);
		}
	}
}


static void prxfac(double x)
{
	if (nxfacs > 0 && nxfacs%3 == 0) prnl();
	if (x > 0.0) printf((nxfacs > 0) ? " + " : "   ");
	if (x < 0.0) { printf(" - "); x = -x; }
	unless (x == 1.0)
	{
		double f = fmod(x, 1.0);
		const char *fmt = (f < EPS || f > 1.0-EPS) ? "%g" : "%14.10f";
		//printf(fmt, x); printf(" * ");
	}
	nxfacs++;
}


/* output contribution from Y vec */
static void pr_ypart(const char *vs,double *ycoeffs)
{
	for (int i=0; i <npoles_gen; i++)
	{
		if (i%2 == 0) prnl();
		//printf(" + (%14.10f * %s[%d])", ycoeffs[i], vs, i);
	}
}


static void prnl()
{
	putchar('\n');
	for (int j = 0; j < margin; j++) putchar(' ');
}


static void giveup(const char *msg, int p1, int p2)
{
	printf("gencode: ");
	printf(msg, p1, p2); putchar('\n');
	exit(1);
}


////////////////////////////////////////////////////////////parte filtro



//teste da funcao
/*
static void filtro(){

	parar = 0;
	segunda_vez=0; // menor de int? Para não precisar calcular os coeficientes de novo
	for(int t = 0; t < 1000; t++){ //testando a entrada

		next_input = entrada_dev[t];
		if(parar == 1) break;
		for (int i = 0; i < nzeros_gen; i++) //pegando os valores de xv antigos
			xv[i] = xv[i+1];
		xv[nzeros_gen] = next_input/pbgain;	//atualizando o ultimo valor com a entrada
		for (int i = 0; i < npoles_gen; i++) //pegando os valores de yv antigos
			yv[i] = yv[i+1];
		yv[npoles_gen] = parte_x() + parte_y();	//parte_x e parte_y calculam as partes do filtro
		next_output = yv[npoles_gen];
		dtoa(s,next_output);//Conversao. Tem que converter aqui, se converter na UASTprintf dá erro
		delayMs(300);
		UARTprintf(" %s\n",s); // precisa delay entre os envios?
		segunda_vez = 1;

	}
	printf("Enviado toda a saida\n");
}

*/
///////////////////////////////////////////////////////////////////////////////

static double parte_x()
{
	nxfacs = 0;
	total_partx = 0;
	int ifora; //o valor de i desse for tem q ser pasado para o if abaixo
	for (int i=0; i < (nzeros_gen+1)/2; i++)
	{
		//printf("Entrei %d\n",i);
		incognita_filtro = 0; // incognita tem que ser zerada em cada interação, pois faz o calculo de cada parte entre parenteses. Ex (x[0] + x[4])
		if(segunda_vez == 0) coef_filtro[i] = 1; //sempre tem coeficiente por isso 1. Para não precisar calcular de novo, na proxima vez nao vai entar aqui
		int j = nzeros_gen-i;
		double xi = xcoeffs[i], xj = xcoeffs[j];
		/* they should be paired, except for allpass resonator */
		if (xi == xj)
		{
			unless (xi == 0.0)
			{
				if(segunda_vez == 0) prxfac_filtro(xi, i);
				incognita_filtro = xv[i] + xv[j]; // multiplicação da incognita
				total_partx = total_partx +(coef_filtro[i]*incognita_filtro);

			}
		}
		else if (xi == -xj)
		{
			if (xi > 0.0)
			{
				if(segunda_vez == 0) prxfac_filtro(xi,i);
				incognita_filtro = xv[i] - xv[j]; // multiplicação da incognita
				total_partx = total_partx +(coef_filtro[i]*incognita_filtro);
			}
			else
			{
				if(segunda_vez == 0) prxfac_filtro(xj,i);
				incognita_filtro = xv[j] - xv[i]; // multiplicação da incognita
				total_partx = total_partx +(coef_filtro[i]*incognita_filtro);
			}
		}
		else
		{
			unless (xi == 0.0)
			{
				if(segunda_vez == 0) prxfac_filtro(xi,i);
				incognita_filtro = xv[i]; // incognita
				total_partx = total_partx +(coef_filtro[i]*incognita_filtro);
			}
			unless (xj == 0.0)
			{
				if(segunda_vez == 0) prxfac_filtro(xj,i);
				incognita_filtro = xv[j]; // incognita
				total_partx = total_partx +(coef_filtro[i]*incognita_filtro);
			}
		}
		ifora = i;
	}
	ifora = ifora + 1; // para que troque o ultimo elemento
	if ((nzeros_gen+1) & 1)
	{
		int j = nzeros_gen/2;
		double xj = xcoeffs[j];
		unless (xj == 0.0)
		{
			if(segunda_vez == 0) prxfac_filtro(xj,ifora);
			incognita_filtro = xv[j]; // incognita
			total_partx = total_partx +(coef_filtro[ifora]*incognita_filtro);
		}
	}
	return total_partx;
}

static void prxfac_filtro(double x, int i)
{
	if (x > 0.0){
		if(nxfacs > 0){
			//printf("+");
			unless (x == 1.0)
			{
				//printf(" * ");
				coef_filtro[i]= x;
			}
		}
		else{
			coef_filtro[i]=1;
			unless (x == 1.0)
			{
				//printf(" * ");
				coef_filtro[i]= x;
			}
		}
	}
	if (x < 0.0) {
		//printf(" - ");
		coef_filtro[i] = (-1);
		x = -x;
		unless (x == 1.0)
			{
				coef_filtro[i]= -x;
			}
	}

	nxfacs++;
}

static double parte_y()
{
	total_party = 0;
	for (int i=0; i <npoles_gen; i++)
	{
		total_party = total_party +(ycoeffs[i]*yv[i]);
	}
	return total_party;
}

////////////////////////////parte dtoa////////////////////////////
/**
 * Double to ASCII
 */
char * dtoa(char *s, double n) {
    // handle special cases
    if (isnan(n)) {
        strcpy(s, "nan");
    } else if (isinf(n)) {
        strcpy(s, "inf");
    } else if (n == 0.0) {
        strcpy(s, "0");
    } else {
        int digit, m, m1;
        char *c = s;
        int neg = (n < 0);
        if (neg)
            n = -n;
        // calculate magnitude
        m = log10(n);
        int useExp = (m >= 14 || (neg && m >= 9) || m <= -9);
        if (neg)
            *(c++) = '-';
        // set up for scientific notation
        if (useExp) {
            if (m < 0)
               m -= 1.0;
            n = n / pow(10.0, m);
            m1 = m;
            m = 0;
        }
        if (m < 1.0) {
            m = 0;
        }
        // convert the number
        while (n > PRECISION || m >= 0) {
            double weight = pow(10.0, m);
            if (weight > 0 && !isinf(weight)) {
                digit = floor(n / weight);
                n -= (digit * weight);
                *(c++) = '0' + digit;
            }
            if (m == 0 && n > 0)
                *(c++) = '.';
            m--;
        }
        if (useExp) {
            // convert the exponent
            int i, j;
            *(c++) = 'e';
            if (m1 > 0) {
                *(c++) = '+';
            } else {
                *(c++) = '-';
                m1 = -m1;
            }
            m = 0;
            while (m1 > 0) {
                *(c++) = '0' + m1 % 10;
                m1 /= 10;
                m++;
            }
            c -= m;
            for (i = 0, j = m-1; i<j; i++, j--) {
                // swap without temporary
                c[i] ^= c[j];
                c[j] ^= c[i];
                c[i] ^= c[j];
            }
            c += m;
        }
        *(c) = '\0';
    }
    return s;
}
/////////////////////////////////////////////////////////////

//Funcao que processa a entrada e seta as variáveis do filtros
void processaEntrada(void)
{
	char convOrder[0]; //A ordem eh ate 8
	char convAlpha[22]; //20 casas de precisao
	char convAlpha2[22]; //20 casas de precisao
	char convChebrip[12];
	int posT; //posicao onde esta t - para descobrir o alpha2
	uint32_t posA; //posicao onde esta a - para descobrir o alpha quando é chebysev
	int i, j;
	if((bufferRequisicao[0] == 'b') && (bufferRequisicao[1] == 'e')){
		f_be = 1;
		puts("be");
	}
	else if((bufferRequisicao[0] == 'b') && (bufferRequisicao[1] == 'u')){
		f_bu = 1;
		puts("bu");
	}
	else if((bufferRequisicao[0] == 'c') && (bufferRequisicao[1] == 'h')){
		f_ch = 1;
	    puts("ch");
	}
	//resposta em frequencia
	if((bufferRequisicao[3] == 'l') && (bufferRequisicao[4] == 'p'))
		f_lp = 1;
	else if((bufferRequisicao[3] == 'h') && (bufferRequisicao[4] == 'p'))
		f_hp = 1;
	else if((bufferRequisicao[3] == 'b') && (bufferRequisicao[4] == 's')){
		f_bs = 1;
		//alpha2 = atof(texto[10]);
	}
	else if((bufferRequisicao[3] == 'b') && (bufferRequisicao[4] == 'p')){
		f_bp = 1;
		//alpha2 = atof(texto[10]);
	}

	//ordem
	convOrder[0] = bufferRequisicao[6];
	order = atoi(convOrder);

	//alpha
	if(f_ch == 0){ // Eh Bessel ou Butterworth
		if(bufferRequisicao[7] == 'a'){ //inicio do alpha
			 i=8;  j=0;
			while(!((bufferRequisicao[i] == 'z') || (bufferRequisicao[i] == 't'))){
				convAlpha[j] = bufferRequisicao[i]; //repassando o alpha
				j++;
				i++;
			}
			if(bufferRequisicao[i] == 't')
				posT = i;
			i=0; j=0;
			alpha = atof(convAlpha);
		}
	}
	else if(f_ch == 1){ //Eh chebshev
		//primeiro encontra-se o chebrip
		if(bufferRequisicao[7] == 'r'){
			 i=8;  j=0;
			while(bufferRequisicao[i] != 'a'){
				convChebrip[j] = bufferRequisicao[i]; //repassando chebrip
				j++;
				i++;
			}
			posA = i;
			j=0;
			chebrip = atof(convChebrip);
		}

		//alpha
		i=i+1;
		while(!((bufferRequisicao[i] == 'z') || (bufferRequisicao[i] == 't'))){
			convAlpha[j] = bufferRequisicao[i]; //repassando o alpha
			j++;
			i++;
		}
		if(bufferRequisicao[i] == 't')
			posT = i;
		i=0; j=0;
		alpha = atof(convAlpha);

		// Eh chebyshev e eh BS ou BP
		// Alpha2
		if((f_bs == 1) || (f_bp == 1)){
			i = posT + 1;
			while(!(bufferRequisicao[i] == 'z')){
				convAlpha2[j] = bufferRequisicao[i];
				j++;
				i++;
			}
			i=0; j=0;
			alpha2 = atof(convAlpha2);
		}
	}

	// Alpha2 e eh BS ou BP
	if((f_bs == 1) || (f_bp == 1)){
		i = posT + 1;
		while(!(bufferRequisicao[i] == 'z')){
			convAlpha2[j] = bufferRequisicao[i];
			j++;
			i++;
		}
		i=0; j=0;
		alpha2 = atof(convAlpha2);
	}

}


/////////////////////////GUI/////////////////////////////////////

//UART interrupt handler
extern "C"//como o codigo esta em c++ tem que colocar esse extern para o linker enxergar a funcao
{
	void UARTIntHandler(void)
	{
		uint32_t ui32Status;
		uint16_t i=0, j;

		// Get the interrrupt status.
		ui32Status = UARTIntStatus(UART0_BASE, true);

		// Clear the asserted interrupts.
		UARTIntClear(UART0_BASE, ui32Status);

		ui32Status = UARTIntStatus(UART0_BASE, true);
		if (flagInterrupcao == 0){
			while(UARTCharsAvail(UART0_BASE))
			{

				texto[i] = UARTCharGetNonBlocking(UART0_BASE);
				//printf("%s\n",texto);
				//UARTgets(texto,strlen(texto));
				i=i+1;
				SysCtlDelay(2*(SysCtlClockGet() / (1000 * 3))); //2ms

				if(i==1){
					if((texto[0] == 'b') || (texto[0] =='c')) //Verificando se recebeu uma verificacao valida ( b e c representam be, bu e/ou ch)
						flag = 1;
					else if (texto[0] == 'F'){ // Vai ser o inicio da requisição de parada, falta tratar isso
						puts("recebeu");
						SysCtlReset();
					}
					else if (texto[0] == 'G'){ //Receber a frequencia do gerador de sinal
						flag_gerador = true;
					}
					else if (texto[0] == 'K'){ //Receber a frequencia de amostragem
						flag_freq_amostragem = true;
					}
				}
			}

			//Tratando a frequencia do gerador de sinal
			if(flag_gerador == true)
			{
				int j = 0;
				for(int i = 1; texto[i] != NULL;i++){
						vetFreq[j] = texto[i]; //repassando a frequencia do gerador
						texto[i] = NULL;
						j++;
				}
				freq = atoi(vetFreq); //Frequencia AD9850
				//UARTprintf("G\n");
				//printf("Enviei G\n");
			}

			//Tratando a frequencia de amostragem
			if(flag_freq_amostragem == true)
			{
				int j = 0;
				for(int i = 1; texto[i] != NULL;i++){
					vetFreq_amostragem[j] = texto[i]; //repassando a frequencia de amostragem
					texto[i] = NULL;
					j++;
				}
				freq_amostragem = atoi(vetFreq_amostragem); //Frequencia amostragem
			}

			//esperando as partes da requisição
			if( ((texto[3] == 'l') && (texto[4] == 'p')) || ((texto[3] == 'h') && (texto[4] == 'p')))
				lp_hp = true;
			else if( ((texto[3] == 'b') && (texto[4] == 's')) || ((texto[3] == 'b') && (texto[4] == 'p')))
				bp_bs = true;
			if(lp_hp == true)
			{
				flag = 0;
				if(parte1 == false){
					strcpy(bufferRequisicao,texto);
					parte1 = true; //primeira parte
					for(j=0;texto[j]!=NULL;j++)
						texto[j]=NULL;
				}
				else if(parte2 == false){
					strcat(bufferRequisicao,texto);
					parte2 = true;
					strcpy(texto,bufferRequisicao);
					flag = 1;
					//ativaRecebimento = 1;
					for(j=0;texto[j]!=NULL;j++)
						texto[j]=NULL;
					lp_hp = false;
				}
			}
			else if(bp_bs == true)
			{
				flag = 0;
				if(parte1 == false){
					strcpy(bufferRequisicao,texto);
					parte1 = true; //primeira parte
					for(j=0;texto[j]!=NULL;j++)
						texto[j]=NULL;
				}
				else if(parte2 == false){
					strcat(bufferRequisicao,texto);
					parte2 = true;
					for(j=0;texto[j]!=NULL;j++)
						texto[j]=NULL;
				}
				else if(parte3 == false){
					strcat(bufferRequisicao,texto);
					parte3 = true;
					strcpy(texto,bufferRequisicao);
					flag = 1;
					//ativaRecebimento = 1;
					for(j=0;texto[j]!=NULL;j++)
						texto[j]=NULL;
					bp_bs = false;
				}
			}
			cont = cont + 1;
			flagInterrupcao	= 1;
		}
		else if (flagInterrupcao == 1)
			flagInterrupcao = 0;
		ui32Status = UARTIntStatus(UART0_BASE, true);
	}
}

extern "C"
{
	void ResetISRMod(void){

		__asm("    .global _c_int00\n"
				  "    b.w     _c_int00");
	}

}


extern "C"//como o codigo esta em c++ tem que colocar esse extern para o linker enxergar a funcao
{
	void ADCIntHandler(void)
	{
		 //printf("interrupcao\n");
		 //
		 // Clear the ADC interrupt flag.
		 //
		 //GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, GPIO_PIN_4);
		 ADCIntClear(ADC0_BASE, 3);
		 if(GPIOPinRead(GPIO_PORTF_BASE, GPIO_PIN_2))
		 {
			 GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3, 0);
		 }
		 else
		 {
			 GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_2, 4);
		 }
         //
         // Read ADC Value.
	     //
	     ADCSequenceDataGet(ADC0_BASE, 3, pui32ADC0Value);

		 //
		 // Display the AIN0 (PE3) digital value on the console.
		 //
		 // UARTprintf("AIN0 = %4d\r", pui32ADC0Value[0]);
		 //Cada nível de quantização equivale a 0.8 mV. Estou imprimindo o
		 //valor já convertido.
	     doubleADC0Value[0] = pui32ADC0Value[0] * 0.0008;

		 //entrada_dev[0] = atof(texto); //convertendo a entrada
		 next_input = doubleADC0Value[0];
		 //if(parar == 1) break;
		 for (int i = 0; i < nzeros_gen; i++) //pegando os valores de xv antigos
		 	xv[i] = xv[i+1];
		 xv[nzeros_gen] = next_input/pbgain;	//atualizando o ultimo valor com a entrada
		 for (int i = 0; i < npoles_gen; i++) //pegando os valores de yv antigos
		 	yv[i] = yv[i+1];
		 yv[npoles_gen] = parte_x() + parte_y();	//parte_x e parte_y calculam as partes do filtro
		 next_output = yv[npoles_gen];
		 dtoa(s,next_output);//Conversao. Tem que converter aqui, se converter na UARTprintf dá erro
		 //debug delayMs(300);
		 UARTprintf(" %s\n",s); // precisa delay entre os envios?

		 //GPIOPinWrite(GPIO_PORTF_BASE, GPIO_PIN_4, 0);

	}
}


//////////////////////////////////////////////////////////////////

int main(void){
	uint32_t ui32Period;

	// Observacao: a função handler foi adicionada no arquivo de startup.csc
	// In CCS right click on your project, "Show Build Settings" -> Build -> ARM Compiler
	//->Advanced Options -> Predefined Symbols add : TAREGT_IS_TM4C123_RB1
	//50MHz clock
	SysCtlClockSet(SYSCTL_SYSDIV_4 | SYSCTL_USE_PLL | SYSCTL_XTAL_16MHZ | SYSCTL_OSC_MAIN);

	//leddd


	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
	GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3);

    //ADC
    // The ADC0 peripheral must be enabled for use.
    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0);
    // For this example ADC0 is used with AIN0 on port E3.
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE);
    // Select the analog ADC function for these pins.
    GPIOPinTypeADC(GPIO_PORTE_BASE, GPIO_PIN_3);

    // Set up the serial console to use for displaying messages.
    InitConsole();

    //enable the uart interrupt
    IntEnable(INT_UART0_TM4C123);

    //enable the source of interrupt
    UARTIntEnable(UART0_BASE, UART_INT_RX | UART_INT_RT);

    // Enable sample sequence 3 with a processor signal trigger.  Sequence 3
    // will do a single sample when the processor sends a signal to start the
    // conversion.  Each ADC module has 4 programmable sequences, sequence 0
    // to sequence 3.  This example is arbitrarily using sequence 3.
    //
    ADCSequenceConfigure(ADC0_BASE, 3, ADC_TRIGGER_TIMER, 0);

    // Configure step 0 on sequence 3.  Sample channel 0 (ADC_CTL_CH0) in
    // single-ended mode (default) and configure the interrupt flag
    // (ADC_CTL_IE) to be set when the sample is done.  Tell the ADC logic
    // that this is the last conversion on sequence 3 (ADC_CTL_END).  Sequence
    // 3 has only one programmable step.  Sequence 1 and 2 have 4 steps, and
    // sequence 0 has 8 programmable steps.  Since we are only doing a single
    // conversion using sequence 3 we will only configure step 0.  For more
    // information on the ADC sequences and steps, reference the datasheet.
    ADCSequenceStepConfigure(ADC0_BASE, 3, 0, ADC_CTL_CH0 | ADC_CTL_IE | ADC_CTL_END);

    // Since sample sequence 3 is now configured, it must be enabled.
    ADCSequenceEnable(ADC0_BASE, 3);

    // Clear the interrupt status flag.  This is done to make sure the
    // interrupt flag is cleared before we sample.
    ADCIntClear(ADC0_BASE, 3);

    ADCIntClear(ADC0_BASE, 3);

    SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);

    //Enable triggering
    TimerControlTrigger(TIMER0_BASE, TIMER_A, true);

    /*freq_amostragem = 128;
    ui32Period = (SysCtlClockGet() / freq_amostragem); //128
    TimerLoadSet(TIMER0_BASE, TIMER_A, ui32Period -1);
*/

    IntMasterEnable();

    IntEnable(INT_ADC0SS3);
    ADCIntEnable(ADC0_BASE, 3);

    //***********************************************************
    //AD9850 config
	SysCtlPeripheralEnable(PORT_ENABLE);
	GPIOPinTypeGPIOOutput(PORT, W_CLK | FQ_UD | DATA | RESET);
	AD9850_Init();
	AD9850_Reset();
    //Os pinos estão no PORT D

	//************************************************************

    printf("Esperando o filtro \n"); //Para a função printf funcionar, o Heap size para alocacao dinamica tem que ser 320

    //Setando as flags
    flagInterrupcao = 0;
    nEntrada = 0;
    flag = 0;
    flagEntrada = 0;
    ativaRecebimento = 0;
    cont = 0;
    parte1 = false;
    parte2 = false;
    parte3 = false;
    lp_hp = false;
    bp_bs = false;
    flag_gerador = false;
    flag_freq_amostragem = false;

    while(!(flag == 1)) //Esperando a requisição do filtro
    {
    	//Tratando a frequencia do gerador de sinal
    	if(flag_gerador == true)
    	{
    		flag_gerador = false;
    		UARTprintf("G\n");
    		printf("Enviei G\n");
    	}

    	//Tratando a frequencia de amostragem
    	if(flag_freq_amostragem == true)
    	{
    		flag_freq_amostragem = false;
    		UARTprintf("K\n");
    		printf("Enviei K\n");
    	}
    	if( ((bufferRequisicao[3] == 'l') && (bufferRequisicao[4] == 'p')) || ((bufferRequisicao[3] == 'h') && (bufferRequisicao[4] == 'p'))){
    		if((parte1 == true) && (parte2 == false)){
    			UARTprintf("a\n");
    			printf("Enviei a\n");
    	    }
    	}
    	else if( ((bufferRequisicao[3] == 'b') && (bufferRequisicao[4] == 's')) || ((bufferRequisicao[3] == 'b') && (bufferRequisicao[4] == 'p'))){
    		if((parte1 == true) && (parte2 == false) && (parte3 == false)){
    			UARTprintf("a\n");
    			printf("Enviei a\n");
    		}
    		else if((parte1 == true) && (parte2 == true) && (parte3 == false)){
				UARTprintf("b\n");
				printf("Enviei b\n");
			}
    	}

    }
    AD9850_Osc(freq, 0); //Setando a frequencia do gerador de sinal
    SysCtlDelay(SysCtlClockGet() / 2400); // delay devido ao bouncing da interrupcao
    printf("A flag eh 1\n");
    flag = 0;

    processaEntrada();
	calcula_coef();
	printf("Esperando a entrada \n");

	//Timer da amostragem

	ui32Period = (SysCtlClockGet() / freq_amostragem); //128
	TimerLoadSet(TIMER0_BASE, TIMER_A, ui32Period -1);

	TimerEnable(TIMER0_BASE, TIMER_A);

	while(1)
	{
	}

}
