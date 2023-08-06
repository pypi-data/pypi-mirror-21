%module emcpp
%{
#define SWIG_FILE_WITH_INIT
#include "../bytearray.h"
#include "../selector.h"
#include "../descriptor.h"
#include "../fitness.h"
#include "../modelbuilder.h"
#include "../entropy.h"
  
#include "../oci/immediateoci.h"
#include "../oci/immediateharvardoci.h"
#include "../oci/indirectoci.h"
#include "../oci/testoci.h"
#include "../oci/loadstoreoci.h"
#include "../oci/stackoci.h"
#include "../oci/stackharvardoci.h"
#include "../oci/sbnzoiscoci.h"
#include "../oci/sbnzoischarvardoci.h"
%}

%include "numpy.i"
%init %{
  srand(time(NULL));
  import_array();
%}


%apply (unsigned char* IN_ARRAY1, int DIM1)             {(unsigned char* inp,   int inp_size)}
%apply (unsigned char* IN_ARRAY1, int DIM1)             {(unsigned char* inp1,  int inp1_size)}
%apply (unsigned char* IN_ARRAY1, int DIM1)             {(unsigned char* inp2,  int inp2_size)}
%apply (unsigned char* IN_ARRAY2, int DIM1, int DIM2)   {(unsigned char* inp2d, int inp_size_1, int inp_size_2)}
%apply (unsigned short* IN_ARRAY1, int DIM1)            {(unsigned short* inp,   int inp_size)}
%apply (unsigned short* IN_ARRAY1, int DIM1)            {(unsigned short* inp1,  int inp1_size)}
%apply (unsigned short* IN_ARRAY1, int DIM1)            {(unsigned short* inp2,  int inp2_size)}
%apply (unsigned short* IN_ARRAY2, int DIM1, int DIM2)  {(unsigned short* inp2d, int inp_size_1, int inp_size_2)}
%apply (unsigned int* IN_ARRAY1, int DIM1)              {(unsigned int* inp,   int inp_size)}
%apply (unsigned int* IN_ARRAY1, int DIM1)              {(unsigned int* inp1,  int inp1_size)}
%apply (unsigned int* IN_ARRAY1, int DIM1)              {(unsigned int* inp2,  int inp2_size)}
%apply (unsigned int* IN_ARRAY2, int DIM1, int DIM2)    {(unsigned int* inp2d, int inp_size_1, int inp_size_2)}
%apply (double* IN_ARRAY1, int DIM1)                    {(double* inp,   int inp_size)}
%apply (double* IN_ARRAY1, int DIM1)                    {(double* inp1,  int inp1_size)}
%apply (double* IN_ARRAY1, int DIM1)                    {(double* inp2,  int inp2_size)}
%apply (double* IN_ARRAY2, int DIM1, int DIM2)          {(double* inp2d, int inp_size_1, int inp_size_2)}
%apply (float* IN_ARRAY1, int DIM1)                     {(float* inp,   int inp_size)}
%apply (float* IN_ARRAY1, int DIM1)                     {(float* inp1,  int inp1_size)}
%apply (float* IN_ARRAY1, int DIM1)                     {(float* inp2,  int inp2_size)}
%apply (float* IN_ARRAY2, int DIM1, int DIM2)           {(float* inp2d, int inp_size_1, int inp_size_2)}

%apply (unsigned char* ARGOUT_ARRAY1, int DIM1)  {(unsigned char* outp,  int outp_size)}
%apply (unsigned char* ARGOUT_ARRAY1, int DIM1)  {(unsigned char* outp1, int outp1_size)}
%apply (unsigned char* ARGOUT_ARRAY1, int DIM1)  {(unsigned char* outp2, int outp2_size)}
%apply (unsigned short* ARGOUT_ARRAY1, int DIM1) {(unsigned short* outp,  int outp_size)}
%apply (unsigned short* ARGOUT_ARRAY1, int DIM1) {(unsigned short* outp1, int outp1_size)}
%apply (unsigned short* ARGOUT_ARRAY1, int DIM1) {(unsigned short* outp2, int outp2_size)}
%apply (unsigned int* ARGOUT_ARRAY1, int DIM1)   {(unsigned int* outp,  int outp_size)}
%apply (unsigned int* ARGOUT_ARRAY1, int DIM1)   {(unsigned int* outp1, int outp1_size)}
%apply (unsigned int* ARGOUT_ARRAY1, int DIM1)   {(unsigned int* outp2, int outp2_size)}
%apply (double* ARGOUT_ARRAY1, int DIM1)         {(double* outp,  int outp_size)}
%apply (double* ARGOUT_ARRAY1, int DIM1)         {(double* outp1, int outp1_size)}
%apply (double* ARGOUT_ARRAY1, int DIM1)         {(double* outp2, int outp2_size)}
%apply (float* ARGOUT_ARRAY1, int DIM1)          {(float* outp,  int outp_size)}
%apply (float* ARGOUT_ARRAY1, int DIM1)          {(float* outp1, int outp1_size)}
%apply (float* ARGOUT_ARRAY1, int DIM1)          {(float* outp2, int outp2_size)}

%apply (unsigned char* INPLACE_ARRAY1, int DIM1)  {(unsigned char* inpl,  int inpl_size)}
%apply (unsigned char* INPLACE_ARRAY1, int DIM1)  {(unsigned char* inpl1, int inpl1_size)}
%apply (unsigned char* INPLACE_ARRAY1, int DIM1)  {(unsigned char* inpl2, int inpl2_size)}
%apply (unsigned short* INPLACE_ARRAY1, int DIM1) {(unsigned short* inpl,  int inpl_size)}
%apply (unsigned short* INPLACE_ARRAY1, int DIM1) {(unsigned short* inpl1, int inpl1_size)}
%apply (unsigned short* INPLACE_ARRAY1, int DIM1) {(unsigned short* inpl2, int inpl2_size)}
%apply (unsigned int* INPLACE_ARRAY1, int DIM1)   {(unsigned int* inpl,  int inpl_size)}
%apply (unsigned int* INPLACE_ARRAY1, int DIM1)   {(unsigned int* inpl1, int inpl1_size)}
%apply (unsigned int* INPLACE_ARRAY1, int DIM1)   {(unsigned int* inpl2, int inpl2_size)}
%apply (double* INPLACE_ARRAY1, int DIM1)         {(double* inpl,  int inpl_size)}
%apply (double* INPLACE_ARRAY1, int DIM1)         {(double* inpl1, int inpl1_size)}
%apply (double* INPLACE_ARRAY1, int DIM1)         {(double* inpl2, int inpl2_size)}
%apply (float* INPLACE_ARRAY1, int DIM1)          {(float* inpl,  int inpl_size)}
%apply (float* INPLACE_ARRAY1, int DIM1)          {(float* inpl1, int inpl1_size)}
%apply (float* INPLACE_ARRAY1, int DIM1)          {(float* inpl2, int inpl2_size)}


// Inclusions

%include "../bytearray.h"
%include "../selector.h"
%include "../descriptor.h"
%include "../fitness.h"
%include "../modelbuilder.h"
%include "../entropy.h"
  
%include "../oci/immediateoci.h"
%include "../oci/immediateharvardoci.h"
%include "../oci/indirectoci.h"
%include "../oci/testoci.h"
%include "../oci/loadstoreoci.h"
%include "../oci/stackoci.h"
%include "../oci/stackharvardoci.h"
%include "../oci/sbnzoiscoci.h"
%include "../oci/sbnzoischarvardoci.h"