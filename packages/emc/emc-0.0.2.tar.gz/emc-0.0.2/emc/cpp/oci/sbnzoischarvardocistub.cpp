/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine SbnzOiscHarvard.
 */


#include "sbnzoischarvardoci.h"

#define ALLOCATION_UNIT 1024


SbnzOiscHarvardOci::SbnzOiscHarvardOci(unsigned int ramSize, unsigned int romSize, unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed) :
	_ramSize(ramSize), _ramMask(ramSize-1), _romSize(romSize), _romMask(romSize-1), 
    _haltFlag(false), _maxCommands(maxCommands), _maxOutputs(maxOutputs), _haltAllowed(haltAllowed),
    _counter(0), _outputPtr(0), _outputAllocated(ALLOCATION_UNIT), _debug(false),
    _countOccurrences(false), _countTouched(false), _numTouched(0)
{
  _ram = new unsigned short[_ramSize];
  _rom = new unsigned short[_romSize];
  
  _touched = new unsigned short[_romSize];
  
  _output = new unsigned char[_outputAllocated];

  _occurrences = new unsigned int[numCategories];
  
  _geneticStringSize = 2 + _ramSize * 2 + _romSize * 2;
}


SbnzOiscHarvardOci::~SbnzOiscHarvardOci()
{
  delete [] _ram;
  delete [] _rom;
  delete [] _touched;
  delete [] _output;
  delete [] _occurrences;
}


void SbnzOiscHarvardOci::_checkAndExtendOutput(unsigned char num)
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


void SbnzOiscHarvardOci::setFromGeneticString(unsigned char* geneticString, int geneticString_size)
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

  // set memory rom
  for (i = 0; i < _romSize; ++i)
  {
    _rom[i] = ((unsigned short *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += _romSize * 2;
}


void SbnzOiscHarvardOci::interpret()
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


void SbnzOiscHarvardOci::interpretN(unsigned int n)
{
  for (unsigned int i = 0; i < n; ++i)
  {
    sbnz();
  }
}


void SbnzOiscHarvardOci::_halt()
{
  _haltFlag = true;
}


void SbnzOiscHarvardOci::_out(unsigned char byte)
{
  _checkAndExtendOutput();
  _output[_outputPtr++] = byte;
}


void SbnzOiscHarvardOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num)
{
  _out(bytes, pos, num, _romMask);
}


void SbnzOiscHarvardOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num, unsigned int mask)
{
  _checkAndExtendOutput(num);
  for (int i = pos; i < pos + num; ++i)
  {
    _output[_outputPtr++] = bytes[i & mask];
  }
}


unsigned short& SbnzOiscHarvardOci::_touch(unsigned int pos)
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


void SbnzOiscHarvardOci::_resetOccurrences()
{
  memset(_occurrences, 0, numCategories * sizeof(unsigned int));
}

void SbnzOiscHarvardOci::_resetTouched()
{
  _numTouched = 0;
  memset(_touched, 0, _romSize * sizeof(unsigned short));
}

// ===============
// getters-setters
// ===============

const unsigned int SbnzOiscHarvardOci::geneticStringSize() { return _geneticStringSize; }

unsigned short SbnzOiscHarvardOci::counter() { return _counter; }
void SbnzOiscHarvardOci::setCounter(unsigned short counter) { _counter = counter; }
unsigned int SbnzOiscHarvardOci::outputPtr() { return _outputPtr; }
void SbnzOiscHarvardOci::setOutputPtr(unsigned int outputPtr) { _outputPtr = outputPtr; }

void SbnzOiscHarvardOci::output(unsigned char* out_output, int out_output_size) { memcpy(out_output, _output, out_output_size); }
unsigned char SbnzOiscHarvardOci::outputAt(unsigned short index) { return _output[index]; }
void SbnzOiscHarvardOci::setOutput(unsigned char* in_output, int in_output_size) { memcpy(_output, in_output, in_output_size); }
void SbnzOiscHarvardOci::setOutputAt(unsigned short index, unsigned char value) { _output[index] = value; }

void SbnzOiscHarvardOci::ram(unsigned short* out_ram, int out_ram_size) { memcpy(out_ram, _ram, out_ram_size * sizeof(unsigned short)); }
unsigned short SbnzOiscHarvardOci::ramAt(unsigned short index) { return _ram[index & _ramMask]; }
void SbnzOiscHarvardOci::setRam(unsigned short* in_ram, int in_ram_size) { memcpy(_ram, in_ram, in_ram_size * sizeof(unsigned short)); }
void SbnzOiscHarvardOci::setRamAt(unsigned short index, unsigned short value) { _ram[index & _ramMask] = value; }

void SbnzOiscHarvardOci::rom(unsigned short* out_rom, int out_rom_size) { memcpy(out_rom, _rom, out_rom_size * sizeof(unsigned short)); }
unsigned short SbnzOiscHarvardOci::romAt(unsigned short index) { return _rom[index & _romMask]; }
void SbnzOiscHarvardOci::setRom(unsigned short* in_rom, int in_rom_size) { memcpy(_rom, in_rom, in_rom_size * sizeof(unsigned short)); }
void SbnzOiscHarvardOci::setRomAt(unsigned short index, unsigned short value) { _rom[index & _romMask] = value; }

bool SbnzOiscHarvardOci::debug() { return _debug; }
void SbnzOiscHarvardOci::setDebug(bool debug) { _debug = debug; }
bool SbnzOiscHarvardOci::countOccurrences() { return _countOccurrences; }
void SbnzOiscHarvardOci::setCountOccurrences(bool countOccurrences) { _countOccurrences = countOccurrences; }
bool SbnzOiscHarvardOci::countTouched() { return _countTouched; }
void SbnzOiscHarvardOci::setCountTouched(bool countTouched) { _countTouched = countTouched; }
int  SbnzOiscHarvardOci::numTouched() { return _numTouched; }
void SbnzOiscHarvardOci::setNumTouched(int numTouched) { _numTouched = numTouched; }

void SbnzOiscHarvardOci::occurrences(unsigned int* out_occurrences, int out_occurrences_size) { memcpy(out_occurrences, _occurrences, out_occurrences_size * sizeof(unsigned int)); }
unsigned int SbnzOiscHarvardOci::occurrencesAt(unsigned short index) { return _occurrences[index]; }
void SbnzOiscHarvardOci::setOccurrences(unsigned int* in_occurrences, int in_occurrences_size) { memcpy(_occurrences, in_occurrences, in_occurrences_size * sizeof(unsigned int)); }
void SbnzOiscHarvardOci::setOccurrencesAt(unsigned short index, unsigned int value) { _occurrences[index] = value; }

void SbnzOiscHarvardOci::touched(unsigned short* out_touched, int out_touched_size) { memcpy(out_touched, _touched, out_touched_size * sizeof(unsigned short)); }
unsigned short SbnzOiscHarvardOci::touchedAt(unsigned short index) { return _touched[index]; }
void SbnzOiscHarvardOci::setTouched(unsigned short* in_touched, int in_touched_size) { memcpy(_touched, in_touched, in_touched_size * sizeof(unsigned short)); }
void SbnzOiscHarvardOci::setTouchedAt(unsigned short index, unsigned short value) { _touched[index] = value; }
