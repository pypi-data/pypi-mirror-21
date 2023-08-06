#include "bytearray.h"


#include <stdlib.h>
#include <math.h>


void randomByteArray(unsigned char* outp, int outp_size)
{
  for (int i = 0; i < outp_size; i++)
  {
    outp[i] = rand();
  }
}


void combineByteArray(unsigned char* inp1, int inp1_size, unsigned char* inp2, int inp2_size,
                      unsigned char* outp1, int outp1_size, unsigned char* outp2, int outp2_size,
                      unsigned int max_cut_points)
{
  unsigned int num_cut_points = max_cut_points > 0 ? rand() % max_cut_points + 1 : 1;
  unsigned int* cut_points = new unsigned int[num_cut_points + 1];
  double cut_points_scale = 0.0;

  for (unsigned int i = 0; i < num_cut_points + 1; i++)
  {
    cut_points[i] = rand();
    cut_points_scale += cut_points[i];
  }

  cut_points_scale = inp1_size / cut_points_scale;
  double cut_point_sum = 0.5; // use 0.5 because msvc has no round function - simulate by using floor(x+0.5)

  for (unsigned int i = 0; i < num_cut_points + 1; i++)
  {
    cut_point_sum += cut_points[i] * cut_points_scale;
    cut_points[i] = (unsigned int) floor(cut_point_sum);
  }

  unsigned char** inputs = new unsigned char*[2];
  inputs[0] = inp1; inputs[1] = inp2;
  char current_inp = 0;

  unsigned int next_cut_point = 0;

  for (int i = 0; i < inp1_size; i++)
  {
    outp1[i] = inputs[current_inp][i];
    outp2[i] = inputs[1 - current_inp][i];

    if (i == cut_points[next_cut_point])
    {
      current_inp = 1 - current_inp;
      next_cut_point++;
    }
  }

  delete [] inputs;
  delete [] cut_points;
}


void mutateBytesInByteArray(unsigned char* bs, int bs_size, unsigned int max_randomizations)
{
  int randomizations = rand() % max_randomizations;

  int rand_byte_idx;

  for (int i = 0; i < randomizations; ++i)
  {
    rand_byte_idx = rand() % bs_size;
    bs[rand_byte_idx] = rand();
  }
}
