#include "sbnzoiscoci.h"

#define RAM(i) _touch(i)

void SbnzOiscOci::sbnz()
{ 
  // Subtract value at mem[AddrB] from value at mem[AddrA], store result
  // into mem[AddrC]
  // if result wasn't zero, branch to AddrD.
  // if underflow, output mem[AddrA] + mem[AddrB]
  
  if (RAM(RAM(_counter)) < RAM(RAM(_counter + 1))) 
  {
  	unsigned short outVal = RAM(RAM(_counter)) + RAM(RAM(_counter + 1));
  	_out(((unsigned char*) &outVal)[0]);
  	_out(((unsigned char*) &outVal)[1]);
  }
  
  if (RAM(RAM(_counter + 2)) = RAM(RAM(_counter)) - RAM(RAM(_counter + 1))) {
    _counter = RAM(_counter + 3); 
  } else {
    _counter += 4;
  }
  
}
