#include "descriptor.h"


#define SQRT2                    (float)1.41421356237
#define MAX_CLUSTER_ITERATIONS   50


DescriptorDirectory::DescriptorDirectory(int numModels, int numTracks, int numBins, int fourierSize, int numClusters) :
    _numModels(numModels), _numTracks(numTracks), _numBins(numBins), _fourierSize(fourierSize), _numClusters(numClusters)
{
  _descriptors = new float**[_numModels];
  _clusters    = new unsigned short**[_numModels];

  for (int modelIdx = 0; modelIdx < _numModels; ++modelIdx)
  {
    _descriptors[modelIdx] = new float*[_numTracks];
    _clusters[modelIdx]    = new unsigned short*[_numTracks];
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      _descriptors[modelIdx][trackIdx] = new float[NUM_DESCRIPTORS * _numBins];
      _clusters[modelIdx][trackIdx]    = new unsigned short[NUM_DESCRIPTORS];
    }
  }

  _centreDescriptors = new float**[_numClusters];

  for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
  {
    _centreDescriptors[clusterIdx] = new float*[_numTracks];
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      _centreDescriptors[clusterIdx][trackIdx] = new float[NUM_DESCRIPTORS * _numBins];
    }
  }

  _tempDescriptor = new float[NUM_DESCRIPTORS * _numBins];
  _tempCorrelations = new float[_numClusters * NUM_DESCRIPTORS];

  _fourierIn   = fftwf_alloc_real(_fourierSize);
  _fourierOut  = fftwf_alloc_complex(_fourierSize);
  _fourierPlan = fftwf_plan_dft_r2c_1d(_fourierSize, _fourierIn, _fourierOut, FFTW_ESTIMATE);
}


DescriptorDirectory::~DescriptorDirectory()
{

  for (int modelIdx = 0; modelIdx < _numModels; ++modelIdx)
  {
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      delete [] _descriptors[modelIdx][trackIdx];
      delete [] _clusters[modelIdx][trackIdx];
    }
    delete [] _descriptors[modelIdx];
    delete [] _clusters[modelIdx];
  }

  for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
  {
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      delete [] _centreDescriptors[clusterIdx][trackIdx];
    }
    delete [] _centreDescriptors[clusterIdx];
  }

  delete [] _descriptors;
  delete [] _clusters;
  delete [] _centreDescriptors;
  delete [] _tempCorrelations;
  delete [] _tempDescriptor;

  fftwf_destroy_plan(_fourierPlan);
  fftwf_free(_fourierIn);
  fftwf_free(_fourierOut);
}



// ====================
// Building descriptors
// ====================

void DescriptorDirectory::trackDescriptor(unsigned short* trackT, int num_props, int num_notes, float* descriptor, int descriptor_size)
{
  unsigned short* interonsets = &(trackT[num_notes * 0]);
  unsigned short* durations   = &(trackT[num_notes * 1]);
  unsigned short* pitches     = &(trackT[num_notes * 4]);

  histogram    (interonsets, num_notes, &(descriptor[0 * _numBins]), _numBins, false);
  diffHistogram(interonsets, num_notes, &(descriptor[1 * _numBins]), _numBins, false);
  fourier      (interonsets, num_notes, &(descriptor[2 * _numBins]), _numBins, false);
  diffFourier  (interonsets, num_notes, &(descriptor[3 * _numBins]), _numBins, false);
  histogram    (durations,   num_notes, &(descriptor[4 * _numBins]), _numBins, false);
  diffHistogram(durations,   num_notes, &(descriptor[5 * _numBins]), _numBins, false);
  fourier      (durations,   num_notes, &(descriptor[6 * _numBins]), _numBins, false);
  diffFourier  (durations,   num_notes, &(descriptor[7 * _numBins]), _numBins, false);
  histogram    (pitches,     num_notes, &(descriptor[8 * _numBins]), _numBins, false);
  diffHistogram(pitches,     num_notes, &(descriptor[9 * _numBins]), _numBins, false);
  fourier      (pitches,     num_notes, &(descriptor[10 * _numBins]), _numBins, false);
  diffFourier  (pitches,     num_notes, &(descriptor[11 * _numBins]), _numBins, false);
}


void DescriptorDirectory::addDescriptor(unsigned short* trackT, int num_props, int num_notes, int modelIdx, int trackIdx)
{
  trackDescriptor(trackT, num_props, num_notes, _descriptors[modelIdx][trackIdx], NUM_DESCRIPTORS * _numBins);
}


void DescriptorDirectory::calculateCentreDescriptors()
{
  // set all cluster indices to 0
  for (int modelIdx = 0; modelIdx < _numModels; ++modelIdx)
  {
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      for (int descriptorIdx = 0; descriptorIdx < NUM_DESCRIPTORS; ++descriptorIdx)
      {
        _clusters[modelIdx][trackIdx][descriptorIdx] = 0;
      }
    }
  }

  // allocate temporary space for correlations between all centers and models
  float*** allTempCorrelations = new float**[_numClusters];


  // set 1st descriptors as new cluster centers
  for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
  {
    allTempCorrelations[clusterIdx] = new float*[_numTracks];
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      allTempCorrelations[clusterIdx][trackIdx] = new float[_numModels];
      for (int idx = 0; idx < NUM_DESCRIPTORS * _numBins; ++idx)
      {
        _centreDescriptors[clusterIdx][trackIdx][idx] = _descriptors[clusterIdx][trackIdx][idx];
      }
    }
  }

  bool centersHaveChanged;
  int clusterIt;
  int numInCluster;


  for (int descriptorIdx = 0; descriptorIdx < NUM_DESCRIPTORS; ++descriptorIdx)
  {
    centersHaveChanged = true;
    clusterIt = 0;

    // do following steps until nothing changes from iteration to iteration
    // or until maximum iteration number is reached (to avoid oscillation infinite loop)
    while (centersHaveChanged && clusterIt < MAX_CLUSTER_ITERATIONS)
    {
      centersHaveChanged = false;

      // E-step
      // calculate correlations between centers and model descriptors
      for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
      {
        for (int modelIdx = 0; modelIdx < _numModels; ++modelIdx)
        {
          for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
          {
            correlation(&(_centreDescriptors [clusterIdx][trackIdx][descriptorIdx * _numBins]), _numBins,
                        &(_descriptors       [modelIdx]  [trackIdx][descriptorIdx * _numBins]), _numBins,
                        &(allTempCorrelations[clusterIdx][trackIdx][modelIdx]), 1,
                        _numBins);
          }
        }
      }

      // still E-step
      // classify each model as part of a cluster based on largest correlation
      for (int modelIdx = 0; modelIdx < _numModels; ++modelIdx)
      {
        for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
        {
          for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
          {
            if (allTempCorrelations[clusterIdx][trackIdx][modelIdx] > allTempCorrelations[_clusters[modelIdx][trackIdx][descriptorIdx]][trackIdx][modelIdx])
            {
              centersHaveChanged = true;
              _clusters[modelIdx][trackIdx][descriptorIdx] = clusterIdx;
            }
          }
        }
      }

      // M-step
      // calculate new centres of gravity, given the new clusters
      for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
      {
        for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
        {
          numInCluster = 0;

          for (int binIdx = 0; binIdx < _numBins; ++binIdx)
          {
            _centreDescriptors[clusterIdx][trackIdx][descriptorIdx * _numBins + binIdx] = 0;
          }

          // find models put into current cluster, and average them
          for (int modelIdx = 0; modelIdx < _numModels; ++modelIdx)
          {
            if (_clusters[modelIdx][trackIdx][descriptorIdx] == clusterIdx)
            {
              numInCluster++;
              for (int binIdx = 0; binIdx < _numBins; ++binIdx)
              {
                _centreDescriptors[clusterIdx][trackIdx][descriptorIdx * _numBins + binIdx] += _descriptors[modelIdx][trackIdx][descriptorIdx * _numBins + binIdx];
              }
            }
          }

          float invNumInCluster = (float)1.0 / (float)numInCluster;

          for (int binIdx = 0; binIdx < _numBins; ++binIdx)
          {
            _centreDescriptors[clusterIdx][trackIdx][descriptorIdx * _numBins + binIdx] *= invNumInCluster;
          }
        }
      }

      clusterIt++;
    }
  }


  // deallocate temporary space for correlations between all centers and models
  for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
  {
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      delete [] allTempCorrelations[clusterIdx][trackIdx];
    }
    delete [] allTempCorrelations[clusterIdx];
  }
  delete [] allTempCorrelations;
}



// =====================
// Calculating correlations
// =====================

void DescriptorDirectory::trackCorrelationsWithCentres(unsigned short* trackT, int num_props, int num_notes, int trackIdx, float* correlations, int num_correlations)
{
  trackDescriptor(trackT, num_props, num_notes, _tempDescriptor, NUM_DESCRIPTORS * _numBins);
  correlationsWithCentres(_tempDescriptor, NUM_DESCRIPTORS * _numBins, trackIdx, correlations, num_correlations);
}


void DescriptorDirectory::correlationsWithCentres(float* descriptor1, int descriptor1_size, int trackIdx, float* correlations, int num_correlations)
{
  for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
  {
    correlation(descriptor1, descriptor1_size, _centreDescriptors[clusterIdx][trackIdx], NUM_DESCRIPTORS * _numBins, &(correlations[clusterIdx * NUM_DESCRIPTORS]), NUM_DESCRIPTORS, _numBins);
  }
}


void correlation(float* x, int descriptor1_size, float* y, int descriptor2_size, float* correlations, int num_correlations, int n)
{
  float mux, muy, cov, std2x, std2y;

  for (int descriptorIdx = 0; descriptorIdx < num_correlations; ++descriptorIdx)
  {
    mux = muy = cov = std2x = std2y = 0.0;

    // 1. calculate means of data
    for (int i = 0; i < n; ++i)
    {
      mux += x[descriptorIdx * n + i];
      muy += y[descriptorIdx * n + i];
    }
    mux /= n;
    muy /= n;
    //printf("Mu_x = %.3f, Mu_y = %.3f\n", mux, muy);

    // 2. calculate covariance and standard deviations
    for (int i = 0; i < n; ++i)
    {
      cov   += (x[descriptorIdx * n + i] - mux) * (y[descriptorIdx * n + i] - muy);
      std2x += (x[descriptorIdx * n + i] - mux) * (x[descriptorIdx * n + i] - mux);
      std2y += (y[descriptorIdx * n + i] - muy) * (y[descriptorIdx * n + i] - muy);
    }
    //printf("Cov = %.3f, Std^2_x = %.3f, Std^2_y = %.3f\n", cov, std2x, std2y);

    // 3. calculate rho
    correlations[descriptorIdx] = cov / (sqrt(std2x) * sqrt(std2y));
    //printf("Corr = %.3f\n\n", correlations[descriptorIdx]);
  }
}



void DescriptorDirectory::trackFitness(unsigned short* trackT, int num_props, int num_notes, int trackIdx, float* data, int data_size, float gamma)
{
  trackCorrelationsWithCentres(trackT, num_props, num_notes, trackIdx, _tempCorrelations, _numClusters * NUM_DESCRIPTORS);

  for (int descriptorIdx = 0; descriptorIdx < NUM_DESCRIPTORS; ++descriptorIdx)
  {
    data[descriptorIdx] = 0;
    for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
    {
      if (_tempCorrelations[clusterIdx * NUM_DESCRIPTORS + descriptorIdx] > data[descriptorIdx])
      {
        data[descriptorIdx] = _tempCorrelations[clusterIdx * NUM_DESCRIPTORS + descriptorIdx];
      }
    }
  }

  fitness(data, data_size, gamma);
}


void fitness(float* data, int data_size, float gamma)
{
  for (int descriptorIdx = 0; descriptorIdx < data_size; ++descriptorIdx)
  {
    if (data[descriptorIdx] < 0)
    {
      data[descriptorIdx] = 0;
    }
    else
    {
      data[descriptorIdx] = pow(data[descriptorIdx], gamma);
    }
  }
}



// ========================
// Getters of prebuilt data
// ========================


void DescriptorDirectory::descriptors(float* descriptor, int descriptor_size)
{
  for (int modelIdx = 0; modelIdx < _numModels; ++modelIdx)
  {
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      for (int idx = 0; idx < NUM_DESCRIPTORS * _numBins; ++idx)
      {
        descriptor[modelIdx * _numTracks * NUM_DESCRIPTORS * _numBins +
                   trackIdx * NUM_DESCRIPTORS * _numBins +
                   idx] = _descriptors[modelIdx][trackIdx][idx];
      }
    }
  }
}


void DescriptorDirectory::centreDescriptors(float* descriptor, int descriptor_size)
{
  for (int clusterIdx = 0; clusterIdx < _numClusters; ++clusterIdx)
  {
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      for (int idx = 0; idx < NUM_DESCRIPTORS * _numBins; ++idx)
      {
        descriptor[clusterIdx * _numTracks * NUM_DESCRIPTORS * _numBins +
                   trackIdx * NUM_DESCRIPTORS * _numBins +
                   idx] = _centreDescriptors[clusterIdx][trackIdx][idx];
      }
    }
  }
}

void DescriptorDirectory::clusters(unsigned short* clusters, int clusters_size)
{
  for (int modelIdx = 0; modelIdx < _numModels; ++modelIdx)
  {
    for (int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
    {
      for (int descriptorIdx = 0; descriptorIdx < NUM_DESCRIPTORS; ++descriptorIdx)
      {
        clusters[modelIdx * _numTracks * NUM_DESCRIPTORS +
                 trackIdx * NUM_DESCRIPTORS +
                 descriptorIdx] = _clusters[modelIdx][trackIdx][descriptorIdx];
      }
    }
  }
}



// =======================
// General numeric methods
// =======================


void normalize(float* data, int data_size)
{
  float sum = 0.0;

  for (int i = 0; i < data_size; ++i)
  {
    sum += data[i];
  }

  if (sum != 0)
  {
    for (int i = 0; i < data_size; ++i)
    {
      data[i] /= sum;
    }
  }
  else
  {
    data[0] = 1.0f / data_size;

    for (int i = 1; i < data_size; ++i)
    {
      data[i] = data[i-1];
    }
  }
}


void histogram(unsigned short* data, int data_size, float* output, int output_size, bool normalizeFlag)
{
  for (int binIdx = 0; binIdx < output_size; ++binIdx)
  {
    output[binIdx] = 0;
  }

  for (int i = 0; i < data_size; ++i)
  {
    if (data[i] < output_size)
    {
      output[data[i]]++;
    }
  }

  if (normalizeFlag)
  {
    normalize(output, output_size);
  }
}


void diffHistogram(unsigned short* data, int data_size, float* output, int output_size, bool normalizeFlag)
{
  for (int binIdx = 0; binIdx < output_size; ++binIdx)
  {
    output[binIdx] = 0;
  }

  short diff;
  for (int i = 1; i < data_size; ++i)
  {
    diff = output_size / 2 + (data[i] - data[i-1]);
    if (diff >= 0 && diff < output_size)
    {
      output[diff]++;
    }
  }

  if (normalizeFlag)
  {
    normalize(output, output_size);
  }
}


void DescriptorDirectory::fourier(unsigned short* data, int data_size, float* output, int output_size, bool normalizeFlag)
{
  int i;
  for (i = 0; i < _fourierSize && i < data_size; ++i)
  {
    _fourierIn[i] = data[i];
  }
  for (; i < _fourierSize; ++i)
  {
    _fourierIn[i] = 0;
  }

  fftwf_execute(_fourierPlan);
  _copyFourierOutput(output, output_size);

  if (normalizeFlag)
  {
    normalize(output, output_size);
  }
}


void DescriptorDirectory::diffFourier(unsigned short* data, int data_size, float* output, int output_size, bool normalizeFlag)
{
  int i;
  for (i = 1; i < _fourierSize && i < data_size; ++i)
  {
    _fourierIn[i] = (float) (data[i] - data[i-1]);
  }
  for (; i < _fourierSize; ++i)
  {
    _fourierIn[i] = 0;
  }

  fftwf_execute(_fourierPlan);
  _copyFourierOutput(output, output_size);

  if (normalizeFlag)
  {
    normalize(output, output_size);
  }
}


void DescriptorDirectory::_copyFourierOutput(float* output, int output_size)
{
  /**
   * TODO Fix with LP here
   */
  int hopSize = _fourierSize / (2*output_size);
  hopSize = 8;
  // omit X[0]
  int i = hopSize;
  for (int o = 0; o < output_size; ++o)
  {
    output[o] = sqrt(_fourierOut[i][0] * _fourierOut[i][0] + _fourierOut[i][1] * _fourierOut[i][1]);
    i += hopSize;
  }
}
