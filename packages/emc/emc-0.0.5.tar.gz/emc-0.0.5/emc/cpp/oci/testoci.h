/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine Test.
 */


#pragma once

#include <stdio.h>
#include <string.h>

/**
 * Class for op-code interpreter Test
 * Description: OCI for testing and demonstration purposes
 */
class TestOci
{
public:

  TestOci(unsigned int ramSize, 
                unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed);
  ~TestOci();


  // ===========================
  // externally callable methods
  // ===========================

  /**
   * Sets condition of VM using a genetic string (stored in inp).
   */
  void setFromGeneticString(unsigned char* inp, int inp_size);

  /**
   * Interpret RAM commands.
   * Reads bytes from where program counter points, and executes the mapped instructions.
   * Stops if halt flag set or if a maximum number of commands/outputs reached.
   */
  void interpret();

  /**
   * Interpret upcoming command.
   * Reads a byte from memory and bit-parses it to find the correct instruction to call.
   */
  void interpretNext();
  
  /**
   * Interpret n RAM commands.
   * Doesn't stop in either case the interpret() method would.
   * Use for performance testing.
   */
  void interpretN(unsigned int n);

  
  // =========
  // constants
  // =========
  
  static const unsigned int counterSize = 1;
  static const unsigned int numRegisters = 8;
  static const unsigned int numCategories = 2;
  
  
  // ===============
  // getters-setters
  // ===============

  const unsigned int geneticStringSize();
  
  unsigned char counter();
  void setCounter(unsigned char counter);
  
  void registers(unsigned char* outp, int outp_size);
  unsigned char registerAt(unsigned short index);
  void setRegisters(unsigned char* inp, int inp_size);
  void setRegister(unsigned short index, unsigned char value);
  
  unsigned char acc();
  void setAcc(unsigned char acc);
  unsigned short dptr();
  void setDptr(unsigned short dptr);

  void ram(unsigned char* outp, int outp_size);
  unsigned char ramAt(unsigned short index);
  void setRam(unsigned char* inp, int inp_size);
  void setRamAt(unsigned short index, unsigned char value);

  void stack(unsigned char* outp, int outp_size);
  unsigned char stackAt(unsigned short index);
  void setStack(unsigned char* inp, int inp_size);
  void setStackAt(unsigned short index, unsigned char value);

  void output(unsigned char* outp, int outp_size);
  unsigned char outputAt(unsigned short index);
  void setOutput(unsigned char* inp, int inp_size);
  void setOutputAt(unsigned short index, unsigned char value);
  unsigned int outputPtr();
  void setOutputPtr(unsigned int outputPtr);
  
  bool debug();
  void setDebug(bool debug);
  bool countOccurrences();
  void setCountOccurrences(bool countOccurrences);
  bool countTouched();
  void setCountTouched(bool countTouched);
  int numTouched();
  void setNumTouched(int numTouched);
  
  void occurrences(unsigned int* outp, int outp_size);
  unsigned int occurrencesAt(unsigned short index);
  void setOccurrences(unsigned int* inp, int inp_size);
  void setOccurrencesAt(unsigned short index, unsigned int value);
  
  void touched(unsigned short* outp, int outp_size);
  unsigned short touchedAt(unsigned short index);
  void setTouched(unsigned short* inp, int inp_size);
  void setTouchedAt(unsigned short index, unsigned short value);

  
  // ===================================
  // assigned states - main instructions
  // ===================================
  
  void a(); // 00 - test method a
  void b(unsigned char r1); // 01 - test method b
  void c(); // 1000 - test method c
  void d(); // 1001 - test method d
  void e(); // 1010 - test method e
  void f(unsigned char r1); // 10110 - test method f
  void g(); // 10111 - test method g
  void h(unsigned char r1); // 11 - test method h


private:

  // =======
  // members
  // =======

  unsigned int _geneticStringSize;
    
  bool _haltFlag;
  unsigned int _maxCommands;
  unsigned int _maxOutputs;
  bool _haltAllowed;

  unsigned char _counter; // program counter
  // registers
  unsigned char* _registers; // general-purpose registers
  // additional registers
  unsigned char _acc;
  unsigned short _dptr;
  
  // flexible memory segments
  unsigned char* _ram;
  unsigned int _ramSize;
  unsigned int _ramMask;
  
  // fixed memory segments
  unsigned char* _stack;
  
  unsigned char* _output; // output memory block
  unsigned int _outputPtr; // output write pointer
  unsigned int _outputAllocated;

  bool _debug;
  bool _countOccurrences;
  unsigned int* _occurrences; // count occurrences of command types in debug mode
  bool _countTouched;
  int _numTouched;
  unsigned short* _touched; // mark touched bytes in the ram


  // ===========================
  // private interpreter methods
  // ===========================

  // =================================================
  // further interpret pending states in state machine
  // =================================================
  
  void _interpret_10(unsigned char cmd);
  void _interpret_1011(unsigned char cmd);


  // =====================
  // extra private methods
  // =====================

  /**
   * Sets halt flag to true.
   * Only stops execution if it was called with interpret().
   */
  void _halt();

  /**
   * Outputs byte to output array and increases output write pointer.
   */
  void _out(unsigned char byte);
  void _out(unsigned char* bytes, unsigned short pos, unsigned char num);
  void _out(unsigned char* bytes, unsigned short pos, unsigned char num, unsigned int mask);
  

  /**
   * If allocated output size has been reached, extends and copies output array.
   * TODO: optimize using paging?
   */
  void _checkAndExtendOutput(unsigned char num = 1);
  
  /**
   * "Touch" byte in RAM (increase its heat) and return reference to it.
   */
  unsigned char& _touch(unsigned int pos);
  
  /**
   * Reset counters for occurrences.
   */
  void _resetOccurrences();
  
  /**
   * Reset counters for how many bytes are touched.
   */
  void _resetTouched();
};
