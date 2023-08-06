#include "loadstoreoci.h"

#include <iostream>
using namespace std;

#define _CARRY_BITIDX  0
#define _CARRY_BIT     (_flags >> _CARRY_BITIDX) & 1

#define _SET_CARRY_BIT    _flags |= 1 << _CARRY_BITIDX
#define _UNSET_CARRY_BIT  _flags &= ~(1 << _CARRY_BITIDX)

#define RAM(i) _touch(i)

void LoadStoreOci::mov_a_addr()    { _a = RAM(_addr); }
void LoadStoreOci::mov_b_addr()    { _b = RAM(_addr); }
void LoadStoreOci::mov_addr_a()    { RAM(_addr) = _a; }
void LoadStoreOci::mov_addr_b()    { RAM(_addr) = _b; }
void LoadStoreOci::mov_addrl_a()   { ((unsigned char*) &_addr)[0] = _a; }
void LoadStoreOci::mov_addrh_a()   { ((unsigned char*) &_addr)[1] = _a; }
void LoadStoreOci::jnc_addr()      { if (!_CARRY_BIT) _counter = _addr; }
void LoadStoreOci::subb()          { unsigned char carry = _CARRY_BIT; _a -= _b + carry; }
void LoadStoreOci::cpl_a()         { _a = ~_a; }
void LoadStoreOci::clr_c()         { _UNSET_CARRY_BIT; }
void LoadStoreOci::cpl_c()         { _flags ^= 1 << _CARRY_BITIDX; }
void LoadStoreOci::andl()          { _a &= _b; }
void LoadStoreOci::norl()          { _a = ~(_a|_b); }
void LoadStoreOci::out_a()         { _out(_a); }
