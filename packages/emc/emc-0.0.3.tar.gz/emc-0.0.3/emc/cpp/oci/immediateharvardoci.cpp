#include "immediateharvardoci.h"


#define _CARRY_BITIDX  0
#define _CARRY_BIT     (_flags >> _CARRY_BITIDX) & 1

#define _SET_CARRY_BIT    _flags |= 1 << _CARRY_BITIDX
#define _UNSET_CARRY_BIT  _flags &= ~(1 << _CARRY_BITIDX)

#define RAM(i) _ram[i & _ramMask]
#define ROM(i) _touch(i)

// =============
// Register MOVs
// =============

void ImmediateHarvardOci::movR_DH(unsigned char r) { _registers[r] = ((unsigned char*) &_dataPtr)[1]; }
void ImmediateHarvardOci::movDH_R(unsigned char r) { ((unsigned char*) &_dataPtr)[1] = _registers[r]; }
void ImmediateHarvardOci::movR_DL(unsigned char r) { _registers[r] = ((unsigned char*) &_dataPtr)[0]; }
void ImmediateHarvardOci::movDL_R(unsigned char r) { ((unsigned char*) &_dataPtr)[0] = _registers[r]; }
void ImmediateHarvardOci::movR_DPtr(unsigned char r) { _registers[r] = RAM(_dataPtr); }
void ImmediateHarvardOci::moviR_DPtr(unsigned char r) { _registers[r] = RAM(_dataPtr++); }
void ImmediateHarvardOci::movDPtr_R(unsigned char r) { RAM(_dataPtr) = _registers[r]; }
void ImmediateHarvardOci::moviDPtr_R(unsigned char r) { RAM(_dataPtr++) = _registers[r]; }
void ImmediateHarvardOci::movR_Next(unsigned char r) { _registers[r] = ROM(_counter++); }
void ImmediateHarvardOci::movR_A(unsigned char r) { _registers[r] = _acc; }
void ImmediateHarvardOci::movA_R(unsigned char r) { _acc = _registers[r]; }
void ImmediateHarvardOci::xchA_R(unsigned char r) { unsigned char temp = _acc; _acc = _registers[r]; _registers[r] = temp; }
void ImmediateHarvardOci::movA_DH() { _acc = ((unsigned char*) &_dataPtr)[1]; }
void ImmediateHarvardOci::movA_DL() { _acc = ((unsigned char*) &_dataPtr)[0]; }
void ImmediateHarvardOci::movDH_A() { ((unsigned char*) &_dataPtr)[1] = _acc; }
void ImmediateHarvardOci::movDL_A() { ((unsigned char*) &_dataPtr)[0] = _acc; }
void ImmediateHarvardOci::movA_DPtr() { _acc = RAM(_dataPtr); }
void ImmediateHarvardOci::moviA_DPtr() { _acc = RAM(_dataPtr++); }
void ImmediateHarvardOci::movDPtr_A() { RAM(_dataPtr) = _acc; }
void ImmediateHarvardOci::moviDPtr_A() { RAM(_dataPtr++) = _acc; }
void ImmediateHarvardOci::xchA_DPtr() { unsigned char temp = _acc; _acc = RAM(_dataPtr); RAM(_dataPtr) = temp; }
void ImmediateHarvardOci::xchiA_DPtr() { unsigned char temp = _acc; _acc = RAM(_dataPtr); RAM(_dataPtr++) = temp; }
void ImmediateHarvardOci::movDPtr_Next() { RAM(_dataPtr) = ROM(_counter++); }
void ImmediateHarvardOci::movDH_Next() { ((unsigned char*) &_dataPtr)[1] = ROM(_counter++); }
void ImmediateHarvardOci::movDL_Next() { ((unsigned char*) &_dataPtr)[0] = ROM(_counter++); }
void ImmediateHarvardOci::movA_Next() { _acc = ROM(_counter++); }
void ImmediateHarvardOci::cplC() { _flags ^= 1 << _CARRY_BITIDX; }

// ==================
// Arithmetic & Logic
// ==================

void ImmediateHarvardOci::inc_R(unsigned char r) { _registers[r]++; }
void ImmediateHarvardOci::dec_R(unsigned char r) { _registers[r]--; }
void ImmediateHarvardOci::inc_A() { _acc++; }
void ImmediateHarvardOci::dec_A() { _acc--; }
void ImmediateHarvardOci::inc_D() { _dataPtr++; }
void ImmediateHarvardOci::dec_D() { _dataPtr--; }
void ImmediateHarvardOci::anlA_R(unsigned char r) { _acc &= _registers[r]; }
void ImmediateHarvardOci::orlA_R(unsigned char r) { _acc |= _registers[r]; }
void ImmediateHarvardOci::addA_R(unsigned char r) { _acc += _registers[r]; }
void ImmediateHarvardOci::subA_R(unsigned char r) { _acc -= _registers[r]; }
void ImmediateHarvardOci::cplA() { _acc = ~_acc; }
void ImmediateHarvardOci::anlA_Next() { _acc &= ROM(_counter++); }
void ImmediateHarvardOci::orlA_Next() { _acc |= ROM(_counter++); }
void ImmediateHarvardOci::anlA_DPtr() { _acc &= RAM(_dataPtr); }
void ImmediateHarvardOci::orlA_DPtr() { _acc |= RAM(_dataPtr); }
void ImmediateHarvardOci::addA_Next() { _acc += ROM(_counter++); }
void ImmediateHarvardOci::subA_Next() { _acc -= ROM(_counter++); }
void ImmediateHarvardOci::addA_DPtr() { _acc += RAM(_dataPtr); }
void ImmediateHarvardOci::subA_DPtr() { _acc -= RAM(_dataPtr); }

void ImmediateHarvardOci::addcA_R(unsigned char r)
{
  if (_acc > 0xFF - _registers[r]) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;
  addA_R(r);
}

void ImmediateHarvardOci::subbA_R(unsigned char r)
{
  if (_acc < _registers[r]) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_R(r);
}

void ImmediateHarvardOci::addcA_Next()
{
  if (_acc > 0xFF - ROM(_counter)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  addA_Next();
}

void ImmediateHarvardOci::subbA_Next()
{
  if (_acc < ROM(_counter)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_Next();
}

void ImmediateHarvardOci::addcA_DPtr()
{
  if (_acc > 0xFF - RAM(_dataPtr)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  addA_DPtr();
}

void ImmediateHarvardOci::subbA_DPtr()
{
  if (_acc < RAM(_dataPtr)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_DPtr();
}

void ImmediateHarvardOci::rlA() { _acc = ((_acc << 1) | (_acc >> 7)); }
void ImmediateHarvardOci::rrA() { _acc = ((_acc >> 1) | (_acc << 7)); }

void ImmediateHarvardOci::rlcA()
{
  // rotates accumulator left with 1 bit, using carry flag
  // TODO do this more efficiently
  unsigned char oldCarry = _CARRY_BIT;
  unsigned char newCarry = _acc >> 7;
  _acc = ((_acc << 1) | oldCarry);
  if (newCarry) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;
}

void ImmediateHarvardOci::rrcA()
{
  // rotates accumulator right with 1 bit, using carry flag
  // TODO do this more efficiently
  unsigned char oldCarry = _CARRY_BIT;
  unsigned char newCarry = _acc & 1;
  _acc = ((_acc >> 1) | (oldCarry << 7));
  if (newCarry) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;
}


// ================
// Stack operations
// ================

void ImmediateHarvardOci::pushDH() { _stack[++_stackPtr] = ((unsigned char*) &_dataPtr)[1]; }
void ImmediateHarvardOci::popDH() { ((unsigned char*) &_dataPtr)[1] = _stack[_stackPtr--]; }
void ImmediateHarvardOci::pushDL() { _stack[++_stackPtr] = ((unsigned char*) &_dataPtr)[0]; }
void ImmediateHarvardOci::popDL() { ((unsigned char*) &_dataPtr)[0] = _stack[_stackPtr--]; }
void ImmediateHarvardOci::pushA() { _stack[++_stackPtr] = _acc; }
void ImmediateHarvardOci::popA() { _acc = _stack[_stackPtr--]; }

// ===============
// Jump operations
// ===============

void ImmediateHarvardOci::sjmpNext() { _counter += (char) ROM(_counter); }
void ImmediateHarvardOci::jmpNext()
{
  unsigned short current_counter = _counter;
  ((unsigned char*) &_counter)[0] = ROM(current_counter++);
  ((unsigned char*) &_counter)[1] = ROM(current_counter);
}

void ImmediateHarvardOci::jmpD() { _counter = _dataPtr; }

void ImmediateHarvardOci::callD()
{
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[0];
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[1];
  _counter = _dataPtr;
}

void ImmediateHarvardOci::callNext()
{
  unsigned short new_counter = ((unsigned short*)(&ROM(_counter)))[0];
  _counter += 2;
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[0];
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[1];
  _counter = new_counter;
}

void ImmediateHarvardOci::ret() {
  ((unsigned char*) &_counter)[1] = _stack[_stackPtr--];
  ((unsigned char*) &_counter)[0] = _stack[_stackPtr--];
}


// =================
// Conditional jumps
// =================

void ImmediateHarvardOci::jnc_D() { if (!_CARRY_BIT) jmpD(); }
void ImmediateHarvardOci::jc_D() { if (_CARRY_BIT) jmpD(); }
void ImmediateHarvardOci::sjnc_Next() { if (!_CARRY_BIT) sjmpNext(); }
void ImmediateHarvardOci::sjc_Next() { if (_CARRY_BIT) sjmpNext(); }
void ImmediateHarvardOci::jnc_Next() { if (!_CARRY_BIT) jmpNext(); }
void ImmediateHarvardOci::jc_Next() { if (_CARRY_BIT) jmpNext(); }
void ImmediateHarvardOci::jnzA_D() { if (_acc) jmpD(); }
void ImmediateHarvardOci::jzA_D() { if (!_acc) jmpD(); }
void ImmediateHarvardOci::sjnzA_Next() { if (_acc) sjmpNext(); }
void ImmediateHarvardOci::sjzA_Next() { if (!_acc) sjmpNext(); }
void ImmediateHarvardOci::jnzA_Next() { if (_acc) jmpNext(); }
void ImmediateHarvardOci::jzA_Next() { if (!_acc) jmpNext(); }
void ImmediateHarvardOci::csjneA_Next_Next() { if (_acc != ROM(_counter++)) sjmpNext(); }
void ImmediateHarvardOci::cjneA_Next_Next() { if (_acc != ROM(_counter++)) jmpNext(); }
void ImmediateHarvardOci::cjneA_Next_D() { if (_acc != ROM(_counter++)) jmpD(); }

// ===============
// Output commands
// ===============

void ImmediateHarvardOci::outR(unsigned char r) { _out(_registers[r]); }
void ImmediateHarvardOci::outDPtr(unsigned char n) { _out(_ram, _dataPtr, n); }
void ImmediateHarvardOci::outiDPtr(unsigned char n) { _out(_ram, _dataPtr, n); _dataPtr += n; }
void ImmediateHarvardOci::outNext(unsigned char n) { _out(_rom, _counter, n); _counter += n; }
void ImmediateHarvardOci::halt() { _halt(); }
