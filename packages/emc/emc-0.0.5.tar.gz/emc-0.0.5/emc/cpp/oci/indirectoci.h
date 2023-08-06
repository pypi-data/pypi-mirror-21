/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine Indirect.
 */


#pragma once

#include <stdio.h>
#include <string.h>

/**
 * Class for op-code interpreter Indirect
 * Description: OCI with no immediate addressing, every instruction is exactly 8 bits
 */
class IndirectOci
{
public:

  IndirectOci(unsigned int ramSize, 
                unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed);
  ~IndirectOci();


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
  static const unsigned int numRegisters = 8;
  static const unsigned int numCategories = 5;
  
  
  // ===============
  // getters-setters
  // ===============

  const unsigned int geneticStringSize();
  
  unsigned short counter();
  void setCounter(unsigned short counter);
  
  void registers(unsigned char* outp, int outp_size);
  unsigned char registerAt(unsigned short index);
  void setRegisters(unsigned char* inp, int inp_size);
  void setRegister(unsigned short index, unsigned char value);
  
  unsigned char acc();
  void setAcc(unsigned char acc);
  unsigned short dataPtr();
  void setDataPtr(unsigned short dataPtr);
  unsigned char flags();
  void setFlags(unsigned char flags);
  unsigned char stackPtr();
  void setStackPtr(unsigned char stackPtr);

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
  
  void movR_DH(unsigned char r); // 00000 - Copies high byte of dataPtr into given register
  void movDH_R(unsigned char r); // 00001 - Copies value of given register into high byte of dataPtr
  void movR_DL(unsigned char r); // 00010 - Copies low byte of dataPtr into given register
  void movDL_R(unsigned char r); // 00011 - Copies value of given register into low byte of dataPtr
  void movR_DPtr(unsigned char r); // 00100 - Copies 1 byte from memory where dataPtr points, into given register
  void movDPtr_R(unsigned char r); // 00101 - Copies value of given register to the memory where dataPtr points
  void movR_A(unsigned char r); // 00110 - Copies acc into given register
  void movA_R(unsigned char r); // 00111 - Copies given register into acc
  void xchA_R(unsigned char r); // 01000 - Exchanges values of acc and given register
  void movA_DH(); // 01001000 - Copies high byte of dataPtr into acc
  void movA_DL(); // 01001001 - Copies value of acc into high byte of dataPtr
  void movDH_A(); // 01001010 - Copies low byte of dataPtr into acc
  void movDL_A(); // 01001011 - Copies value of acc into low byte of dataPtr
  void movA_DPtr(); // 01001100 - Copies 1 byte from memory where dataPtr points, into acc
  void movDPtr_A(); // 01001101 - Copies value of acc to the memory where dataPtr points
  void cplC(); // 01001110 - Inverts value of carry flag
  void inc_A(); // 01001111 - Increments value of acc
  void dec_A(); // 01010000 - Decrements value of acc
  void inc_D(); // 01010001 - Increments value of dataPtr
  void dec_D(); // 01010010 - Decrements value of dataPtr
  void cplA(); // 01010011 - Inverts value of acc bitwise
  void anlA_RPtr(unsigned char rp); // 010101 - Performs bitwise and between acc and memory memory where given register points
  void anlA_R(unsigned char r); // 01011 - Performs bitwise and between acc and given register
  void orlA_R(unsigned char r); // 01100 - Performs bitwise or between acc and given register
  void addA_R(unsigned char r); // 01101 - Adds value of given register to acc
  void addcA_R(unsigned char r); // 01110 - Adds value of given register to acc, with carry
  void subA_R(unsigned char r); // 01111 - Subtracts value of given register from acc
  void subbA_R(unsigned char r); // 10000 - Subtracts value of given register from acc, with borrow
  void orlA_RPtr(unsigned char rp); // 100010 - Performs bitwise or between acc and memory memory where given register points
  void anlA_DPtr(); // 10001100 - Performs bitwise and between acc and memory where dataPtr points
  void orlA_DPtr(); // 10001101 - Performs bitwise or between acc and memory where dataPtr points
  void addA_DPtr(); // 10001110 - Adds value of memory where dataPtr points to acc
  void addcA_DPtr(); // 10001111 - Adds value of memory where dataPtr points to acc, with carry
  void addA_RPtr(unsigned char rp); // 100100 - Adds value of memory where given register points to acc
  void addcA_RPtr(unsigned char rp); // 100101 - Adds value of memory where given register points to acc, with carry
  void subA_RPtr(unsigned char rp); // 100110 - Subtracts value of memory where given register points from acc
  void subbA_RPtr(unsigned char rp); // 100111 - Subtracts value of memory where given register points from acc, with borrow
  void subA_DPtr(); // 10100000 - Subtracts value of memory where dataPtr points from acc
  void subbA_DPtr(); // 10100001 - Subtracts value of memory where dataPtr points from acc, with borrow
  void rlA(); // 10100010 - Rotates acc left with 1 bit
  void rrA(); // 10100011 - Rotates acc right with 1 bit
  void rlcA(); // 10100100 - Rotates acc left with 1 bit, using carry flag
  void rrcA(); // 10100101 - Rotates acc right with 1 bit, using carry flag
  void pushDH(); // 10100110 - Pushes high byte of dataPtr to stack
  void popDH(); // 10100111 - Pops high byte of dataPtr from stack
  void pushDL(); // 10101000 - Pushes low byte of dataPtr to stack
  void popDL(); // 10101001 - Pops low byte of dataPtr from stack
  void pushA(); // 10101010 - Pushes value of acc to stack
  void popA(); // 10101011 - Pops value of acc from stack
  void pushR(unsigned char r); // 101011 - Pushes value of a register to stack
  void popR(unsigned char r); // 101100 - Pops value of a register from stack
  void sjmpR(unsigned char r); // 101101 - Short jumps program counter with value of register (R0-R3)
  void jmpR(unsigned char rp); // 101110 - Absolute jumps to memory address given by pair of registers
  void jmpD(); // 10111100 - Absolute jumps to value of dataPtr
  void callD(); // 10111101 - Pushes program counter, and then jmpD
  void ret(); // 10111110 - Pops program counter from stack
  void jnc_D(); // 10111111 - jmpD if carry bit is not set
  void scallR(unsigned char r); // 110000 - Pushes program counter, and then sjmpR
  void callR(unsigned char rp); // 110001 - Pushes program counter, and then jmpR
  void jc_D(); // 11001000 - jmpD if carry bit is set
  void jnzA_D(); // 11001001 - jmpD if acc is not zero
  void jzA_D(); // 11001010 - jmpD if acc is zero
  void halt(); // 11001011 - Signals the VM to halt
  void sjnc_R(unsigned char r); // 110011 - sjmpR if carry bit is not set
  void sjc_R(unsigned char r); // 110100 - sjmpR if carry bit is set
  void jnc_R(unsigned char rp); // 110101 - jmpR if carry bit is not set
  void jc_R(unsigned char rp); // 110110 - jmpR if carry bit is set
  void sjnzA_R(unsigned char r); // 110111 - sjmpR if acc is not zero
  void sjzA_R(unsigned char r); // 111000 - sjmpR if acc is zero
  void jnzA_R(unsigned char rp); // 111001 - jmpR if acc is not zero
  void jzA_R(unsigned char rp); // 111010 - jmpR if acc is zero
  void outRPtr(unsigned char rp); // 111011 - Outputs byte from where a pair of registers is pointing
  void outR(unsigned char r); // 11110 - Outputs the value of a given register
  void outDPtr(unsigned char n); // 11111 - Outputs next n bytes from where dataPtr points


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
  // registers
  unsigned char* _registers; // general-purpose registers
  // additional registers
  unsigned char _acc;
  unsigned short _dataPtr;
  unsigned char _flags;
  unsigned char _stackPtr;
  
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
  
  void _interpret_01001(unsigned char cmd);
  void _interpret_01010(unsigned char cmd);
  void _interpret_010100(unsigned char cmd);
  void _interpret_10001(unsigned char cmd);
  void _interpret_100011(unsigned char cmd);
  void _interpret_10010(unsigned char cmd);
  void _interpret_10011(unsigned char cmd);
  void _interpret_10100(unsigned char cmd);
  void _interpret_10101(unsigned char cmd);
  void _interpret_101010(unsigned char cmd);
  void _interpret_10110(unsigned char cmd);
  void _interpret_10111(unsigned char cmd);
  void _interpret_101111(unsigned char cmd);
  void _interpret_11000(unsigned char cmd);
  void _interpret_11001(unsigned char cmd);
  void _interpret_110010(unsigned char cmd);
  void _interpret_11010(unsigned char cmd);
  void _interpret_11011(unsigned char cmd);
  void _interpret_11100(unsigned char cmd);
  void _interpret_11101(unsigned char cmd);


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
