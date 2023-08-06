#include "indirectoci.h"


#define _CARRY_BITIDX  0
#define _CARRY_BIT     (_flags >> _CARRY_BITIDX) & 1

#define _SET_CARRY_BIT    _flags |= 1 << _CARRY_BITIDX
#define _UNSET_CARRY_BIT  _flags &= ~(1 << _CARRY_BITIDX)

#define RAM(i) _touch(i)

// =============
// Register MOVs
// =============

void IndirectOci::movR_DH(unsigned char r)
{
  // copies high byte of dataPtr into given register
  _registers[r] = ((unsigned char*) &_dataPtr)[1];
}

void IndirectOci::movDH_R(unsigned char r)
{
  // copies value of given register into high byte of dataPtr
  ((unsigned char*) &_dataPtr)[1] = _registers[r];
}

void IndirectOci::movR_DL(unsigned char r)
{
  // copies low byte of dataPtr into given register
  _registers[r] = ((unsigned char*) &_dataPtr)[0];
}

void IndirectOci::movDL_R(unsigned char r)
{
  // copies value of given register into low byte of dataPtr
  ((unsigned char*) &_dataPtr)[0] = _registers[r];
}

void IndirectOci::movR_DPtr(unsigned char r)
{
  // copies 1 byte from memory where dataPtr points, into given register
  _registers[r] = RAM(_dataPtr);
}

void IndirectOci::movDPtr_R(unsigned char r)
{
  // copies value of given register to the memory where dataPtr points
  RAM(_dataPtr) = _registers[r];
}

void IndirectOci::movR_A(unsigned char r)
{
  // copies accumulator into given register
  _registers[r] = _acc;
}

void IndirectOci::movA_R(unsigned char r)
{
  // copies given register into accumulator
  _acc = _registers[r];
}

void IndirectOci::xchA_R(unsigned char r)
{
  // exchanges values of accumulator and given register
  unsigned char temp = _acc;
  _acc = _registers[r];
  _registers[r] = temp;
}

void IndirectOci::movA_DH()
{
  // copies high byte of dataPtr into accumulator
  _acc = ((unsigned char*) &_dataPtr)[1];
}

void IndirectOci::movA_DL()
{
  // copies value of accumulator into high byte of dataPtr
  _acc = ((unsigned char*) &_dataPtr)[0];
}

void IndirectOci::movDH_A()
{
  // copies low byte of dataPtr into accumulator
  ((unsigned char*) &_dataPtr)[1] = _acc;
}

void IndirectOci::movDL_A()
{
  // copies value of accumulator into low byte of dataPtr
  ((unsigned char*) &_dataPtr)[0] = _acc;
}

void IndirectOci::movA_DPtr()
{
  // copies 1 byte from memory where dataPtr points, into accumulator
  _acc = RAM(_dataPtr);
}

void IndirectOci::movDPtr_A()
{
  // copies value of accumulator to the memory where dataPtr points
  RAM(_dataPtr) = _acc;
}

void IndirectOci::cplC()
{
  // inverts value of carry flag
  _flags ^= 1 << _CARRY_BITIDX;
}


// ==================
// Arithmetic & Logic
// ==================

void IndirectOci::inc_A()
{
  // increments value of accumulator
  _acc++;
}

void IndirectOci::dec_A()
{
  // decrements value of accumulator
  _acc--;
}

void IndirectOci::inc_D()
{
  // increments value of dataPtr
  _dataPtr++;
}

void IndirectOci::dec_D()
{
  // decrements value of dataPtr
  _dataPtr--;
}

void IndirectOci::anlA_R(unsigned char r)
{
  // performs bitwise and between accumulator and given register
  _acc &= _registers[r];
}

void IndirectOci::orlA_R(unsigned char r)
{
  // performs bitwise or between accumulator and given register
  _acc |= _registers[r];
}

void IndirectOci::addA_R(unsigned char r)
{
  // adds value of given register to accumulator
  _acc += _registers[r];
}

void IndirectOci::addcA_R(unsigned char r)
{
  // adds value of given register to accumulator, with carry
  if (_acc > 0xFF - _registers[r]) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  addA_R(r);
}

void IndirectOci::subA_R(unsigned char r)
{
  // subtracts value of given register from accumulator
  _acc -= _registers[r];
}

void IndirectOci::subbA_R(unsigned char r)
{
  // subtracts value of given register from accumulator, with borrow
  if (_acc < _registers[r]) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_R(r);
}

void IndirectOci::cplA()
{
  // inverts value of accumulator bitwise
  _acc = ~_acc;
}

void IndirectOci::anlA_RPtr(unsigned char rp)
{
  // performs bitwise and between accumulator and memory memory where given register points
  _acc &= RAM(((unsigned short*) _registers)[rp]);
}

void IndirectOci::orlA_RPtr(unsigned char rp)
{
  // performs bitwise or between accumulator and memory memory where given register points
  _acc |= RAM(((unsigned short*) _registers)[rp]);
}

void IndirectOci::anlA_DPtr()
{
  // performs bitwise and between accumulator and memory where dataPtr points
  _acc &= RAM(_dataPtr);
}

void IndirectOci::orlA_DPtr()
{
  // performs bitwise or between accumulator and memory where dataPtr points
  _acc |= RAM(_dataPtr);
}

void IndirectOci::addA_RPtr(unsigned char rp)
{
  // adds value of memory where given register points to accumulator
  _acc += RAM(((unsigned short*) _registers)[rp]);
}

void IndirectOci::addcA_RPtr(unsigned char rp)
{
  // adds value of memory where given register points to accumulator, with carry
  if (_acc > 0xFF - RAM(((unsigned short*) _registers)[rp])) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  addA_RPtr(rp);
}

void IndirectOci::subA_RPtr(unsigned char rp)
{
  // subtracts value of memory where given register points from accumulator
  _acc -= RAM(((unsigned short*) _registers)[rp]);
}

void IndirectOci::subbA_RPtr(unsigned char rp)
{
  // subtracts value of memory where given register points from accumulator, with borrow
  if (_acc < RAM(((unsigned short*) _registers)[rp])) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_RPtr(rp);
}

void IndirectOci::addA_DPtr()
{
  // adds value of memory where dataPtr points to accumulator
  _acc += RAM(_dataPtr);
}

void IndirectOci::addcA_DPtr()
{
  // adds value of memory where dataPtr points to accumulator, with carry
  if (_acc > 0xFF - RAM(_dataPtr)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  addA_DPtr();
}

void IndirectOci::subA_DPtr()
{
  // subtracts value of memory where dataPtr points from accumulator
  _acc -= RAM(_dataPtr);
}

void IndirectOci::subbA_DPtr()
{
  // subtracts value of memory where dataPtr points from accumulator, with borrow
  if (_acc < RAM(_dataPtr)) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;

  subA_DPtr();
}

void IndirectOci::rlA()
{
  // rotates accumulator left with 1 bit
  _acc = ((_acc << 1) | (_acc >> 7));
}

void IndirectOci::rrA()
{
  // rotates accumulator right with 1 bit
  _acc = ((_acc >> 1) | (_acc << 7));
}

void IndirectOci::rlcA()
{
  // rotates accumulator left with 1 bit, using carry flag
  // TODO do this more efficiently
  unsigned char oldCarry = _CARRY_BIT;
  unsigned char newCarry = _acc >> 7;
  _acc = ((_acc << 1) | oldCarry);
  if (newCarry) _SET_CARRY_BIT;
  else _UNSET_CARRY_BIT;
}

void IndirectOci::rrcA()
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

void IndirectOci::pushDH()
{
  // pushes high byte of dataPtr to stack
  _stack[++_stackPtr] = ((unsigned char*) &_dataPtr)[1];
}

void IndirectOci::popDH()
{
  // pops high byte of dataPtr from stack
  ((unsigned char*) &_dataPtr)[1] = _stack[_stackPtr--];
}

void IndirectOci::pushDL()
{
  // pushes low byte of dataPtr to stack
  _stack[++_stackPtr] = ((unsigned char*) &_dataPtr)[0];
}

void IndirectOci::popDL()
{
  // pops low byte of dataPtr from stack
  ((unsigned char*) &_dataPtr)[0] = _stack[_stackPtr--];
}

void IndirectOci::pushA()
{
  // pushes value of accumulator to stack
  _stack[++_stackPtr] = _acc;
}

void IndirectOci::popA()
{
  // pops value of accumulator from stack
  _acc = _stack[_stackPtr--];
}

void IndirectOci::pushR(unsigned char r)
{
  // pushes value of a register to stack
  _stack[++_stackPtr] = _registers[r];
}

void IndirectOci::popR(unsigned char r)
{
  // pops value of a register from stack
  _registers[r] = _stack[_stackPtr--];
}


// ===============
// Jump operations
// ===============

void IndirectOci::sjmpR(unsigned char r)
{
  // short jumps program counter with value of register (R0-R3)
  _counter += (char) _registers[r];
}

void IndirectOci::jmpR(unsigned char rp)
{
  // absolute jumps to memory address given by pair of registers
  _counter = ((unsigned short*) _registers)[rp];
}

void IndirectOci::jmpD()
{
  // absolute jumps to value of dataPtr
  _counter = _dataPtr;
}

void IndirectOci::scallR(unsigned char r)
{
  // pushes program counter, and then sjmpR
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[0];
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[1];
  _counter += (char) _registers[r];
}

void IndirectOci::callR(unsigned char rp)
{
  // pushes program counter, and then jmpR
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[0];
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[1];
  _counter = ((unsigned short*) _registers)[rp];
}

void IndirectOci::callD()
{
  // pushes program counter, and then jmpD
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[0];
  _stack[++_stackPtr] = ((unsigned char*) &_counter)[1];
  _counter = _dataPtr;
}

void IndirectOci::ret()
{
  // pops program counter from stack
  ((unsigned char*) &_counter)[1] = _stack[_stackPtr--];
  ((unsigned char*) &_counter)[0] = _stack[_stackPtr--];
}


// =================
// Conditional jumps
// =================

void IndirectOci::jnc_D()
{
  // jmpD if carry bit is not set
  if (!_CARRY_BIT) jmpD();
}

void IndirectOci::jc_D()
{
  // jmpD if carry bit is set
  if (_CARRY_BIT) jmpD();
}

void IndirectOci::sjnc_R(unsigned char r)
{
  // sjmpR if carry bit is not set
  if (!_CARRY_BIT) sjmpR(r);
}

void IndirectOci::sjc_R(unsigned char r)
{
  // sjmpR if carry bit is set
  if (_CARRY_BIT) sjmpR(r);
}

void IndirectOci::jnc_R(unsigned char rp)
{
  // jmpR if carry bit is not set
  if (!_CARRY_BIT) jmpR(rp);
}

void IndirectOci::jc_R(unsigned char rp)
{
  // jmpR if carry bit is set
  if (_CARRY_BIT) jmpR(rp);
}

void IndirectOci::jnzA_D()
{
  // jmpD if accumulator is not zero
  if (_acc) jmpD();
}

void IndirectOci::jzA_D()
{
  // jmpD if accumulator is zero
  if (!_acc) jmpD();
}

void IndirectOci::sjnzA_R(unsigned char r)
{
  // sjmpR if accumulator is not zero
  if (_acc) sjmpR(r);
}

void IndirectOci::sjzA_R(unsigned char r)
{
  // sjmpR if accumulator is zero
  if (!_acc) sjmpR(r);
}

void IndirectOci::jnzA_R(unsigned char rp)
{
  // jmpR if accumulator is not zero
  if (_acc) jmpR(rp);
}

void IndirectOci::jzA_R(unsigned char rp)
{
  // jmpR if accumulator is zero
  if (!_acc) jmpR(rp);
}


// ===============
// Output commands
// ===============

void IndirectOci::outR(unsigned char r)
{
  // outputs the value of a given register
  _out(_registers[r]);
}

void IndirectOci::outRPtr(unsigned char rp)
{
  // outputs byte from where a pair of registers is pointing
  _out(_ram, ((unsigned short*) _registers)[rp], 1);
}

void IndirectOci::outDPtr(unsigned char n)
{
  // outputs next n bytes from where dataPtr points
  _out(_ram, _dataPtr, n);
}

void IndirectOci::halt()
{
  // Signals the VM to halt
  _halt();
}
