/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine Stack.
 */


#include "stackoci.h"

#define ALLOCATION_UNIT 1024


StackOci::StackOci(unsigned int stackSize, unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed) :
	_stackSize(stackSize), _stackMask(stackSize-1), 
    _haltFlag(false), _maxCommands(maxCommands), _maxOutputs(maxOutputs), _haltAllowed(haltAllowed),
    _counter(0), _outputPtr(0), _outputAllocated(ALLOCATION_UNIT), _debug(false),
    _countOccurrences(false), _countTouched(false), _numTouched(0)
{
  _stack = new unsigned short[_stackSize];
  
  _touched = new unsigned short[_stackSize];
  
  _output = new unsigned char[_outputAllocated];

  _occurrences = new unsigned int[numCategories];
  
  _geneticStringSize = 4 + _stackSize * 2;
}


StackOci::~StackOci()
{
  delete [] _stack;
  delete [] _touched;
  delete [] _output;
  delete [] _occurrences;
}


void StackOci::_checkAndExtendOutput(unsigned char num)
{
  if (_outputPtr + num > _outputAllocated)
  {
    // TODO implement paging for efficiency
    _outputAllocated += ALLOCATION_UNIT;
    unsigned char* newOutput = new unsigned char[_outputAllocated];

    output(newOutput, _outputPtr);

    delete [] _output;
    _output = newOutput;
  }
}


void StackOci::setFromGeneticString(unsigned char* geneticString, int geneticString_size)
{
  _haltFlag = false;
  _outputPtr = 0;
  if (_countOccurrences)
  {
    _resetOccurrences();
  }
  if (_countTouched)
  {
    _resetTouched();
  }

  unsigned int genStrReadPtr = 0;
  unsigned int i;

  // set program counter
  _counter = ((unsigned short *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 2;

  // set register sp
  _sp = ((unsigned short *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 2;

  // set memory stack
  for (i = 0; i < _stackSize; ++i)
  {
    _stack[i] = ((unsigned short *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += _stackSize * 2;
}


void StackOci::interpret()
{
  _haltFlag = false;
  unsigned int numCommands = 0;
  //_counter = 0;
  _outputPtr = 0;

  while ((!_haltFlag || !_haltAllowed)
       && numCommands < _maxCommands
       && _outputPtr < _maxOutputs)
  {
    interpretNext();
    numCommands++;
  }
}


void StackOci::interpretN(unsigned int n)
{
  for (unsigned int i = 0; i < n; ++i)
  {
    interpretNext();
  }
}


void StackOci::interpretNext()
{
  _touch(_counter);
  unsigned char cmd = _stack[_counter];
  _counter = (_counter + 1) & _stackMask;
  
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      _interpret_0(cmd);
      break;
    }
  case 1:
    {
      _interpret_1(cmd);
      break;
    }
  }
}


void StackOci::_interpret_0(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      _interpret_00(cmd);
      break;
    }
  case 1:
    {
      _interpret_01(cmd);
      break;
    }
  }
}


void StackOci::_interpret_00(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("dup()\n");
      if (_countOccurrences) _occurrences[0]++;
      dup();
      break;
    }
  case 1:
    {
      if (_debug) printf("one()\n");
      if (_countOccurrences) _occurrences[0]++;
      one();
      break;
    }
  }
}


void StackOci::_interpret_01(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("zero()\n");
      if (_countOccurrences) _occurrences[0]++;
      zero();
      break;
    }
  case 1:
    {
      if (_debug) printf("load()\n");
      if (_countOccurrences) _occurrences[0]++;
      load();
      break;
    }
  }
}


void StackOci::_interpret_1(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      _interpret_10(cmd);
      break;
    }
  case 1:
    {
      _interpret_11(cmd);
      break;
    }
  }
}


void StackOci::_interpret_10(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("pop()\n");
      if (_countOccurrences) _occurrences[0]++;
      pop();
      break;
    }
  case 1:
    {
      if (_debug) printf("sub()\n");
      if (_countOccurrences) _occurrences[0]++;
      sub();
      break;
    }
  }
}


void StackOci::_interpret_11(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("jpos()\n");
      if (_countOccurrences) _occurrences[0]++;
      jpos();
      break;
    }
  case 1:
    {
      if (_debug) printf("out()\n");
      if (_countOccurrences) _occurrences[1]++;
      out();
      break;
    }
  }
}


void StackOci::_halt()
{
  _haltFlag = true;
}


void StackOci::_out(unsigned char byte)
{
  _checkAndExtendOutput();
  _output[_outputPtr++] = byte;
}


void StackOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num)
{
  _out(bytes, pos, num, _stackMask);
}


void StackOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num, unsigned int mask)
{
  _checkAndExtendOutput(num);
  for (int i = pos; i < pos + num; ++i)
  {
    _output[_outputPtr++] = bytes[i & mask];
  }
}


unsigned short& StackOci::_touch(unsigned int pos)
{
  if (_countTouched)
  {
  	if (_debug) printf("touch(%d)\n", pos);
    if (!_touched[pos & _stackMask]) 
    {
      _numTouched++;
    }
    _touched[pos & _stackMask]++;
  }
  return _stack[pos & _stackMask];
}


void StackOci::_resetOccurrences()
{
  memset(_occurrences, 0, numCategories * sizeof(unsigned int));
}

void StackOci::_resetTouched()
{
  _numTouched = 0;
  memset(_touched, 0, _stackSize * sizeof(unsigned short));
}

// ===============
// getters-setters
// ===============

const unsigned int StackOci::geneticStringSize() { return _geneticStringSize; }

unsigned short StackOci::counter() { return _counter; }
void StackOci::setCounter(unsigned short counter) { _counter = counter; }
unsigned int StackOci::outputPtr() { return _outputPtr; }
void StackOci::setOutputPtr(unsigned int outputPtr) { _outputPtr = outputPtr; }
unsigned short StackOci::sp() { return _sp; }
void StackOci::setSp(unsigned short sp) { _sp = sp; }

void StackOci::output(unsigned char* out_output, int out_output_size) { memcpy(out_output, _output, out_output_size); }
unsigned char StackOci::outputAt(unsigned short index) { return _output[index]; }
void StackOci::setOutput(unsigned char* in_output, int in_output_size) { memcpy(_output, in_output, in_output_size); }
void StackOci::setOutputAt(unsigned short index, unsigned char value) { _output[index] = value; }

void StackOci::stack(unsigned short* out_stack, int out_stack_size) { memcpy(out_stack, _stack, out_stack_size * sizeof(unsigned short)); }
unsigned short StackOci::stackAt(unsigned short index) { return _stack[index & _stackMask]; }
void StackOci::setStack(unsigned short* in_stack, int in_stack_size) { memcpy(_stack, in_stack, in_stack_size * sizeof(unsigned short)); }
void StackOci::setStackAt(unsigned short index, unsigned short value) { _stack[index & _stackMask] = value; }

bool StackOci::debug() { return _debug; }
void StackOci::setDebug(bool debug) { _debug = debug; }
bool StackOci::countOccurrences() { return _countOccurrences; }
void StackOci::setCountOccurrences(bool countOccurrences) { _countOccurrences = countOccurrences; }
bool StackOci::countTouched() { return _countTouched; }
void StackOci::setCountTouched(bool countTouched) { _countTouched = countTouched; }
int  StackOci::numTouched() { return _numTouched; }
void StackOci::setNumTouched(int numTouched) { _numTouched = numTouched; }

void StackOci::occurrences(unsigned int* out_occurrences, int out_occurrences_size) { memcpy(out_occurrences, _occurrences, out_occurrences_size * sizeof(unsigned int)); }
unsigned int StackOci::occurrencesAt(unsigned short index) { return _occurrences[index]; }
void StackOci::setOccurrences(unsigned int* in_occurrences, int in_occurrences_size) { memcpy(_occurrences, in_occurrences, in_occurrences_size * sizeof(unsigned int)); }
void StackOci::setOccurrencesAt(unsigned short index, unsigned int value) { _occurrences[index] = value; }

void StackOci::touched(unsigned short* out_touched, int out_touched_size) { memcpy(out_touched, _touched, out_touched_size * sizeof(unsigned short)); }
unsigned short StackOci::touchedAt(unsigned short index) { return _touched[index]; }
void StackOci::setTouched(unsigned short* in_touched, int in_touched_size) { memcpy(_touched, in_touched, in_touched_size * sizeof(unsigned short)); }
void StackOci::setTouchedAt(unsigned short index, unsigned short value) { _touched[index] = value; }
