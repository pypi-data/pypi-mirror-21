#pragma once


/**
 * Example module for EMC C++ module used in Python code.
 */


void exampleMethod();

void exampleMethodWithNumPy(unsigned char* input, int input_size);

class ExampleClass
{
public:
  ExampleClass(double exampleProp = 42.0);
  void printProp();
  void printArrayTimesProp(double* input, int input_size);
private:
  double _exampleProp;
};
