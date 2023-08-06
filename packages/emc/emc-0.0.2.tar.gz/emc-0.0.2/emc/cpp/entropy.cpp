#include "entropy.h"

#include <stdio.h>
#include <string.h>
#include <math.h>


float _occurrences[256];

float entropy(unsigned short* inp, int inp_size)
{
  // set counters to 0
  memset(_occurrences, 0, sizeof _occurrences);

  for (unsigned int i = 0; i < inp_size; ++i)
  {
    _occurrences[inp[i] & 0xff]++;
  }

  float ret = 0;

  for (unsigned int i = 0; i < 256; ++i)
  {
    if (_occurrences[i] > 0)
    {
      float p_i = _occurrences[i] / (float) inp_size;
      ret += -p_i * log2(p_i);
    }
  }

  return ret * 31.875f;
}
