/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine LoadStore.
 */


#pragma once

#include <stdio.h>
#include <string.h>

/**
 * Class for op-code interpreter LoadStore
 * Description: 
 */
class LoadStoreOci
{
public:

  LoadStoreOci(unsigned int ramSize, 
                unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed);
  ~LoadStoreOci();


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
  
  static const unsigned int counterSize = 2;
  static const unsigned int numRegisters = 0;
  static const unsigned int numCategories = 2;
  
  
  // ===============
  // getters-setters
  // ===============

  const unsigned int geneticStringSize();
  
  unsigned short counter();
  void setCounter(unsigned short counter);
  
  unsigned char a();
  void setA(unsigned char a);
  unsigned char b();
  void setB(unsigned char b);
  unsigned char flags();
  void setFlags(unsigned char flags);
  unsigned short addr();
  void setAddr(unsigned short addr);

  void ram(unsigned char* outp, int outp_size);
  unsigned char ramAt(unsigned short index);
  void setRam(unsigned char* inp, int inp_size);
  void setRamAt(unsigned short index, unsigned char value);

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
  
  void mov_a_addr(); // 0000 - 
  void mov_b_addr(); // 0001 - 
  void mov_addr_a(); // 0010 - 
  void mov_addr_b(); // 0011 - 
  void mov_addrl_a(); // 0100 - 
  void mov_addrh_a(); // 0101 - 
  void jnc_addr(); // 011 - 
  void subb(); // 1000 - 
  void cpl_a(); // 1001 - 
  void clr_c(); // 1010 - 
  void cpl_c(); // 1011 - 
  void andl(); // 1100 - 
  void norl(); // 1101 - 
  void out_a(); // 111 - 


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
  unsigned char _a;
  unsigned char _b;
  unsigned char _flags;
  unsigned short _addr;
  
  // flexible memory segments
  unsigned char* _ram;
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
  
  void _interpret_0(unsigned char cmd);
  void _interpret_00(unsigned char cmd);
  void _interpret_000(unsigned char cmd);
  void _interpret_001(unsigned char cmd);
  void _interpret_01(unsigned char cmd);
  void _interpret_010(unsigned char cmd);
  void _interpret_1(unsigned char cmd);
  void _interpret_10(unsigned char cmd);
  void _interpret_100(unsigned char cmd);
  void _interpret_101(unsigned char cmd);
  void _interpret_11(unsigned char cmd);
  void _interpret_110(unsigned char cmd);


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
