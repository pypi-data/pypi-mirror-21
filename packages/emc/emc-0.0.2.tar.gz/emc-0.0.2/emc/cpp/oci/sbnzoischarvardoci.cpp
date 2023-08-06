#include "sbnzoischarvardoci.h"

#define ROM(i) _touch(i)
#define RAM(i) _ram[(i) & _ramMask]

void SbnzOiscHarvardOci::sbnz()
{ 
  // Subtract value at mem[AddrB] from value at mem[AddrA], store result
  // into mem[AddrC]
  // if result wasn't zero, branch to AddrD.
  // if underflow, output mem[AddrA] + mem[AddrB]
  
  if (RAM(ROM(_counter)) < RAM(ROM(_counter + 1))) 
  {
  	unsigned short outVal = RAM(ROM(_counter)) + RAM(ROM(_counter + 1));
  	_out(((unsigned char*) &outVal)[0]);
  	_out(((unsigned char*) &outVal)[1]);
  }
  
  if (RAM(ROM(_counter + 2)) = RAM(ROM(_counter)) - RAM(ROM(_counter + 1))) {
    _counter = ROM(_counter + 3); 
  } else {
    _counter += 4;
  }
  
}
