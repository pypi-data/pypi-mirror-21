/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine Test.
 */


#include "testoci.h"

#define ALLOCATION_UNIT 1024


TestOci::TestOci(unsigned int ramSize, unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed) :
	_ramSize(ramSize), _ramMask(ramSize-1), 
    _haltFlag(false), _maxCommands(maxCommands), _maxOutputs(maxOutputs), _haltAllowed(haltAllowed),
    _counter(0), _outputPtr(0), _outputAllocated(ALLOCATION_UNIT), _debug(false),
    _countOccurrences(false), _countTouched(false), _numTouched(0)
{
  _registers = new unsigned char[numRegisters];
  
  _ram = new unsigned char[_ramSize];
  
  _stack = new unsigned char[16];
  _touched = new unsigned short[_ramSize];
  
  _output = new unsigned char[_outputAllocated];

  _occurrences = new unsigned int[numCategories];
  
  _geneticStringSize = 28 + _ramSize;
}


TestOci::~TestOci()
{
  delete [] _registers;
  delete [] _ram;
  delete [] _stack;
  delete [] _touched;
  delete [] _output;
  delete [] _occurrences;
}


void TestOci::_checkAndExtendOutput(unsigned char num)
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


void TestOci::setFromGeneticString(unsigned char* geneticString, int geneticString_size)
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
  _counter = ((unsigned char *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 1;

  // set main registers
  for (i = 0; i < numRegisters; ++i)
  {
    _registers[i] = geneticString[genStrReadPtr++];
  }

  // set register acc
  _acc = ((unsigned char *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 1;

  // set register dptr
  _dptr = ((unsigned short *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 2;

  // set memory ram
  for (i = 0; i < _ramSize; ++i)
  {
    _ram[i] = ((unsigned char *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += _ramSize;

  // set memory stack
  for (i = 0; i < 16; ++i)
  {
    _stack[i] = ((unsigned char *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += 16;
}


void TestOci::interpret()
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


void TestOci::interpretN(unsigned int n)
{
  for (unsigned int i = 0; i < n; ++i)
  {
    interpretNext();
  }
}


void TestOci::interpretNext()
{
  _touch(_counter);
  unsigned char cmd = _ram[_counter];
  _counter = (_counter + 1) & _ramMask;
  
  unsigned char i = cmd >> 6;
  cmd = cmd << 2;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("a()\n");
      if (_countOccurrences) _occurrences[0]++;
      a();
      break;
    }
  case 1:
    {
      unsigned char r1 = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("b(%d)\n", r1);
      if (_countOccurrences) _occurrences[0]++;
      b(r1);
      break;
    }
  case 2:
    {
      _interpret_10(cmd);
      break;
    }
  case 3:
    {
      unsigned char r1 = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("h(%d)\n", r1);
      if (_countOccurrences) _occurrences[1]++;
      h(r1);
      break;
    }
  }
}


void TestOci::_interpret_10(unsigned char cmd)
{
  unsigned char i = cmd >> 6;
  cmd = cmd << 2;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("c()\n");
      if (_countOccurrences) _occurrences[0]++;
      c();
      break;
    }
  case 1:
    {
      if (_debug) printf("d()\n");
      if (_countOccurrences) _occurrences[0]++;
      d();
      break;
    }
  case 2:
    {
      if (_debug) printf("e()\n");
      if (_countOccurrences) _occurrences[1]++;
      e();
      break;
    }
  case 3:
    {
      _interpret_1011(cmd);
      break;
    }
  }
}


void TestOci::_interpret_1011(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      unsigned char r1 = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("f(%d)\n", r1);
      if (_countOccurrences) _occurrences[1]++;
      f(r1);
      break;
    }
  case 1:
    {
      if (_debug) printf("g()\n");
      if (_countOccurrences) _occurrences[1]++;
      g();
      break;
    }
  }
}


void TestOci::_halt()
{
  _haltFlag = true;
}


void TestOci::_out(unsigned char byte)
{
  _checkAndExtendOutput();
  _output[_outputPtr++] = byte;
}


void TestOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num)
{
  _out(bytes, pos, num, _ramMask);
}


void TestOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num, unsigned int mask)
{
  _checkAndExtendOutput(num);
  for (int i = pos; i < pos + num; ++i)
  {
    _output[_outputPtr++] = bytes[i & mask];
  }
}


unsigned char& TestOci::_touch(unsigned int pos)
{
  if (_countTouched)
  {
  	if (_debug) printf("touch(%d)\n", pos);
    if (!_touched[pos & _ramMask]) 
    {
      _numTouched++;
    }
    _touched[pos & _ramMask]++;
  }
  return _ram[pos & _ramMask];
}


void TestOci::_resetOccurrences()
{
  memset(_occurrences, 0, numCategories * sizeof(unsigned int));
}

void TestOci::_resetTouched()
{
  _numTouched = 0;
  memset(_touched, 0, _ramSize * sizeof(unsigned short));
}

// ===============
// getters-setters
// ===============

const unsigned int TestOci::geneticStringSize() { return _geneticStringSize; }

unsigned char TestOci::counter() { return _counter; }
void TestOci::setCounter(unsigned char counter) { _counter = counter; }
unsigned int TestOci::outputPtr() { return _outputPtr; }
void TestOci::setOutputPtr(unsigned int outputPtr) { _outputPtr = outputPtr; }
unsigned char TestOci::acc() { return _acc; }
void TestOci::setAcc(unsigned char acc) { _acc = acc; }
unsigned short TestOci::dptr() { return _dptr; }
void TestOci::setDptr(unsigned short dptr) { _dptr = dptr; }

void TestOci::output(unsigned char* out_output, int out_output_size) { memcpy(out_output, _output, out_output_size); }
unsigned char TestOci::outputAt(unsigned short index) { return _output[index]; }
void TestOci::setOutput(unsigned char* in_output, int in_output_size) { memcpy(_output, in_output, in_output_size); }
void TestOci::setOutputAt(unsigned short index, unsigned char value) { _output[index] = value; }

void TestOci::registers(unsigned char* out_registers, int out_registers_size) { memcpy(out_registers, _registers, out_registers_size); }
unsigned char TestOci::registerAt(unsigned short index) { return _registers[index]; }
void TestOci::setRegisters(unsigned char* in_registers, int in_registers_size) { memcpy(_registers, in_registers, in_registers_size); }
void TestOci::setRegister(unsigned short index, unsigned char value) { _registers[index] = value; }

void TestOci::ram(unsigned char* out_ram, int out_ram_size) { memcpy(out_ram, _ram, out_ram_size * sizeof(unsigned char)); }
unsigned char TestOci::ramAt(unsigned short index) { return _ram[index & _ramMask]; }
void TestOci::setRam(unsigned char* in_ram, int in_ram_size) { memcpy(_ram, in_ram, in_ram_size * sizeof(unsigned char)); }
void TestOci::setRamAt(unsigned short index, unsigned char value) { _ram[index & _ramMask] = value; }

void TestOci::stack(unsigned char* out_stack, int out_stack_size) { memcpy(out_stack, _stack, out_stack_size); }
unsigned char TestOci::stackAt(unsigned short index) { return _stack[index]; }
void TestOci::setStack(unsigned char* in_stack, int in_stack_size) { memcpy(_stack, in_stack, in_stack_size); }
void TestOci::setStackAt(unsigned short index, unsigned char value) { _stack[index] = value; }

bool TestOci::debug() { return _debug; }
void TestOci::setDebug(bool debug) { _debug = debug; }
bool TestOci::countOccurrences() { return _countOccurrences; }
void TestOci::setCountOccurrences(bool countOccurrences) { _countOccurrences = countOccurrences; }
bool TestOci::countTouched() { return _countTouched; }
void TestOci::setCountTouched(bool countTouched) { _countTouched = countTouched; }
int  TestOci::numTouched() { return _numTouched; }
void TestOci::setNumTouched(int numTouched) { _numTouched = numTouched; }

void TestOci::occurrences(unsigned int* out_occurrences, int out_occurrences_size) { memcpy(out_occurrences, _occurrences, out_occurrences_size * sizeof(unsigned int)); }
unsigned int TestOci::occurrencesAt(unsigned short index) { return _occurrences[index]; }
void TestOci::setOccurrences(unsigned int* in_occurrences, int in_occurrences_size) { memcpy(_occurrences, in_occurrences, in_occurrences_size * sizeof(unsigned int)); }
void TestOci::setOccurrencesAt(unsigned short index, unsigned int value) { _occurrences[index] = value; }

void TestOci::touched(unsigned short* out_touched, int out_touched_size) { memcpy(out_touched, _touched, out_touched_size * sizeof(unsigned short)); }
unsigned short TestOci::touchedAt(unsigned short index) { return _touched[index]; }
void TestOci::setTouched(unsigned short* in_touched, int in_touched_size) { memcpy(_touched, in_touched, in_touched_size * sizeof(unsigned short)); }
void TestOci::setTouchedAt(unsigned short index, unsigned short value) { _touched[index] = value; }
