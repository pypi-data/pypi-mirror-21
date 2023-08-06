/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine StackHarvard.
 */


#pragma once

#include <stdio.h>
#include <string.h>

/**
 * Class for op-code interpreter StackHarvard
 * Description: 
 */
class StackHarvardOci
{
public:

  StackHarvardOci(unsigned int romSize, unsigned int stackSize, 
                unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed);
  ~StackHarvardOci();


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
  
  unsigned short sp();
  void setSp(unsigned short sp);

  void rom(unsigned short* outp, int outp_size);
  unsigned short romAt(unsigned short index);
  void setRom(unsigned short* inp, int inp_size);
  void setRomAt(unsigned short index, unsigned short value);

  void stack(unsigned short* outp, int outp_size);
  unsigned short stackAt(unsigned short index);
  void setStack(unsigned short* inp, int inp_size);
  void setStackAt(unsigned short index, unsigned short value);

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
  
  void dup(); // 000 - Duplicate the stack top. This is the only way to allocate stack space. 
  void one(); // 001 - Shift the stack top left one bit, shifting one into the least significant bit. 
  void zero(); // 010 - Shift the stack top left one bit, shifting zero into the least significant bit.
  void load(); // 011 - Use the value on the stack top as a memory address; replace it with the contents of the referenced location. 
  void pop(); // 100 - Store the value from the top of the stack in the memory location referenced by the second word on the stack; pop both. 
  void sub(); // 101 - Subtract the top value on the stack from the value below it, pop both and push the result. 
  void jpos(); // 110 - If the word below the stack top is positive, jump to the word pointed to by the stack top. In any case, pop both. 
  void out(); // 111 - Write the value of the stack top to the output


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
  unsigned short _sp;
  
  // flexible memory segments
  unsigned short* _rom;
  unsigned int _romSize;
  unsigned int _romMask;
  unsigned short* _stack;
  unsigned int _stackSize;
  unsigned int _stackMask;
  
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
  void _interpret_01(unsigned char cmd);
  void _interpret_1(unsigned char cmd);
  void _interpret_10(unsigned char cmd);
  void _interpret_11(unsigned char cmd);


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
