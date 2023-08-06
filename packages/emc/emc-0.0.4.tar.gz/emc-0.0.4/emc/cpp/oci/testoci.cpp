#include "testoci.h"

#include <iostream>
using namespace std;

#define RAM(i) _touch(i)

void TestOci::a()                 { cout << "a " << endl; }
void TestOci::b(unsigned char r1) { cout << "b " << (int) r1 << " " << endl; }
void TestOci::c()                 { cout << "c " << endl; }
void TestOci::d()                 { cout << "d " << endl; }
void TestOci::e()                 { cout << "e " << endl; }
void TestOci::f(unsigned char r1) { cout << "f " << (int) r1 << " " << endl; }
void TestOci::g()                 { cout << "g " << endl; }
void TestOci::h(unsigned char r1) { cout << "h " << (int) r1 << " " << endl; }
