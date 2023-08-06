#pragma once

#include <stdio.h>

/**
 * Adapt fitness test importances based on a set of grades.
 *
 * If overall grades for a given fitness test are very high,
 * the importance for that test is lowered.
 *
 * If overall grades for a given fitness test are very low,
 * the importance for that test is made higher.
 *
 * The factor of lowering/heightening the importances is given by alpha.
 * The new importance i' for a test t becomes:
 *
 * i'(t) = (1-alpha) * i(t) + alpha * (1-mean(f(u,t)))
 */
void realignImportances(float* inpl,  int inpl_size,
                        float* inp2d, int inp_size_1, int inp_size_2,
                        float  alpha);
