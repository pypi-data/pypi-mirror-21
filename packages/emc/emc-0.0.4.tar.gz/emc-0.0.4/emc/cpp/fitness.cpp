#include "fitness.h"


void realignImportances(float* importances, int num_importances, float* grades, int num_units, int num_tests, float alpha)
{
  float meanGrades;
  float sumImportances = 0.0f;


  for (int testIdx = 0; testIdx < num_tests; ++testIdx)
  {
    meanGrades = 0.0f;

    for (int unitIdx = 0; unitIdx < num_units; ++unitIdx)
    {
      meanGrades += grades[unitIdx * num_tests + testIdx];
    }

    meanGrades /= num_units;

    importances[testIdx] = (1.0f - alpha) * importances[testIdx]
                         + alpha          * (1.0f - meanGrades);
    sumImportances += importances[testIdx];
  }


  for (int testIdx = 0; testIdx < num_tests; ++testIdx)
  {
    importances[testIdx] /= sumImportances;
  }
}
