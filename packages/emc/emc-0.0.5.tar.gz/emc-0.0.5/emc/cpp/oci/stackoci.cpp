#include "stackoci.h"

#include <iostream>
using namespace std;

#define STACK(i) _touch(i)


void StackOci::dup()
{ 
  // DUP: Duplicate the stack top. This is the only way to allocate stack space.
  // mem[SP]->mem[SP+1]; SP+1->SP
  STACK(_sp+1) = STACK(_sp);
  _sp++; 
}

void StackOci::one()
{
  // ONE: Shift the stack top left one bit, shifting one into the least significant bit.
  // mem[SP]<<1
  STACK(_sp) = (STACK(_sp) << 1) | 1;
}

void StackOci::zero()
{
  // ZERO: Shift the stack top left one bit, shifting zero into the least significant bit.
  // mem[SP]<<0 
  STACK(_sp) = (STACK(_sp) << 1);
}

void StackOci::load()
{
  // LOAD: Use the value on the stack top as a memory address; replace it with the contents of the referenced location.
  // mem[mem[SP]]->mem[SP]
  STACK(_sp) = STACK(STACK(_sp)); 
}

void StackOci::pop()
{
  // POP: Store the value from the top of the stack in the memory location referenced by the second word on the stack; pop both.
  // mem[SP]->mem[mem[SP-1]]; SP-2 -> SP 
  STACK(STACK(_sp-1)) = STACK(_sp);
  _sp -= 2;
}

void StackOci::sub()
{
  // SUB: Subtract the top value on the stack from the value below it, pop both and push the result.
  // mem[SP-1] - mem[SP] -> mem[SP-1]; SP-1 -> SP
  STACK(_sp - 1) -= STACK(_sp);
  _sp--;
}

void StackOci::jpos()
{
  // JPOS: If the word below the stack top is positive, jump to the word pointed to by the stack top. In any case, pop both.
  // if mem[SP-1]>-1 then mem[SP]->PC; SP-2 -> SP
  if (((short) (STACK(_sp-1))) >= 0) _counter = STACK(_sp);
  _sp -= 2;
}

void StackOci::out()
{
  // OUT: write the value of the stack top to the output
  // mem[SP]->output
  _out((unsigned char*) _stack, _sp * 2, 2, 2 * _stackSize - 1);
}
