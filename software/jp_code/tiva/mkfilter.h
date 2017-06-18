/*
 * mkfilter.h
 *
 *  Created on: 19/08/2016
 *      Author: jp
 */

#ifndef FILTRO_GUI_SEM_ADCMEIO_MKFILTER_H_
#define FILTRO_GUI_SEM_ADCMEIO_MKFILTER_H_

#include <string.h>
#include <math.h>

#define global
#define unless(x)   if(!(x))
#define until(x)    while(!(x))

//#define VERSION	    "4.6"
#undef	PI
#define PI	    3.14159265358979323846
#define TWOPI	    (2.0 * PI)
#define EPS	    1e-10
#define MAXORDER    10
#define MAXPZ	    255	    /* .ge. 2*MAXORDER, to allow for doubling of poles in BP filter;
			       high values needed for FIR filters */
#define MAXSTRING   256

typedef void (*proc)();
typedef unsigned int uint;

extern "C"
  {
	double atof(const char*); // atoi é para double, trocar tbm a função?
    int atoi(char*);
    void exit(int);
  };

//extern char *progname;
void gencode(double&, int&, double*, int&, double*); //arquivo gencode.cpp

inline double sqr(double x)
{
	return x*x;
}
/*inline bool seq(char *s1, char *s2)
{
	return strcmp(s1,s2) == 0;
}*/
inline bool onebit(uint m)
{
	return (m != 0) && ((m & m-1) == 0);
}

inline double asinh(double x)
  {
    return log(x + sqrt(1.0 + sqr(x)));
  }

//inline double fix(double x)
 // { /* nearest integer */
//    return (x >= 0.0) ? floor(0.5+x) : -floor(0.5-x);
//  }


#endif /* FILTRO_FUNCAO_SIMPLES_FILTRO_GUI_SEM_ADCMEIO_MKFILTER_H_ */
