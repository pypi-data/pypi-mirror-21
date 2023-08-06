/**
 * Genotype selector.
 * An extension to the roulette wheel choosing algorithm, which builds
 * hypothetical best-case children and chooses every father based on those.
 *
 * \author: Csaba Sulyok
 */

#pragma once


/**
 * Complementary genotype selector.
 * Uses roulette-wheel selection for each mother, and builds hypothetical best-case
 * children with each potential father, then chooses father based on a roulette-wheel of children.
 */
class ComplementaryGenotypeSelector
{
public:

  ComplementaryGenotypeSelector(unsigned short numUnits, unsigned short numTests, float minProb, float survivalProb);
  ~ComplementaryGenotypeSelector();


  /**
   * Normalizes a set of values so their sum is 1.
   * Effectively makes probabilities out of them.
   * The local minimal probability is taken into account, so all probabilities are
   * in between minProb and 1-minProb.
   */
  void probabilityUsingMinimal(float* inp,  int inp_size,
                               float* outp, int outp_size);


  /**
   * Select survivors and parents based on multi-objective fitness test grades.
   * Survivors are chosen randomly based on their overall grades.
   * Mothers are chosen based on roulette wheel,
   * and fathers are chosen based on roulette wheel of the hypothetical best-case
   * children with each mother.
   *
   * The return array contains survivor indices in the beginning (with the cut point being
   * the short return value), and the remaining numbers are mother/father indices.
   *
   * Inputs: grades, overall grades, ages and importances.
   * Output: units (indices)
   */
  unsigned short chooseUnits(float* inp2d,         int inp_size_1, int inp_size_2,
                             float* inp,           int inp_size,
                             unsigned short* inp1, int inp1_size,
                             float* inp2,          int inp2_size,
                             unsigned short* outp, int outp_size,
                             unsigned short maxAge);


  /**
   * Based on grades, selects some units to be survivors, based on random chance,
   * the probability being the grade.
   *
   * Input: A generation's overall grades + ages
   * Output: Survivor indices and count.
   */
  unsigned short selectSurvivors(float* inp1, int inp1_size,
                                 unsigned short* inp2, int inp2_size,
                                 unsigned short* outp, int outp_size,
                                 unsigned short maxAge);


private:
  /**
   * Number of units and tests in a population.
   */
  unsigned short _numUnits;
  unsigned short _numTests;

  /**
   * Minimal probability each unit has to be chosen.
   * All probabilities are scaled to be between
   */
  float _minProb;

  /**
   * Probability of survival.
   * This is taken together with overall grades, so every unit has this chance of survival
   * is their overall grades are 100%.
   */
  float _survivalProb;

  /**
   * Helper array to store hypothetical children's overall grades.
   * This will be used to choose fathers.
   */
  float*  _childOverallGrades;

  /**
   * Helper array to store CDFs of mother and father.
   * CDF of mother is of size _numUnits,
   * while CDF of father is of size _numUnits-1.
   */
  float*  _motherCum;
  float*  _fatherCum;

  /**
   * Choose a father, given a selected mother.
   * Builds hypothetical best-case children based on multi-objective fitness test results,
   * builds their CDF and chooses father based on it.
   */
  unsigned short _chooseFather(float* grades, int grades_size, unsigned short motherIdx, float* importances);
};


/**
 * Generates random float number uniformly distributed between 0 and 1.
 */
float randf();


/**
 * Makes a PDF into a CDF.
 * CDF(i) = sum(PDF(j)) where j=0:i.
 * Assumes input is already normalized.
 */
void cumulative(float* inpl, int inpl_size);


/**
 * Roulette-wheel selection.
 * Chooses an index from a CDF.
 * Generates a random number between 0 and 1 and returns the index from
 * the CDF where the random fits in.
 */
unsigned short chooseOneFromCumulative(float* inp, int inp_size);


/**
 * Choose multiple values from a CDF based on roulette-wheel.
 */
void chooseFromCumulative(float*          inp,  int inp_size,
                          unsigned short* outp, int outp_size);
