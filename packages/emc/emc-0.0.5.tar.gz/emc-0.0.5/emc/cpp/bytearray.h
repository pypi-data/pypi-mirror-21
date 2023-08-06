/**
 * C++ library for EMC genetic string manipulation.
 *
 * \author Csaba Sulyok
 */


#pragma once


/**
 * Create random byte array of given size.
 * Uses NumPy array, therefore allocation not necessary, but size must be in parameters.
 */
void randomByteArray(unsigned char* outp, int outp_size);


/**
 * Splice together two byte arrays at multiple cut points. All 3 given sizes must be equal.
 * Randomly generates a number of cut points, at at those points, changes which parent it takes values from.
 * Uses NumPy array, therefore allocation not necessary, but size must be in parameters.
 */
void combineByteArray(unsigned char* inp1, int inp1_size, unsigned char* inp2, int inp2_size,
                      unsigned char* inpl1, int inpl1_size, unsigned char* inpl2, int inpl2_size,
                      unsigned int max_cut_points);


/**
 * Mutate some bytes in a byte array.
 * Effectively give new random value to some random bytes in a byte array.
 * Uses NumPy array, therefore allocation not necessary, but size must be in parameters.
 */
void mutateBytesInByteArray(unsigned char* inpl, int inpl_size, unsigned int max_randomizations);
