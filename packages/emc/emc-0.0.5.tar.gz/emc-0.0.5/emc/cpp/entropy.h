/**
 * C++ library for data entropy calculation
 *
 * \author Csaba Sulyok
 */


#pragma once


/**
 * Measure binary Shannon entropy of data set.
 * Returns value between 0 and 255 if casting needed to uint8.
 */
float entropy(unsigned short* inp, int inp_size);

