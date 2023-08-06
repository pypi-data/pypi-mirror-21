#include "immediateoci.h"


#define _CARRY_BITIDX  0
#define _CARRY_BIT     (_flags >> _CARRY_BITIDX) & 1

#define _SET_CARRY_BIT    _flags |= 1 << _CARRY_BITIDX
#define _UNSET_CARRY_BIT  _flags &= ~(1 << _CARRY_BITIDX)

#define RAM(i) _touch(i)

// =============
// Register MOVs
// =============

void ImmediateOci::movR_DH(unsigned char r) { _registers[r] = ((unsigned char*) &_dataPtr)[1]; }
void ImmediateOci::movDH_R(unsigned char r) { ((unsigned char*) &_dataPtr)[1] = _registers[r]; }
void ImmediateOci::movR_DL(unsigned char r) { _registers[r] = ((unsigned char*) &_dataPtr)[0]; }
void ImmediateOci::movDL_R(unsigned char r) { ((unsigned char*) &_dataPtr)[0] = _registers[r]; }
void ImmediateOci::movR_DPtr(unsigned char r) { _registers[r] = RAM(_dataPtr); }
void ImmediateOci::moviR_DPtr(unsigned char r) { _registers[r] = RAM(_dataPtr++); }
void ImmediateOci::movDPtr_R(unsigned char r) { RAM(_dataPtr) = _registers[r]; }
void ImmediateOci::moviDPtr_R(unsigned char r) { RAM(_dataPtr++) = _registers[r]; }
void ImmediateOci::movR_Next(unsigned char r) { _registers[r] = RAM(_counter++); }
void ImmediateOci::movR_A(unsigned char r) { _registers[r] = _acc; }
void ImmediateOci::movA_R(unsigned char r) { _acc = _registers[r]; }
void ImmediateOci::xchA_R(unsigned char r) { unsigned char temp = _acc; _acc = _registers[r]; _registers[r] = temp; }
void ImmediateOci::movA_DH() { _acc = ((unsigned char*) &_dataPtr)[1]; }
void ImmediateOci::movA_DL() { _acc = ((unsigned char*) &_dataPtr)[0]; }
void ImmediateOci::movDH_A() { ((unsigned char*) &_dataPtr)[1] = _acc; }
void ImmediateOci::movDL_A() { ((unsigned char*) &_dataPtr)[0] = _acc; }
void ImmediateOci::movA_DPtr() { _acc = RAM(_dataPtr); }
void ImmediateOci::moviA_DPtr() { _acc = RAM(_dataPtr++); }
void ImmediateOci::movDPtr_A() { RAM(_dataPtr) = _acc; }
void ImmediateOci::moviDPtr_A() { RAM(_dataPtr++) = _acc; }
void ImmediateOci::xchA_DPtr() { unsigned char temp = _acc; _acc = RAM(_dataPtr); RAM(_dataPtr) = temp; }
void ImmediateOci::xchiA_DPtr() { unsigned char temp = _acc; _acc = RAM(_dataPtr); RAM(_dataPtr++) = temp; }
void ImmediateOci::movDPtr_Next() { RAM(_dataPtr) = RAM(_counter++); }
void ImmediateOci::movDH_Next() { ((unsigned char*) &_dataPtr)[1] = RAM(_counter++); }
void ImmediateOci::movDL_Next() { ((unsigned char*) &_dataPtr)[0] = RAM(_counter++); }
void ImmediateOci::movA_Next() { _acc = RAM(_counter++); }
void ImmediateOci::cplC() { _flags ^= 1 << _CARRY_BITIDX; }

// ==================
// Arithmetic & Logic
// ==================

void ImmediateOci::inc_R(unsigned char r) { _registers[r]++; }
void ImmediateOci::dec_R(unsigned char r) { _registers[r]--; }
void ImmediateOci::inc_A() { _acc++; }
void ImmediateOci::dec_A() { _acc--; }
void ImmediateOci::inc_D() { _dataPtr++; }
void ImmediateOci::dec_D() { _dataPtr--; }
void ImmediateOci::anlA_R(unsigned char r) { _acc &= _registers[r]; }
void ImmediateOci::orlA_R(unsigned char r) { _acc |= _registers[r]; }
void ImmediateOci::addA_R(unsigned char r) { _acc += _registers[r]; }
void ImmediateOci::subA_R(unsigned char r) { _acc -= _registers[r]; }
void ImmediateOci::cplA() { _acc = ~_acc; }
void ImmediateOci::anlA_Next() { _acc &= RAM(_counter++); }
void ImmediateOci::orlA_Next() { _acc |= RAM(_counter++); }
void ImmediateOci::anlA_DPtr() { _acc &= RAM(_dataPtr); }
void ImmediateOci::orlA_DPtr() { _acc |= RAM(_dataPtr); }
void ImmediateOci::addA_Next() { _acc += RAM(_counter++); }
void ImmediateOci::subA_Next() { _acc -= RAM(_counter++); }
void ImmediateOci::addA_DPtr() { _acc += RAM(_dataPtr); }
void ImmediateOci::subA_DPtr() { _acc -= RAM(_dataPtr); }

void ImmediateOci::addcA_R(unsigned char r)
{
  if (_acc > 0xFF - _registers[r]) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;
  addA_R(r);
}

void ImmediateOci::subbA_R(unsigned char r)
{
  if (_acc < _registers[r]) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_R(r);
}

void ImmediateOci::addcA_Next()
{
  if (_acc > 0xFF - RAM(_counter)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  addA_Next();
}

void ImmediateOci::subbA_Next()
{
  if (_acc < RAM(_counter)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_Next();
}

void ImmediateOci::addcA_DPtr()
{
  if (_acc > 0xFF - RAM(_dataPtr)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  addA_DPtr();
}

void ImmediateOci::subbA_DPtr()
{
  if (_acc < RAM(_dataPtr)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_DPtr();
}

void ImmediateOci::rlA() { _acc = ((_acc << 1) | (_acc >> 7)); }
void ImmediateOci::rrA() { _acc = ((_acc >> 1) | (_acc << 7)); }

void ImmediateOci::rlcA()
{
  // rotates accumulator left with 1 bit, using carry flag
  // TODO do this more efficiently
  unsigned char oldCarry = _CARRY_BIT;
  unsigned char newCarry = _acc >> 7;
  _acc = ((_acc << 1) | oldCarry);
  if (newCarry) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;
}

void ImmediateOci::rrcA()
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

void ImmediateOci::pushDH() { _stack[++_stackPtr] = ((unsigned char*) &_dataPtr)[1]; }
void ImmediateOci::popDH() { ((unsigned char*) &_dataPtr)[1] = _stack[_stackPtr--]; }
void ImmediateOci::pushDL() { _stack[++_stackPtr] = ((unsigned char*) &_dataPtr)[0]; }
void ImmediateOci::popDL() { ((unsigned char*) &_dataPtr)[0] = _stack[_stackPtr--]; }
void ImmediateOci::pushA() { _stack[++_stackPtr] = _acc; }
void ImmediateOci::popA() { _acc = _stack[_stackPtr--]; }

// ===============
// Jump operations
// ===============

void ImmediateOci::sjmpNext() { _counter += (char) RAM(_counter); }
void ImmediateOci::jmpNext()
{
  unsigned short current_counter = _counter;
  ((unsigned char*) &_counter)[0] = RAM(current_counter++);
  ((unsigned char*) &_counter)[1] = RAM(current_counter);
}

void ImmediateOci::jmpD() { _counter = _dataPtr; }

void ImmediateOci::callD()
{
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[0];
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[1];
  _counter = _dataPtr;
}

void ImmediateOci::callNext()
{
  unsigned short new_counter = ((unsigned short*)(&RAM(_counter)))[0];
  _counter += 2;
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[0];
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[1];
  _counter = new_counter;
}

void ImmediateOci::ret() {
  ((unsigned char*) &_counter)[1] = _stack[_stackPtr--];
  ((unsigned char*) &_counter)[0] = _stack[_stackPtr--];
}


// =================
// Conditional jumps
// =================

void ImmediateOci::jnc_D() { if (!_CARRY_BIT) jmpD(); }
void ImmediateOci::jc_D() { if (_CARRY_BIT) jmpD(); }
void ImmediateOci::sjnc_Next() { if (!_CARRY_BIT) sjmpNext(); }
void ImmediateOci::sjc_Next() { if (_CARRY_BIT) sjmpNext(); }
void ImmediateOci::jnc_Next() { if (!_CARRY_BIT) jmpNext(); }
void ImmediateOci::jc_Next() { if (_CARRY_BIT) jmpNext(); }
void ImmediateOci::jnzA_D() { if (_acc) jmpD(); }
void ImmediateOci::jzA_D() { if (!_acc) jmpD(); }
void ImmediateOci::sjnzA_Next() { if (_acc) sjmpNext(); }
void ImmediateOci::sjzA_Next() { if (!_acc) sjmpNext(); }
void ImmediateOci::jnzA_Next() { if (_acc) jmpNext(); }
void ImmediateOci::jzA_Next() { if (!_acc) jmpNext(); }
void ImmediateOci::csjneA_Next_Next() { if (_acc != RAM(_counter++)) sjmpNext(); }
void ImmediateOci::cjneA_Next_Next() { if (_acc != RAM(_counter++)) jmpNext(); }
void ImmediateOci::cjneA_Next_D() { if (_acc != RAM(_counter++)) jmpD(); }

// ===============
// Output commands
// ===============

void ImmediateOci::outR(unsigned char r) { _out(_registers[r]); }
void ImmediateOci::outDPtr(unsigned char n) { _out(_ram, _dataPtr, n); }
void ImmediateOci::outiDPtr(unsigned char n) { _out(_ram, _dataPtr, n); _dataPtr += n; }
void ImmediateOci::outNext(unsigned char n) { _out(_ram, _counter, n); _counter += n; }
void ImmediateOci::halt() { _halt(); }
