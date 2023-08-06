#include "example.h"

#include <iostream>
using namespace std;


void exampleMethod()
{
  cout << "The C++ example method" << endl;
}


void exampleMethodWithNumPy(unsigned char* input, int input_size)
{
  cout << "The C++ NumPy example method: " << (short) input[0];
  for (int i = 1; i < input_size; ++i)
  {
    cout << ", " << (short) input[i];
  }
  cout << endl;
}


ExampleClass::ExampleClass(double exampleProp) :
    _exampleProp(exampleProp) {}


void ExampleClass::printProp()
{
  cout << "The C++ class example method: " << _exampleProp << endl;
}


void ExampleClass::printArrayTimesProp(double* input, int input_size)
{
  cout << "The C++ class NumPy example method: " << _exampleProp * input[0];
  for (int i = 1; i < input_size; ++i)
  {
    cout << ", " << _exampleProp * input[i];
  }
  cout << endl;
}
