/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine SbnzOisc.
 */


#include "sbnzoiscoci.h"

#define ALLOCATION_UNIT 1024


SbnzOiscOci::SbnzOiscOci(unsigned int ramSize, unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed) :
	_ramSize(ramSize), _ramMask(ramSize-1), 
    _haltFlag(false), _maxCommands(maxCommands), _maxOutputs(maxOutputs), _haltAllowed(haltAllowed),
    _counter(0), _outputPtr(0), _outputAllocated(ALLOCATION_UNIT), _debug(false),
    _countOccurrences(false), _countTouched(false), _numTouched(0)
{
  _ram = new unsigned short[_ramSize];
  
  _touched = new unsigned short[_ramSize];
  
  _output = new unsigned char[_outputAllocated];

  _occurrences = new unsigned int[numCategories];
  
  _geneticStringSize = 2 + _ramSize * 2;
}


SbnzOiscOci::~SbnzOiscOci()
{
  delete [] _ram;
  delete [] _touched;
  delete [] _output;
  delete [] _occurrences;
}


void SbnzOiscOci::_checkAndExtendOutput(unsigned char num)
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


void SbnzOiscOci::setFromGeneticString(unsigned char* geneticString, int geneticString_size)
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

  // set memory ram
  for (i = 0; i < _ramSize; ++i)
  {
    _ram[i] = ((unsigned short *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += _ramSize * 2;
}


void SbnzOiscOci::interpret()
{
  _haltFlag = false;
  unsigned int numCommands = 0;
  //_counter = 0;
  _outputPtr = 0;

  while ((!_haltFlag || !_haltAllowed)
       && numCommands < _maxCommands
       && _outputPtr < _maxOutputs)
  {
    sbnz();
    numCommands++;
  }
}


void SbnzOiscOci::interpretN(unsigned int n)
{
  for (unsigned int i = 0; i < n; ++i)
  {
    sbnz();
  }
}


void SbnzOiscOci::_halt()
{
  _haltFlag = true;
}


void SbnzOiscOci::_out(unsigned char byte)
{
  _checkAndExtendOutput();
  _output[_outputPtr++] = byte;
}


void SbnzOiscOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num)
{
  _out(bytes, pos, num, _ramMask);
}


void SbnzOiscOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num, unsigned int mask)
{
  _checkAndExtendOutput(num);
  for (int i = pos; i < pos + num; ++i)
  {
    _output[_outputPtr++] = bytes[i & mask];
  }
}


unsigned short& SbnzOiscOci::_touch(unsigned int pos)
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


void SbnzOiscOci::_resetOccurrences()
{
  memset(_occurrences, 0, numCategories * sizeof(unsigned int));
}

void SbnzOiscOci::_resetTouched()
{
  _numTouched = 0;
  memset(_touched, 0, _ramSize * sizeof(unsigned short));
}

// ===============
// getters-setters
// ===============

const unsigned int SbnzOiscOci::geneticStringSize() { return _geneticStringSize; }

unsigned short SbnzOiscOci::counter() { return _counter; }
void SbnzOiscOci::setCounter(unsigned short counter) { _counter = counter; }
unsigned int SbnzOiscOci::outputPtr() { return _outputPtr; }
void SbnzOiscOci::setOutputPtr(unsigned int outputPtr) { _outputPtr = outputPtr; }

void SbnzOiscOci::output(unsigned char* out_output, int out_output_size) { memcpy(out_output, _output, out_output_size); }
unsigned char SbnzOiscOci::outputAt(unsigned short index) { return _output[index]; }
void SbnzOiscOci::setOutput(unsigned char* in_output, int in_output_size) { memcpy(_output, in_output, in_output_size); }
void SbnzOiscOci::setOutputAt(unsigned short index, unsigned char value) { _output[index] = value; }

void SbnzOiscOci::ram(unsigned short* out_ram, int out_ram_size) { memcpy(out_ram, _ram, out_ram_size * sizeof(unsigned short)); }
unsigned short SbnzOiscOci::ramAt(unsigned short index) { return _ram[index & _ramMask]; }
void SbnzOiscOci::setRam(unsigned short* in_ram, int in_ram_size) { memcpy(_ram, in_ram, in_ram_size * sizeof(unsigned short)); }
void SbnzOiscOci::setRamAt(unsigned short index, unsigned short value) { _ram[index & _ramMask] = value; }

bool SbnzOiscOci::debug() { return _debug; }
void SbnzOiscOci::setDebug(bool debug) { _debug = debug; }
bool SbnzOiscOci::countOccurrences() { return _countOccurrences; }
void SbnzOiscOci::setCountOccurrences(bool countOccurrences) { _countOccurrences = countOccurrences; }
bool SbnzOiscOci::countTouched() { return _countTouched; }
void SbnzOiscOci::setCountTouched(bool countTouched) { _countTouched = countTouched; }
int  SbnzOiscOci::numTouched() { return _numTouched; }
void SbnzOiscOci::setNumTouched(int numTouched) { _numTouched = numTouched; }

void SbnzOiscOci::occurrences(unsigned int* out_occurrences, int out_occurrences_size) { memcpy(out_occurrences, _occurrences, out_occurrences_size * sizeof(unsigned int)); }
unsigned int SbnzOiscOci::occurrencesAt(unsigned short index) { return _occurrences[index]; }
void SbnzOiscOci::setOccurrences(unsigned int* in_occurrences, int in_occurrences_size) { memcpy(_occurrences, in_occurrences, in_occurrences_size * sizeof(unsigned int)); }
void SbnzOiscOci::setOccurrencesAt(unsigned short index, unsigned int value) { _occurrences[index] = value; }

void SbnzOiscOci::touched(unsigned short* out_touched, int out_touched_size) { memcpy(out_touched, _touched, out_touched_size * sizeof(unsigned short)); }
unsigned short SbnzOiscOci::touchedAt(unsigned short index) { return _touched[index]; }
void SbnzOiscOci::setTouched(unsigned short* in_touched, int in_touched_size) { memcpy(_touched, in_touched, in_touched_size * sizeof(unsigned short)); }
void SbnzOiscOci::setTouchedAt(unsigned short index, unsigned short value) { _touched[index] = value; }
