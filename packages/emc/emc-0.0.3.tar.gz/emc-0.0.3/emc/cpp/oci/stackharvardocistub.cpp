/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine StackHarvard.
 */


#include "stackharvardoci.h"

#define ALLOCATION_UNIT 1024


StackHarvardOci::StackHarvardOci(unsigned int romSize, unsigned int stackSize, unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed) :
	_romSize(romSize), _romMask(romSize-1), _stackSize(stackSize), _stackMask(stackSize-1), 
    _haltFlag(false), _maxCommands(maxCommands), _maxOutputs(maxOutputs), _haltAllowed(haltAllowed),
    _counter(0), _outputPtr(0), _outputAllocated(ALLOCATION_UNIT), _debug(false),
    _countOccurrences(false), _countTouched(false), _numTouched(0)
{
  _rom = new unsigned short[_romSize];
  _stack = new unsigned short[_stackSize];
  
  _touched = new unsigned short[_romSize];
  
  _output = new unsigned char[_outputAllocated];

  _occurrences = new unsigned int[numCategories];
  
  _geneticStringSize = 4 + _romSize * 2 + _stackSize * 2;
}


StackHarvardOci::~StackHarvardOci()
{
  delete [] _rom;
  delete [] _stack;
  delete [] _touched;
  delete [] _output;
  delete [] _occurrences;
}


void StackHarvardOci::_checkAndExtendOutput(unsigned char num)
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


void StackHarvardOci::setFromGeneticString(unsigned char* geneticString, int geneticString_size)
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

  // set memory rom
  for (i = 0; i < _romSize; ++i)
  {
    _rom[i] = ((unsigned short *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += _romSize * 2;

  // set memory stack
  for (i = 0; i < _stackSize; ++i)
  {
    _stack[i] = ((unsigned short *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += _stackSize * 2;
}


void StackHarvardOci::interpret()
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


void StackHarvardOci::interpretN(unsigned int n)
{
  for (unsigned int i = 0; i < n; ++i)
  {
    interpretNext();
  }
}


void StackHarvardOci::interpretNext()
{
  _touch(_counter);
  unsigned char cmd = _rom[_counter];
  _counter = (_counter + 1) & _romMask;
  
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


void StackHarvardOci::_interpret_0(unsigned char cmd)
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


void StackHarvardOci::_interpret_00(unsigned char cmd)
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


void StackHarvardOci::_interpret_01(unsigned char cmd)
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


void StackHarvardOci::_interpret_1(unsigned char cmd)
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


void StackHarvardOci::_interpret_10(unsigned char cmd)
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


void StackHarvardOci::_interpret_11(unsigned char cmd)
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


void StackHarvardOci::_halt()
{
  _haltFlag = true;
}


void StackHarvardOci::_out(unsigned char byte)
{
  _checkAndExtendOutput();
  _output[_outputPtr++] = byte;
}


void StackHarvardOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num)
{
  _out(bytes, pos, num, _romMask);
}


void StackHarvardOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num, unsigned int mask)
{
  _checkAndExtendOutput(num);
  for (int i = pos; i < pos + num; ++i)
  {
    _output[_outputPtr++] = bytes[i & mask];
  }
}


unsigned short& StackHarvardOci::_touch(unsigned int pos)
{
  if (_countTouched)
  {
  	if (_debug) printf("touch(%d)\n", pos);
    if (!_touched[pos & _romMask]) 
    {
      _numTouched++;
    }
    _touched[pos & _romMask]++;
  }
  return _rom[pos & _romMask];
}


void StackHarvardOci::_resetOccurrences()
{
  memset(_occurrences, 0, numCategories * sizeof(unsigned int));
}

void StackHarvardOci::_resetTouched()
{
  _numTouched = 0;
  memset(_touched, 0, _romSize * sizeof(unsigned short));
}

// ===============
// getters-setters
// ===============

const unsigned int StackHarvardOci::geneticStringSize() { return _geneticStringSize; }

unsigned short StackHarvardOci::counter() { return _counter; }
void StackHarvardOci::setCounter(unsigned short counter) { _counter = counter; }
unsigned int StackHarvardOci::outputPtr() { return _outputPtr; }
void StackHarvardOci::setOutputPtr(unsigned int outputPtr) { _outputPtr = outputPtr; }
unsigned short StackHarvardOci::sp() { return _sp; }
void StackHarvardOci::setSp(unsigned short sp) { _sp = sp; }

void StackHarvardOci::output(unsigned char* out_output, int out_output_size) { memcpy(out_output, _output, out_output_size); }
unsigned char StackHarvardOci::outputAt(unsigned short index) { return _output[index]; }
void StackHarvardOci::setOutput(unsigned char* in_output, int in_output_size) { memcpy(_output, in_output, in_output_size); }
void StackHarvardOci::setOutputAt(unsigned short index, unsigned char value) { _output[index] = value; }

void StackHarvardOci::rom(unsigned short* out_rom, int out_rom_size) { memcpy(out_rom, _rom, out_rom_size * sizeof(unsigned short)); }
unsigned short StackHarvardOci::romAt(unsigned short index) { return _rom[index & _romMask]; }
void StackHarvardOci::setRom(unsigned short* in_rom, int in_rom_size) { memcpy(_rom, in_rom, in_rom_size * sizeof(unsigned short)); }
void StackHarvardOci::setRomAt(unsigned short index, unsigned short value) { _rom[index & _romMask] = value; }

void StackHarvardOci::stack(unsigned short* out_stack, int out_stack_size) { memcpy(out_stack, _stack, out_stack_size * sizeof(unsigned short)); }
unsigned short StackHarvardOci::stackAt(unsigned short index) { return _stack[index & _stackMask]; }
void StackHarvardOci::setStack(unsigned short* in_stack, int in_stack_size) { memcpy(_stack, in_stack, in_stack_size * sizeof(unsigned short)); }
void StackHarvardOci::setStackAt(unsigned short index, unsigned short value) { _stack[index & _stackMask] = value; }

bool StackHarvardOci::debug() { return _debug; }
void StackHarvardOci::setDebug(bool debug) { _debug = debug; }
bool StackHarvardOci::countOccurrences() { return _countOccurrences; }
void StackHarvardOci::setCountOccurrences(bool countOccurrences) { _countOccurrences = countOccurrences; }
bool StackHarvardOci::countTouched() { return _countTouched; }
void StackHarvardOci::setCountTouched(bool countTouched) { _countTouched = countTouched; }
int  StackHarvardOci::numTouched() { return _numTouched; }
void StackHarvardOci::setNumTouched(int numTouched) { _numTouched = numTouched; }

void StackHarvardOci::occurrences(unsigned int* out_occurrences, int out_occurrences_size) { memcpy(out_occurrences, _occurrences, out_occurrences_size * sizeof(unsigned int)); }
unsigned int StackHarvardOci::occurrencesAt(unsigned short index) { return _occurrences[index]; }
void StackHarvardOci::setOccurrences(unsigned int* in_occurrences, int in_occurrences_size) { memcpy(_occurrences, in_occurrences, in_occurrences_size * sizeof(unsigned int)); }
void StackHarvardOci::setOccurrencesAt(unsigned short index, unsigned int value) { _occurrences[index] = value; }

void StackHarvardOci::touched(unsigned short* out_touched, int out_touched_size) { memcpy(out_touched, _touched, out_touched_size * sizeof(unsigned short)); }
unsigned short StackHarvardOci::touchedAt(unsigned short index) { return _touched[index]; }
void StackHarvardOci::setTouched(unsigned short* in_touched, int in_touched_size) { memcpy(_touched, in_touched, in_touched_size * sizeof(unsigned short)); }
void StackHarvardOci::setTouchedAt(unsigned short index, unsigned short value) { _touched[index] = value; }
