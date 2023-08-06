/**
 * Defines a descriptor for an EMC model, consisting of histograms and FFTs of the model information.
 * Also provides distancing methods, so a fitness can be built based on a correlation between model descriptors.
 *
 * \author Csaba Sulyok
 */


#pragma once

#include <math.h>
#include <stdio.h>
#include <fftw3.h>


/**
 * Number of descriptors, i.e. number of property analysis points.
 */
#define NUM_DESCRIPTORS 12


/**
 * Corpus of descriptors.
 * Corpus objects can be added to be cached here.
 * They will be clustered, and their cluster centers are saved.
 * Distancing methods are added to the cluster centers, and also the builder of a descriptor based on an EMC model.
 */
class DescriptorDirectory
{
public:

  DescriptorDirectory(int numModels, int numTracks, int numBins, int fourierSize, int numClusters);
  ~DescriptorDirectory();


  // ===============
  // public methods
  // ===============

  /**
   * Builds a model descriptor. It is a flattened matrix containing histogram and FFTs normalized to sum to 1.
   * Input: model notes array
   * Output: descriptor array
   */
  void trackDescriptor(unsigned short* inp2d, int inp_size_1, int inp_size_2, float* outp, int outp_size);


  /**
   * Calculates a model's descriptor and the correlations between it and the centre descriptors of the corpus.
   * Returns all correlations based on properties, numClusters for ioi histogram difference, numClusters for ioi fft difference, etc.
   */
  void trackCorrelationsWithCentres(unsigned short* inp2d, int inp_size_1, int inp_size_2, int trackIdx, float* outp, int outp_size);


  /**
   * Calculates the correlations between a descriptor and the centre descriptors of the corpus.
   * Returns all correlations based on properties, numClusters for ioi histogram difference, numClusters for ioi fft difference, etc.
   */
  void correlationsWithCentres(float* descriptor1, int descriptor1_size, int trackIdx, float* outp, int outp_size);


  /**
   * Returns fitness of a model.
   * Calculates correlations of the model's descriptor with the centre descriptors,
   * finds maximal correlation in each descriptor index, then calls fitness function to normalize output.
   */
  void trackFitness(unsigned short* inp2d, int inp_size_1, int inp_size_2, int trackIdx, float* outp, int outp_size, float gamma);



  /**
   * Add corpus model descriptor.
   * Calculates a descriptor of a given model and saves it as a reference descriptor, i.e. will be used in mean
   * calculation and distancing.
   */
  void addDescriptor(unsigned short* inp2d, int inp_size_1, int inp_size_2, int modelIdx, int trackIdx);


  /**
   * After all corpus models have been added via addDescriptor, this method performs K-means clustering on the corpus,
   * and saves the clusters' centres as the centre descriptors.
   * This will be used later in distancing.
   */
  void calculateCentreDescriptors();


  /**
   * Returns all descriptors, flattened into 1-D array.
   */
  void descriptors(float* outp, int outp_size);


  /**
   * Returns currently set centre descriptors. Copy is returned, so changing return value has no effect.
   * At this point, all corpus elements should be set (addDescriptor) and the mean should be calculated (calculateMeanDescriptor).
   */
  void centreDescriptors(float* outp, int outp_size);


  /**
   * Returns clusters - index of which cluster each reference descriptor has been classified into.
   */
  void clusters(unsigned short* outp, int outp_size);


  /**
   * Calculates FFT of data.
   * It is copied over to _fftInput, and zeropadded. An FFT is then performed on it.
   * Interleaved values of _fftOutput are then copied to the output.
   * Only returns magnitude of FFT.
   */
  void fourier(unsigned short* inpl, int inpl_size, float* outp, int outp_size, bool normalize);


  /**
   * Calculates FFT of first-order derivative of data.
   * The derivative is copied over to _fftInput, and zeropadded. An FFT is then performed on it.
   * Interleaved values of _fftOutput are then copied to the output.
   * Only returns magnitude of FFT.
   */
  void diffFourier(unsigned short* inpl, int inpl_size, float* outp, int outp_size, bool normalize);


private:

  /**
   * Number of models in corpus.
   */
  int _numModels;

  /**
   * Number of tracks per each model in corpus.
   * Must be universal in directory.
   */
  int _numTracks;

  /**
   * Number of bins the descriptors should have per property.
   * Effectively it is the size of histograms and FFTs.
   */
  int _numBins;

  /**
   * Size of input-output arrays of FFTs.
   */
  int _fourierSize;

  /**
   * Number of clusters to use for the classification the descriptors.
   * The centres of gravity of these clusters will be the references in fitness calculation.
   */
  int _numClusters;


  /**
   * Descriptors of the corpus.
   * D1 - model index
   * D2 - track index
   * D3 - descriptor index (size: number of descriptors * number of bins)
   */
  float*** _descriptors;

  /**
   * Indices of clusters each reference descriptor belongs to.
   * D1 - cluster index
   * D2 - track index
   * D3 - descriptor index (size: number of descriptors)
   */
  unsigned short*** _clusters;

  /**
   * Centre descriptors of all the descriptors within the corpus. Of size numClusters.
   * These are the centres of gravity of the clusters where the corpus has been classified.
   * D1 - cluster index
   * D2 - track index
   * D3 - descriptor index (size: number of descriptors * number of bins)
   */
  float*** _centreDescriptors;

  /**
   * Temporary space for correlations between a model/track and each cluster centre.
   * The minimal value of this array is used to calculate fitness.
   */
  float*  _tempCorrelations;

  /**
   * Temporary space for descriptors to be put when the descriptor itself is not of interest,
   * only the correlation is.
   */
  float*  _tempDescriptor;



  /**
   * Input for FFTs.
   * Any input we get from the outside is copied here.
   */
  float*         _fourierIn;

  /**
   * Output for FFTs.
   */
  fftwf_complex* _fourierOut;

  /**
   * FFTW plan for FFTs.
   */
  fftwf_plan     _fourierPlan;

  /**
   * Helper method to copy magnitude of resulting FFT in fftOutput to an output buffer.
   * Present to avoid duplicate code.
   */
  void _copyFourierOutput(float* output, int output_size);

};


// ==========================
// numerical analysis methods
// ==========================


/**
 * Normalizes data, i.e. the values will be scaled so that sum(data)=1.0
 */
void normalize    (float*          inpl, int inpl_size);


/**
 * Calculates histogram of data.
 * Based on an output size, counts instances of 0:output_size-1.
 * Optionally can normalize the output.
 */
void histogram    (unsigned short* inp, int inp_size, float* output, int output_size, bool normalize);


/**
 * Calculates histogram of first order differential of data.
 * Based on an output size, counts instances of 0:output_size-1 in differences between adjacent elements.
 * Optionally can normalize the output.
 */
void diffHistogram(unsigned short* inp, int inp_size, float* output, int output_size, bool normalize);


/**
 * Calculates the correlation between two descriptors.
 * Performs row-by-row differencing.
 */
void correlation  (float* inp1, int inp1_size, float* inp2, int inp2_size, float* outp, int outp_size, int num_bins);


/**
 * Calculates fitness values based on correlations. Assumes input array are correlations between descriptors.
 * A gamma value can be given to fine-tune the scale of the values.
 */
void fitness      (float* inpl, int inpl_size, float gamma);
