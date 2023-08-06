/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine LoadStore.
 */


#include "loadstoreoci.h"

#define ALLOCATION_UNIT 1024


LoadStoreOci::LoadStoreOci(unsigned int ramSize, unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed) :
	_ramSize(ramSize), _ramMask(ramSize-1), 
    _haltFlag(false), _maxCommands(maxCommands), _maxOutputs(maxOutputs), _haltAllowed(haltAllowed),
    _counter(0), _outputPtr(0), _outputAllocated(ALLOCATION_UNIT), _debug(false),
    _countOccurrences(false), _countTouched(false), _numTouched(0)
{
  _ram = new unsigned char[_ramSize];
  
  _touched = new unsigned short[_ramSize];
  
  _output = new unsigned char[_outputAllocated];

  _occurrences = new unsigned int[numCategories];
  
  _geneticStringSize = 7 + _ramSize;
}


LoadStoreOci::~LoadStoreOci()
{
  delete [] _ram;
  delete [] _touched;
  delete [] _output;
  delete [] _occurrences;
}


void LoadStoreOci::_checkAndExtendOutput(unsigned char num)
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


void LoadStoreOci::setFromGeneticString(unsigned char* geneticString, int geneticString_size)
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

  // set register a
  _a = ((unsigned char *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 1;

  // set register b
  _b = ((unsigned char *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 1;

  // set register flags
  _flags = ((unsigned char *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 1;

  // set register addr
  _addr = ((unsigned short *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 2;

  // set memory ram
  for (i = 0; i < _ramSize; ++i)
  {
    _ram[i] = ((unsigned char *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += _ramSize;
}


void LoadStoreOci::interpret()
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


void LoadStoreOci::interpretN(unsigned int n)
{
  for (unsigned int i = 0; i < n; ++i)
  {
    interpretNext();
  }
}


void LoadStoreOci::interpretNext()
{
  _touch(_counter);
  unsigned char cmd = _ram[_counter];
  _counter = (_counter + 1) & _ramMask;
  
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


void LoadStoreOci::_interpret_0(unsigned char cmd)
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


void LoadStoreOci::_interpret_00(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      _interpret_000(cmd);
      break;
    }
  case 1:
    {
      _interpret_001(cmd);
      break;
    }
  }
}


void LoadStoreOci::_interpret_000(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("mov_a_addr()\n");
      if (_countOccurrences) _occurrences[0]++;
      mov_a_addr();
      break;
    }
  case 1:
    {
      if (_debug) printf("mov_b_addr()\n");
      if (_countOccurrences) _occurrences[0]++;
      mov_b_addr();
      break;
    }
  }
}


void LoadStoreOci::_interpret_001(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("mov_addr_a()\n");
      if (_countOccurrences) _occurrences[0]++;
      mov_addr_a();
      break;
    }
  case 1:
    {
      if (_debug) printf("mov_addr_b()\n");
      if (_countOccurrences) _occurrences[0]++;
      mov_addr_b();
      break;
    }
  }
}


void LoadStoreOci::_interpret_01(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      _interpret_010(cmd);
      break;
    }
  case 1:
    {
      if (_debug) printf("jnc_addr()\n");
      if (_countOccurrences) _occurrences[0]++;
      jnc_addr();
      break;
    }
  }
}


void LoadStoreOci::_interpret_010(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("mov_addrl_a()\n");
      if (_countOccurrences) _occurrences[0]++;
      mov_addrl_a();
      break;
    }
  case 1:
    {
      if (_debug) printf("mov_addrh_a()\n");
      if (_countOccurrences) _occurrences[0]++;
      mov_addrh_a();
      break;
    }
  }
}


void LoadStoreOci::_interpret_1(unsigned char cmd)
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


void LoadStoreOci::_interpret_10(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      _interpret_100(cmd);
      break;
    }
  case 1:
    {
      _interpret_101(cmd);
      break;
    }
  }
}


void LoadStoreOci::_interpret_100(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("subb()\n");
      if (_countOccurrences) _occurrences[0]++;
      subb();
      break;
    }
  case 1:
    {
      if (_debug) printf("cpl_a()\n");
      if (_countOccurrences) _occurrences[0]++;
      cpl_a();
      break;
    }
  }
}


void LoadStoreOci::_interpret_101(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("clr_c()\n");
      if (_countOccurrences) _occurrences[0]++;
      clr_c();
      break;
    }
  case 1:
    {
      if (_debug) printf("cpl_c()\n");
      if (_countOccurrences) _occurrences[0]++;
      cpl_c();
      break;
    }
  }
}


void LoadStoreOci::_interpret_11(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      _interpret_110(cmd);
      break;
    }
  case 1:
    {
      if (_debug) printf("out_a()\n");
      if (_countOccurrences) _occurrences[1]++;
      out_a();
      break;
    }
  }
}


void LoadStoreOci::_interpret_110(unsigned char cmd)
{
  unsigned char i = cmd >> 7;
  cmd = cmd << 1;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("andl()\n");
      if (_countOccurrences) _occurrences[0]++;
      andl();
      break;
    }
  case 1:
    {
      if (_debug) printf("norl()\n");
      if (_countOccurrences) _occurrences[0]++;
      norl();
      break;
    }
  }
}


void LoadStoreOci::_halt()
{
  _haltFlag = true;
}


void LoadStoreOci::_out(unsigned char byte)
{
  _checkAndExtendOutput();
  _output[_outputPtr++] = byte;
}


void LoadStoreOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num)
{
  _out(bytes, pos, num, _ramMask);
}


void LoadStoreOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num, unsigned int mask)
{
  _checkAndExtendOutput(num);
  for (int i = pos; i < pos + num; ++i)
  {
    _output[_outputPtr++] = bytes[i & mask];
  }
}


unsigned char& LoadStoreOci::_touch(unsigned int pos)
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


void LoadStoreOci::_resetOccurrences()
{
  memset(_occurrences, 0, numCategories * sizeof(unsigned int));
}

void LoadStoreOci::_resetTouched()
{
  _numTouched = 0;
  memset(_touched, 0, _ramSize * sizeof(unsigned short));
}

// ===============
// getters-setters
// ===============

const unsigned int LoadStoreOci::geneticStringSize() { return _geneticStringSize; }

unsigned short LoadStoreOci::counter() { return _counter; }
void LoadStoreOci::setCounter(unsigned short counter) { _counter = counter; }
unsigned int LoadStoreOci::outputPtr() { return _outputPtr; }
void LoadStoreOci::setOutputPtr(unsigned int outputPtr) { _outputPtr = outputPtr; }
unsigned char LoadStoreOci::a() { return _a; }
void LoadStoreOci::setA(unsigned char a) { _a = a; }
unsigned char LoadStoreOci::b() { return _b; }
void LoadStoreOci::setB(unsigned char b) { _b = b; }
unsigned char LoadStoreOci::flags() { return _flags; }
void LoadStoreOci::setFlags(unsigned char flags) { _flags = flags; }
unsigned short LoadStoreOci::addr() { return _addr; }
void LoadStoreOci::setAddr(unsigned short addr) { _addr = addr; }

void LoadStoreOci::output(unsigned char* out_output, int out_output_size) { memcpy(out_output, _output, out_output_size); }
unsigned char LoadStoreOci::outputAt(unsigned short index) { return _output[index]; }
void LoadStoreOci::setOutput(unsigned char* in_output, int in_output_size) { memcpy(_output, in_output, in_output_size); }
void LoadStoreOci::setOutputAt(unsigned short index, unsigned char value) { _output[index] = value; }

void LoadStoreOci::ram(unsigned char* out_ram, int out_ram_size) { memcpy(out_ram, _ram, out_ram_size * sizeof(unsigned char)); }
unsigned char LoadStoreOci::ramAt(unsigned short index) { return _ram[index & _ramMask]; }
void LoadStoreOci::setRam(unsigned char* in_ram, int in_ram_size) { memcpy(_ram, in_ram, in_ram_size * sizeof(unsigned char)); }
void LoadStoreOci::setRamAt(unsigned short index, unsigned char value) { _ram[index & _ramMask] = value; }

bool LoadStoreOci::debug() { return _debug; }
void LoadStoreOci::setDebug(bool debug) { _debug = debug; }
bool LoadStoreOci::countOccurrences() { return _countOccurrences; }
void LoadStoreOci::setCountOccurrences(bool countOccurrences) { _countOccurrences = countOccurrences; }
bool LoadStoreOci::countTouched() { return _countTouched; }
void LoadStoreOci::setCountTouched(bool countTouched) { _countTouched = countTouched; }
int  LoadStoreOci::numTouched() { return _numTouched; }
void LoadStoreOci::setNumTouched(int numTouched) { _numTouched = numTouched; }

void LoadStoreOci::occurrences(unsigned int* out_occurrences, int out_occurrences_size) { memcpy(out_occurrences, _occurrences, out_occurrences_size * sizeof(unsigned int)); }
unsigned int LoadStoreOci::occurrencesAt(unsigned short index) { return _occurrences[index]; }
void LoadStoreOci::setOccurrences(unsigned int* in_occurrences, int in_occurrences_size) { memcpy(_occurrences, in_occurrences, in_occurrences_size * sizeof(unsigned int)); }
void LoadStoreOci::setOccurrencesAt(unsigned short index, unsigned int value) { _occurrences[index] = value; }

void LoadStoreOci::touched(unsigned short* out_touched, int out_touched_size) { memcpy(out_touched, _touched, out_touched_size * sizeof(unsigned short)); }
unsigned short LoadStoreOci::touchedAt(unsigned short index) { return _touched[index]; }
void LoadStoreOci::setTouched(unsigned short* in_touched, int in_touched_size) { memcpy(_touched, in_touched, in_touched_size * sizeof(unsigned short)); }
void LoadStoreOci::setTouchedAt(unsigned short index, unsigned short value) { _touched[index] = value; }
