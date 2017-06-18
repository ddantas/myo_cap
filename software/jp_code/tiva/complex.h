/*
 * complex.h
 *
 *  Created on: 19/08/2016
 *      Author: jp
 */

#ifndef FILTRO_GUI_SEM_ADCMEIO_COMPLEX_H_
#define FILTRO_GUI_SEM_ADCMEIO_COMPLEX_H_

typedef struct c_complex
  {
	double re, im;
  } C_complex;

typedef struct complex
  {
	double re, im;
	complex(double r, double i = 0.0){re = r;im = i;  } //Não pode construtor em C
	complex() { }					/* uninitialized complex */
	complex(c_complex z){ re = z.re; im = z.im; }	/* init from denotation */
  } Complex;


extern Complex csqrt(Complex);
extern Complex cexp(Complex);
extern Complex expj(double);
extern Complex evaluate(Complex[], int, Complex[], int, Complex);   /* from Complex.C */

inline double c_hypot(Complex z)
{
	return hypot(z.im, z.re);
}
inline double c_atan2(Complex z)
{
	return atan2(z.im, z.re);
}


inline Complex cconj(Complex z)
 {
	z.im = -z.im;
    return z;
 }

 inline Complex operator * (double a, Complex z)
 {
	z.re *= a;
	z.im *= a;
	return z;
 }

inline Complex operator / (Complex z, double a)
  {
	//z.re /= a;
	z.re = z.re / a;
	//z.im /= a;
	z.im = z.im / a;
    return z;
  }

inline void operator /= (Complex &z, double a)
  {
	z = z / a;
  }

extern Complex operator * (Complex, Complex);
extern Complex operator / (Complex, Complex);

inline Complex operator + (Complex z1, Complex z2)
  {
	//z1.re += z2.re;
	z1.re = z1.re + z2.re;
    //z1.im += z2.im;
    z1.im = z1.im + z2.im;
    return z1;
  }

inline Complex operator - (Complex z1, Complex z2)
  {
	//z1.re -= z2.re;
	z1.re = z1.re - z2.re;
    //z1.im -= z2.im;
    z1.im = z1.im - z2.im;
    return z1;
  }

inline Complex operator - (Complex z)
  {
	return (0.0 - z);
  }

inline bool operator == (Complex z1, Complex z2)
  {
	return (z1.re == z2.re) && (z1.im == z2.im);
  }

inline Complex sqr(Complex z)
  {
	return z*z;
  }



#endif /* FILTRO_FUNCAO_SIMPLES_FILTRO_GUI_SEM_ADCMEIO_COMPLEX_H_ */
