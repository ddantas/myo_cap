/*
 * complex.c
 *
 *  Created on: 19/08/2016
 *      Author: jp
 */

#include <math.h>

#include "mkfilter.h"
#include "complex.h"

static Complex eval(Complex[], int, Complex);
static double Xsqrt(double);

global Complex evaluate(Complex topco[], int nz, Complex botco[], int np, Complex z)
  { /* evaluate response, substituting for z */
    return eval(topco, nz, z) / eval(botco, np, z);
  }

static Complex eval(Complex coeffs[], int npz, Complex z)
  { /* evaluate polynomial in z, substituting for z */
    Complex sum = complex(0.0);
    for (int i = npz; i >= 0; i = i-1)
    	sum = (sum * z) + coeffs[i];
    return sum;
  }

global Complex csqrt(Complex x)
  { double r = c_hypot(x);
    Complex z = Complex( Xsqrt(0.5 * (r + x.re)), Xsqrt(0.5 * (r - x.re)));
    if (x.im < 0.0)
    	z.im = -z.im;
    return z;
  }

static double Xsqrt(double x)
  { /* because of deficiencies in hypot on Sparc, it's possible for arg of Xsqrt to be small and -ve,
       which logically it can't be (since r >= |x.re|).	 Take it as 0. */
    return (x >= 0.0) ? sqrt(x) : 0.0; // Deixar normal ou assim ?
  }

global Complex cexp(Complex z)
  {
	return exp(z.re) * expj(z.im);
  }

global Complex expj(double theta)
  {
	return Complex(cos(theta), sin(theta));
  }

global Complex operator * (Complex z1, Complex z2)
  {
	return Complex(z1.re*z2.re - z1.im*z2.im, z1.re*z2.im + z1.im*z2.re);
  }

global Complex operator / (Complex z1, Complex z2)
  {
	double mag = (z2.re * z2.re) + (z2.im * z2.im);
    return Complex ( ((z1.re * z2.re) + (z1.im * z2.im)) / mag, ((z1.im * z2.re) - (z1.re * z2.im)) / mag);
  }
