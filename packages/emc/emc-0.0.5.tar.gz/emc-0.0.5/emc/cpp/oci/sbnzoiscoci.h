/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine SbnzOisc.
 */


#pragma once

#include <stdio.h>
#include <string.h>

/**
 * Class for op-code interpreter SbnzOisc
 * Description: One-instruction set computer (OISC) using SBNZ and the von Neumann architecture
 */
class SbnzOiscOci
{
public:

  SbnzOiscOci(unsigned int ramSize, 
                unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed);
  ~SbnzOiscOci();


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
   * Interpret n RAM commands.
   * Doesn't stop in either case the interpret() method would.
   * Use for performance testing.
   */
  void interpretN(unsigned int n);

  
  // =========
  // constants
  // =========
  
  static const unsigned int counterSize = 2;
  static const unsigned int numRegisters = 0;
  static const unsigned int numCategories = 1;
  
  
  // ===============
  // getters-setters
  // ===============

  const unsigned int geneticStringSize();
  
  unsigned short counter();
  void setCounter(unsigned short counter);
  

  void ram(unsigned short* outp, int outp_size);
  unsigned short ramAt(unsigned short index);
  void setRam(unsigned short* inp, int inp_size);
  void setRamAt(unsigned short index, unsigned short value);

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
  
  void sbnz(); //  - SBNZ AddrA, AddrB, AddrC, AddrD: Subtract value at ram[AddrB] from value at ram[AddrA]; store result in ram[AddrC]; if result was not zero, branch to AddrD; if underflow occurred, output ram[addrA]+ram[addrB].


private:

  // =======
  // members
  // =======

  unsigned int _geneticStringSize;
    
  bool _haltFlag;
  unsigned int _maxCommands;
  unsigned int _maxOutputs;
  bool _haltAllowed;

  unsigned short _counter; // program counter
  // additional registers
  
  // flexible memory segments
  unsigned short* _ram;
  unsigned int _ramSize;
  unsigned int _ramMask;
  
  // fixed memory segments
  
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
  unsigned short& _touch(unsigned int pos);
  
  /**
   * Reset counters for occurrences.
   */
  void _resetOccurrences();
  
  /**
   * Reset counters for how many bytes are touched.
   */
  void _resetTouched();
};
