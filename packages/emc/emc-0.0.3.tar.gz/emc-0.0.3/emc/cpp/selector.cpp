#include "selector.h"

#include <stdio.h>
#include <stdlib.h>


#define GRADES(i,j)          grades[i * _numTests + j]



ComplementaryGenotypeSelector::ComplementaryGenotypeSelector(unsigned short numUnits, unsigned short numTests,
                                                           float minProb, float survivalProb) :
    _numUnits(numUnits), _numTests(numTests), _minProb(minProb), _survivalProb(survivalProb)
{
  _childOverallGrades = new float[_numUnits - 1];
  _motherCum          = new float[_numUnits];
  _fatherCum          = new float[_numUnits - 1];
}


ComplementaryGenotypeSelector::~ComplementaryGenotypeSelector()
{
  delete [] _childOverallGrades;
  delete [] _motherCum;
  delete [] _fatherCum;
}


void ComplementaryGenotypeSelector::probabilityUsingMinimal(float* values, int values_size, float* probs, int probs_size)
{
  float sum = 0.0;

  for (int i = 0; i < values_size; ++i)
  {
    sum += values[i];
  }

  if (sum != 0)
  {
    for (int i = 0; i < values_size; ++i)
    {
      probs[i] = values[i] / sum;
    }
  }
  else
  {
    probs[0] = 1.0f / values_size;

    for (int i = 1; i < values_size; ++i)
    {
      probs[i] = probs[i-1];
    }
  }

  float scaledMinProb = _minProb / values_size;

  for (int i = 0; i < values_size; ++i)
  {
    probs[i] = (1.0f - _minProb) * probs[i] + scaledMinProb;
  }

  /*printf("Probs: [%.3f", probs[0]);
  for (int i = 1; i < values_size; ++i)
  {
    printf(", %.3f", probs[i]);
  }
  printf("]\n");*/
}


void cumulative(float* probs, int probs_size)
{
  for (int i = 1; i < probs_size; ++i)
  {
    probs[i] += probs[i-1];
  }
}



float randf()
{
  return (float) rand() / (float) RAND_MAX;
}


unsigned short chooseOneFromCumulative(float* cums, int cums_size)
{
  short ret = 0;
  float r = randf();
  while (r > cums[ret] && ret < cums_size - 1)
  {
    ret++;
  }
  return ret;
}



void chooseFromCumulative(float* cums, int cums_size, unsigned short* units, int units_size)
{
  for (int i = 0; i < units_size; ++i)
  {
    units[i] = chooseOneFromCumulative(cums, cums_size);
  }
}


unsigned short ComplementaryGenotypeSelector::selectSurvivors(float* overall_grades, int overall_grades_size,
                                                             unsigned short* ages, int ages_size,
                                                             unsigned short* units, int units_size,
                                                             unsigned short maxAge)
{
  unsigned short numSurvivors = 0;
  short maxUnchosenIdx = -1;

  for (int i = 0; i < overall_grades_size; ++i)
  {
    if (ages[i] < maxAge)
    {
      if (overall_grades[i] * _survivalProb > randf())
      {
        //printf("A survivor is you: %d\n", i);
        units[numSurvivors++] = i;
      }
      else if (maxUnchosenIdx < 0 || overall_grades[i] > overall_grades[maxUnchosenIdx])
      {
        maxUnchosenIdx = i;
      }
    }
  }

  // if odd number of survivors, use max unchosen to balance it out
  if ((numSurvivors & 1) != 0)
  {
    if (maxUnchosenIdx >= 0)
    {
      units[numSurvivors++] = maxUnchosenIdx;
    }
    else
    {
      printf("Error: Correct number of survivors could not be obtained. Behavior unpredictable.\n");
    }
  }

  return numSurvivors;
}


unsigned short ComplementaryGenotypeSelector::chooseUnits(float* grades,         int grades_size_1, int grades_size_2,
                                                         float* overall_grades, int overall_grades_size,
                                                         unsigned short* ages,  int ages_size,
                                                         float* importances,    int importances_size,
                                                         unsigned short* units, int units_size,
                                                         unsigned short maxAge)
{
  // select survivors
  unsigned short numSurvivors = selectSurvivors(overall_grades, overall_grades_size, ages, ages_size, units, units_size, maxAge);
  unsigned short numParents = (units_size - numSurvivors) / 2;

  // cumulative probabilities for mother
  probabilityUsingMinimal(overall_grades, grades_size_1, _motherCum, grades_size_1);
  cumulative(_motherCum, grades_size_1);

  // choose all mothers
  unsigned short* mothers = &(units[numSurvivors]);
  unsigned short* fathers = &(units[numSurvivors + numParents]);
  chooseFromCumulative(_motherCum, units_size, mothers, numParents);

  //for (int i = 0; i < numParents; ++i) printf("A mother is you: %d\n", mothers[i]);

  // for each mother, find father
  for (int i = 0; i < numParents; ++i)
  {
    fathers[i] = _chooseFather(grades, grades_size_1, mothers[i], importances);
    //printf("A father is you: %d\n", fathers[i]);
  }

  return numSurvivors;
}


unsigned short ComplementaryGenotypeSelector::_chooseFather(float* grades, int grades_size, unsigned short motherIdx, float* importances)
{
  int unitIdx;

  for (int childIdx = 0; childIdx < grades_size - 1; ++childIdx)
  {
    unitIdx = childIdx + (childIdx >= motherIdx);

    _childOverallGrades[childIdx] = 0.0;
    for (int testIdx = 0; testIdx < _numTests; ++testIdx)
    {
      _childOverallGrades[childIdx] += importances[testIdx] *
                                      (GRADES(unitIdx, testIdx) > GRADES(motherIdx, testIdx) ?
                                       GRADES(unitIdx, testIdx) : GRADES(motherIdx, testIdx));
    }
  }

  // build father cumulative probabilities
  probabilityUsingMinimal(_childOverallGrades, grades_size-1, _fatherCum, grades_size-1);
  cumulative(_fatherCum, grades_size-1);

  // choose father
  unsigned short ret = chooseOneFromCumulative(_fatherCum, grades_size-1);

  if (ret >= motherIdx)
  {
    ret++;
  }

  return ret;
}
