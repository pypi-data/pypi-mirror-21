/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine Immediate.
 */


#include "immediateoci.h"

#define ALLOCATION_UNIT 1024


ImmediateOci::ImmediateOci(unsigned int ramSize, unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed) :
	_ramSize(ramSize), _ramMask(ramSize-1), 
    _haltFlag(false), _maxCommands(maxCommands), _maxOutputs(maxOutputs), _haltAllowed(haltAllowed),
    _counter(0), _outputPtr(0), _outputAllocated(ALLOCATION_UNIT), _debug(false),
    _countOccurrences(false), _countTouched(false), _numTouched(0)
{
  _registers = new unsigned char[numRegisters];
  
  _ram = new unsigned char[_ramSize];
  
  _stack = new unsigned char[256];
  _touched = new unsigned short[_ramSize];
  
  _output = new unsigned char[_outputAllocated];

  _occurrences = new unsigned int[numCategories];
  
  _geneticStringSize = 271 + _ramSize;
}


ImmediateOci::~ImmediateOci()
{
  delete [] _registers;
  delete [] _ram;
  delete [] _stack;
  delete [] _touched;
  delete [] _output;
  delete [] _occurrences;
}


void ImmediateOci::_checkAndExtendOutput(unsigned char num)
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


void ImmediateOci::setFromGeneticString(unsigned char* geneticString, int geneticString_size)
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

  // set main registers
  for (i = 0; i < numRegisters; ++i)
  {
    _registers[i] = geneticString[genStrReadPtr++];
  }

  // set register acc
  _acc = ((unsigned char *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 1;

  // set register dataPtr
  _dataPtr = ((unsigned short *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 2;

  // set register flags
  _flags = ((unsigned char *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 1;

  // set register stackPtr
  _stackPtr = ((unsigned char *) &(geneticString[genStrReadPtr]))[0];
  genStrReadPtr += 1;

  // set memory ram
  for (i = 0; i < _ramSize; ++i)
  {
    _ram[i] = ((unsigned char *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += _ramSize;

  // set memory stack
  for (i = 0; i < 256; ++i)
  {
    _stack[i] = ((unsigned char *) &(geneticString[genStrReadPtr]))[i];
  }
  genStrReadPtr += 256;
}


void ImmediateOci::interpret()
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


void ImmediateOci::interpretN(unsigned int n)
{
  for (unsigned int i = 0; i < n; ++i)
  {
    interpretNext();
  }
}


void ImmediateOci::interpretNext()
{
  _touch(_counter);
  unsigned char cmd = _ram[_counter];
  _counter = (_counter + 1) & _ramMask;
  
  unsigned char i = cmd >> 3;
  cmd = cmd << 5;
  
  switch (i)
  {
  case 0:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movR_DH(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movR_DH(r);
      break;
    }
  case 1:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movDH_R(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movDH_R(r);
      break;
    }
  case 2:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movR_DL(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movR_DL(r);
      break;
    }
  case 3:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movDL_R(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movDL_R(r);
      break;
    }
  case 4:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movR_DPtr(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movR_DPtr(r);
      break;
    }
  case 5:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("moviR_DPtr(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      moviR_DPtr(r);
      break;
    }
  case 6:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movDPtr_R(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movDPtr_R(r);
      break;
    }
  case 7:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("moviDPtr_R(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      moviDPtr_R(r);
      break;
    }
  case 8:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movR_Next(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movR_Next(r);
      break;
    }
  case 9:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movR_A(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movR_A(r);
      break;
    }
  case 10:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("movA_R(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      movA_R(r);
      break;
    }
  case 11:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("xchA_R(%d)\n", r);
      if (_countOccurrences) _occurrences[0]++;
      xchA_R(r);
      break;
    }
  case 12:
    {
      _interpret_01100(cmd);
      break;
    }
  case 13:
    {
      _interpret_01101(cmd);
      break;
    }
  case 14:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("inc_R(%d)\n", r);
      if (_countOccurrences) _occurrences[1]++;
      inc_R(r);
      break;
    }
  case 15:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("dec_R(%d)\n", r);
      if (_countOccurrences) _occurrences[1]++;
      dec_R(r);
      break;
    }
  case 16:
    {
      _interpret_10000(cmd);
      break;
    }
  case 17:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("anlA_R(%d)\n", r);
      if (_countOccurrences) _occurrences[1]++;
      anlA_R(r);
      break;
    }
  case 18:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("orlA_R(%d)\n", r);
      if (_countOccurrences) _occurrences[1]++;
      orlA_R(r);
      break;
    }
  case 19:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("addA_R(%d)\n", r);
      if (_countOccurrences) _occurrences[1]++;
      addA_R(r);
      break;
    }
  case 20:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("addcA_R(%d)\n", r);
      if (_countOccurrences) _occurrences[1]++;
      addcA_R(r);
      break;
    }
  case 21:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("subA_R(%d)\n", r);
      if (_countOccurrences) _occurrences[1]++;
      subA_R(r);
      break;
    }
  case 22:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("subbA_R(%d)\n", r);
      if (_countOccurrences) _occurrences[1]++;
      subbA_R(r);
      break;
    }
  case 23:
    {
      _interpret_10111(cmd);
      break;
    }
  case 24:
    {
      _interpret_11000(cmd);
      break;
    }
  case 25:
    {
      _interpret_11001(cmd);
      break;
    }
  case 26:
    {
      _interpret_11010(cmd);
      break;
    }
  case 27:
    {
      _interpret_11011(cmd);
      break;
    }
  case 28:
    {
      unsigned char r = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("outR(%d)\n", r);
      if (_countOccurrences) _occurrences[4]++;
      outR(r);
      break;
    }
  case 29:
    {
      unsigned char n = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("outDPtr(%d)\n", n);
      if (_countOccurrences) _occurrences[4]++;
      outDPtr(n);
      break;
    }
  case 30:
    {
      unsigned char n = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("outiDPtr(%d)\n", n);
      if (_countOccurrences) _occurrences[4]++;
      outiDPtr(n);
      break;
    }
  case 31:
    {
      unsigned char n = cmd >> 5; cmd = cmd << 3;
      if (_debug) printf("outNext(%d)\n", n);
      if (_countOccurrences) _occurrences[4]++;
      outNext(n);
      break;
    }
  }
}


void ImmediateOci::_interpret_01100(unsigned char cmd)
{
  unsigned char i = cmd >> 5;
  cmd = cmd << 3;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("movA_DH()\n");
      if (_countOccurrences) _occurrences[0]++;
      movA_DH();
      break;
    }
  case 1:
    {
      if (_debug) printf("movA_DL()\n");
      if (_countOccurrences) _occurrences[0]++;
      movA_DL();
      break;
    }
  case 2:
    {
      if (_debug) printf("movDH_A()\n");
      if (_countOccurrences) _occurrences[0]++;
      movDH_A();
      break;
    }
  case 3:
    {
      if (_debug) printf("movDL_A()\n");
      if (_countOccurrences) _occurrences[0]++;
      movDL_A();
      break;
    }
  case 4:
    {
      if (_debug) printf("movA_DPtr()\n");
      if (_countOccurrences) _occurrences[0]++;
      movA_DPtr();
      break;
    }
  case 5:
    {
      if (_debug) printf("moviA_DPtr()\n");
      if (_countOccurrences) _occurrences[0]++;
      moviA_DPtr();
      break;
    }
  case 6:
    {
      if (_debug) printf("movDPtr_A()\n");
      if (_countOccurrences) _occurrences[0]++;
      movDPtr_A();
      break;
    }
  case 7:
    {
      if (_debug) printf("moviDPtr_A()\n");
      if (_countOccurrences) _occurrences[0]++;
      moviDPtr_A();
      break;
    }
  }
}


void ImmediateOci::_interpret_01101(unsigned char cmd)
{
  unsigned char i = cmd >> 5;
  cmd = cmd << 3;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("xchA_DPtr()\n");
      if (_countOccurrences) _occurrences[0]++;
      xchA_DPtr();
      break;
    }
  case 1:
    {
      if (_debug) printf("xchiA_DPtr()\n");
      if (_countOccurrences) _occurrences[0]++;
      xchiA_DPtr();
      break;
    }
  case 2:
    {
      if (_debug) printf("movDPtr_Next()\n");
      if (_countOccurrences) _occurrences[0]++;
      movDPtr_Next();
      break;
    }
  case 3:
    {
      if (_debug) printf("movDH_Next()\n");
      if (_countOccurrences) _occurrences[0]++;
      movDH_Next();
      break;
    }
  case 4:
    {
      if (_debug) printf("movDL_Next()\n");
      if (_countOccurrences) _occurrences[0]++;
      movDL_Next();
      break;
    }
  case 5:
    {
      if (_debug) printf("movA_Next()\n");
      if (_countOccurrences) _occurrences[0]++;
      movA_Next();
      break;
    }
  case 6:
    {
      if (_debug) printf("cplC()\n");
      if (_countOccurrences) _occurrences[1]++;
      cplC();
      break;
    }
  case 7:
    {
      if (_debug) printf("inc_A()\n");
      if (_countOccurrences) _occurrences[1]++;
      inc_A();
      break;
    }
  }
}


void ImmediateOci::_interpret_10000(unsigned char cmd)
{
  unsigned char i = cmd >> 5;
  cmd = cmd << 3;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("dec_A()\n");
      if (_countOccurrences) _occurrences[1]++;
      dec_A();
      break;
    }
  case 1:
    {
      if (_debug) printf("inc_D()\n");
      if (_countOccurrences) _occurrences[1]++;
      inc_D();
      break;
    }
  case 2:
    {
      if (_debug) printf("dec_D()\n");
      if (_countOccurrences) _occurrences[1]++;
      dec_D();
      break;
    }
  case 3:
    {
      if (_debug) printf("cplA()\n");
      if (_countOccurrences) _occurrences[1]++;
      cplA();
      break;
    }
  case 4:
    {
      if (_debug) printf("anlA_Next()\n");
      if (_countOccurrences) _occurrences[1]++;
      anlA_Next();
      break;
    }
  case 5:
    {
      if (_debug) printf("orlA_Next()\n");
      if (_countOccurrences) _occurrences[1]++;
      orlA_Next();
      break;
    }
  case 6:
    {
      if (_debug) printf("anlA_DPtr()\n");
      if (_countOccurrences) _occurrences[1]++;
      anlA_DPtr();
      break;
    }
  case 7:
    {
      if (_debug) printf("orlA_DPtr()\n");
      if (_countOccurrences) _occurrences[1]++;
      orlA_DPtr();
      break;
    }
  }
}


void ImmediateOci::_interpret_10111(unsigned char cmd)
{
  unsigned char i = cmd >> 5;
  cmd = cmd << 3;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("addA_Next()\n");
      if (_countOccurrences) _occurrences[1]++;
      addA_Next();
      break;
    }
  case 1:
    {
      if (_debug) printf("addcA_Next()\n");
      if (_countOccurrences) _occurrences[1]++;
      addcA_Next();
      break;
    }
  case 2:
    {
      if (_debug) printf("subA_Next()\n");
      if (_countOccurrences) _occurrences[1]++;
      subA_Next();
      break;
    }
  case 3:
    {
      if (_debug) printf("subbA_Next()\n");
      if (_countOccurrences) _occurrences[1]++;
      subbA_Next();
      break;
    }
  case 4:
    {
      if (_debug) printf("addA_DPtr()\n");
      if (_countOccurrences) _occurrences[1]++;
      addA_DPtr();
      break;
    }
  case 5:
    {
      if (_debug) printf("addcA_DPtr()\n");
      if (_countOccurrences) _occurrences[1]++;
      addcA_DPtr();
      break;
    }
  case 6:
    {
      if (_debug) printf("subA_DPtr()\n");
      if (_countOccurrences) _occurrences[1]++;
      subA_DPtr();
      break;
    }
  case 7:
    {
      if (_debug) printf("subbA_DPtr()\n");
      if (_countOccurrences) _occurrences[1]++;
      subbA_DPtr();
      break;
    }
  }
}


void ImmediateOci::_interpret_11000(unsigned char cmd)
{
  unsigned char i = cmd >> 5;
  cmd = cmd << 3;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("rlA()\n");
      if (_countOccurrences) _occurrences[1]++;
      rlA();
      break;
    }
  case 1:
    {
      if (_debug) printf("rrA()\n");
      if (_countOccurrences) _occurrences[1]++;
      rrA();
      break;
    }
  case 2:
    {
      if (_debug) printf("rlcA()\n");
      if (_countOccurrences) _occurrences[1]++;
      rlcA();
      break;
    }
  case 3:
    {
      if (_debug) printf("rrcA()\n");
      if (_countOccurrences) _occurrences[1]++;
      rrcA();
      break;
    }
  case 4:
    {
      if (_debug) printf("pushDH()\n");
      if (_countOccurrences) _occurrences[2]++;
      pushDH();
      break;
    }
  case 5:
    {
      if (_debug) printf("popDH()\n");
      if (_countOccurrences) _occurrences[2]++;
      popDH();
      break;
    }
  case 6:
    {
      if (_debug) printf("pushDL()\n");
      if (_countOccurrences) _occurrences[2]++;
      pushDL();
      break;
    }
  case 7:
    {
      if (_debug) printf("popDL()\n");
      if (_countOccurrences) _occurrences[2]++;
      popDL();
      break;
    }
  }
}


void ImmediateOci::_interpret_11001(unsigned char cmd)
{
  unsigned char i = cmd >> 5;
  cmd = cmd << 3;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("pushA()\n");
      if (_countOccurrences) _occurrences[2]++;
      pushA();
      break;
    }
  case 1:
    {
      if (_debug) printf("popA()\n");
      if (_countOccurrences) _occurrences[2]++;
      popA();
      break;
    }
  case 2:
    {
      if (_debug) printf("sjmpNext()\n");
      if (_countOccurrences) _occurrences[3]++;
      sjmpNext();
      break;
    }
  case 3:
    {
      if (_debug) printf("jmpNext()\n");
      if (_countOccurrences) _occurrences[3]++;
      jmpNext();
      break;
    }
  case 4:
    {
      if (_debug) printf("jmpD()\n");
      if (_countOccurrences) _occurrences[3]++;
      jmpD();
      break;
    }
  case 5:
    {
      if (_debug) printf("callD()\n");
      if (_countOccurrences) _occurrences[3]++;
      callD();
      break;
    }
  case 6:
    {
      if (_debug) printf("callNext()\n");
      if (_countOccurrences) _occurrences[3]++;
      callNext();
      break;
    }
  case 7:
    {
      if (_debug) printf("ret()\n");
      if (_countOccurrences) _occurrences[3]++;
      ret();
      break;
    }
  }
}


void ImmediateOci::_interpret_11010(unsigned char cmd)
{
  unsigned char i = cmd >> 5;
  cmd = cmd << 3;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("jnc_D()\n");
      if (_countOccurrences) _occurrences[3]++;
      jnc_D();
      break;
    }
  case 1:
    {
      if (_debug) printf("jc_D()\n");
      if (_countOccurrences) _occurrences[3]++;
      jc_D();
      break;
    }
  case 2:
    {
      if (_debug) printf("sjnc_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      sjnc_Next();
      break;
    }
  case 3:
    {
      if (_debug) printf("sjc_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      sjc_Next();
      break;
    }
  case 4:
    {
      if (_debug) printf("jnc_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      jnc_Next();
      break;
    }
  case 5:
    {
      if (_debug) printf("jc_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      jc_Next();
      break;
    }
  case 6:
    {
      if (_debug) printf("jnzA_D()\n");
      if (_countOccurrences) _occurrences[3]++;
      jnzA_D();
      break;
    }
  case 7:
    {
      if (_debug) printf("jzA_D()\n");
      if (_countOccurrences) _occurrences[3]++;
      jzA_D();
      break;
    }
  }
}


void ImmediateOci::_interpret_11011(unsigned char cmd)
{
  unsigned char i = cmd >> 5;
  cmd = cmd << 3;
  
  switch (i)
  {
  case 0:
    {
      if (_debug) printf("sjnzA_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      sjnzA_Next();
      break;
    }
  case 1:
    {
      if (_debug) printf("sjzA_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      sjzA_Next();
      break;
    }
  case 2:
    {
      if (_debug) printf("jnzA_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      jnzA_Next();
      break;
    }
  case 3:
    {
      if (_debug) printf("jzA_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      jzA_Next();
      break;
    }
  case 4:
    {
      if (_debug) printf("csjneA_Next_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      csjneA_Next_Next();
      break;
    }
  case 5:
    {
      if (_debug) printf("cjneA_Next_Next()\n");
      if (_countOccurrences) _occurrences[3]++;
      cjneA_Next_Next();
      break;
    }
  case 6:
    {
      if (_debug) printf("cjneA_Next_D()\n");
      if (_countOccurrences) _occurrences[3]++;
      cjneA_Next_D();
      break;
    }
  case 7:
    {
      if (_debug) printf("halt()\n");
      if (_countOccurrences) _occurrences[2]++;
      halt();
      break;
    }
  }
}


void ImmediateOci::_halt()
{
  _haltFlag = true;
}


void ImmediateOci::_out(unsigned char byte)
{
  _checkAndExtendOutput();
  _output[_outputPtr++] = byte;
}


void ImmediateOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num)
{
  _out(bytes, pos, num, _ramMask);
}


void ImmediateOci::_out(unsigned char* bytes, unsigned short pos, unsigned char num, unsigned int mask)
{
  _checkAndExtendOutput(num);
  for (int i = pos; i < pos + num; ++i)
  {
    _output[_outputPtr++] = bytes[i & mask];
  }
}


unsigned char& ImmediateOci::_touch(unsigned int pos)
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


void ImmediateOci::_resetOccurrences()
{
  memset(_occurrences, 0, numCategories * sizeof(unsigned int));
}

void ImmediateOci::_resetTouched()
{
  _numTouched = 0;
  memset(_touched, 0, _ramSize * sizeof(unsigned short));
}

// ===============
// getters-setters
// ===============

const unsigned int ImmediateOci::geneticStringSize() { return _geneticStringSize; }

unsigned short ImmediateOci::counter() { return _counter; }
void ImmediateOci::setCounter(unsigned short counter) { _counter = counter; }
unsigned int ImmediateOci::outputPtr() { return _outputPtr; }
void ImmediateOci::setOutputPtr(unsigned int outputPtr) { _outputPtr = outputPtr; }
unsigned char ImmediateOci::acc() { return _acc; }
void ImmediateOci::setAcc(unsigned char acc) { _acc = acc; }
unsigned short ImmediateOci::dataPtr() { return _dataPtr; }
void ImmediateOci::setDataPtr(unsigned short dataPtr) { _dataPtr = dataPtr; }
unsigned char ImmediateOci::flags() { return _flags; }
void ImmediateOci::setFlags(unsigned char flags) { _flags = flags; }
unsigned char ImmediateOci::stackPtr() { return _stackPtr; }
void ImmediateOci::setStackPtr(unsigned char stackPtr) { _stackPtr = stackPtr; }

void ImmediateOci::output(unsigned char* out_output, int out_output_size) { memcpy(out_output, _output, out_output_size); }
unsigned char ImmediateOci::outputAt(unsigned short index) { return _output[index]; }
void ImmediateOci::setOutput(unsigned char* in_output, int in_output_size) { memcpy(_output, in_output, in_output_size); }
void ImmediateOci::setOutputAt(unsigned short index, unsigned char value) { _output[index] = value; }

void ImmediateOci::registers(unsigned char* out_registers, int out_registers_size) { memcpy(out_registers, _registers, out_registers_size); }
unsigned char ImmediateOci::registerAt(unsigned short index) { return _registers[index]; }
void ImmediateOci::setRegisters(unsigned char* in_registers, int in_registers_size) { memcpy(_registers, in_registers, in_registers_size); }
void ImmediateOci::setRegister(unsigned short index, unsigned char value) { _registers[index] = value; }

void ImmediateOci::ram(unsigned char* out_ram, int out_ram_size) { memcpy(out_ram, _ram, out_ram_size * sizeof(unsigned char)); }
unsigned char ImmediateOci::ramAt(unsigned short index) { return _ram[index & _ramMask]; }
void ImmediateOci::setRam(unsigned char* in_ram, int in_ram_size) { memcpy(_ram, in_ram, in_ram_size * sizeof(unsigned char)); }
void ImmediateOci::setRamAt(unsigned short index, unsigned char value) { _ram[index & _ramMask] = value; }

void ImmediateOci::stack(unsigned char* out_stack, int out_stack_size) { memcpy(out_stack, _stack, out_stack_size); }
unsigned char ImmediateOci::stackAt(unsigned short index) { return _stack[index]; }
void ImmediateOci::setStack(unsigned char* in_stack, int in_stack_size) { memcpy(_stack, in_stack, in_stack_size); }
void ImmediateOci::setStackAt(unsigned short index, unsigned char value) { _stack[index] = value; }

bool ImmediateOci::debug() { return _debug; }
void ImmediateOci::setDebug(bool debug) { _debug = debug; }
bool ImmediateOci::countOccurrences() { return _countOccurrences; }
void ImmediateOci::setCountOccurrences(bool countOccurrences) { _countOccurrences = countOccurrences; }
bool ImmediateOci::countTouched() { return _countTouched; }
void ImmediateOci::setCountTouched(bool countTouched) { _countTouched = countTouched; }
int  ImmediateOci::numTouched() { return _numTouched; }
void ImmediateOci::setNumTouched(int numTouched) { _numTouched = numTouched; }

void ImmediateOci::occurrences(unsigned int* out_occurrences, int out_occurrences_size) { memcpy(out_occurrences, _occurrences, out_occurrences_size * sizeof(unsigned int)); }
unsigned int ImmediateOci::occurrencesAt(unsigned short index) { return _occurrences[index]; }
void ImmediateOci::setOccurrences(unsigned int* in_occurrences, int in_occurrences_size) { memcpy(_occurrences, in_occurrences, in_occurrences_size * sizeof(unsigned int)); }
void ImmediateOci::setOccurrencesAt(unsigned short index, unsigned int value) { _occurrences[index] = value; }

void ImmediateOci::touched(unsigned short* out_touched, int out_touched_size) { memcpy(out_touched, _touched, out_touched_size * sizeof(unsigned short)); }
unsigned short ImmediateOci::touchedAt(unsigned short index) { return _touched[index]; }
void ImmediateOci::setTouched(unsigned short* in_touched, int in_touched_size) { memcpy(_touched, in_touched, in_touched_size * sizeof(unsigned short)); }
void ImmediateOci::setTouchedAt(unsigned short index, unsigned short value) { _touched[index] = value; }
