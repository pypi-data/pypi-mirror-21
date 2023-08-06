/**
 * WARNING
 * =======
 * This is a generated file that can be overwritten with regeneration.
 * It is an op-code interpreter for the op code state machine ImmediateHarvard.
 */


#pragma once

#include <stdio.h>
#include <string.h>

/**
 * Class for op-code interpreter ImmediateHarvard
 * Description: OCI with immediate addressing (parameters of instructions in subsequent byte(s))
 */
class ImmediateHarvardOci
{
public:

  ImmediateHarvardOci(unsigned int ramSize, unsigned int romSize, 
                unsigned int maxCommands, unsigned int maxOutputs, bool haltAllowed);
  ~ImmediateHarvardOci();


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

  void rom(unsigned char* outp, int outp_size);
  unsigned char romAt(unsigned short index);
  void setRom(unsigned char* inp, int inp_size);
  void setRomAt(unsigned short index, unsigned char value);

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
  void moviR_DPtr(unsigned char r); // 00101 - Copies 1 byte from memory where dataPtr points, into given register, and increases dataPtr
  void movDPtr_R(unsigned char r); // 00110 - Copies value of given register to the memory where dataPtr points
  void moviDPtr_R(unsigned char r); // 00111 - Copies value of given register to the memory where dataPtr points, and increases dataPtr
  void movR_Next(unsigned char r); // 01000 - Copies next byte after call into given register
  void movR_A(unsigned char r); // 01001 - Copies acc into given register
  void movA_R(unsigned char r); // 01010 - Copies given register into acc
  void xchA_R(unsigned char r); // 01011 - Exchanges values of acc and given register
  void movA_DH(); // 01100000 - Copies high byte of dataPtr into acc
  void movA_DL(); // 01100001 - Copies value of acc into high byte of dataPtr
  void movDH_A(); // 01100010 - Copies low byte of dataPtr into acc
  void movDL_A(); // 01100011 - Copies value of acc into low byte of dataPtr
  void movA_DPtr(); // 01100100 - Copies 1 byte from memory where dataPtr points, into acc
  void moviA_DPtr(); // 01100101 - Copies 1 byte from memory where dataPtr points, into acc, and increases dataPtr
  void movDPtr_A(); // 01100110 - Copies value of acc to the memory where dataPtr points
  void moviDPtr_A(); // 01100111 - Copies value of acc to the memory where dataPtr points, and increases dataPtr
  void xchA_DPtr(); // 01101000 - Exchanges values of acc and the memory where dataPtr points
  void xchiA_DPtr(); // 01101001 - Exchanges values of acc and the memory where dataPtr points, and increases dataPtr
  void movDPtr_Next(); // 01101010 - Copies next byte after call into memory where dataPtr points
  void movDH_Next(); // 01101011 - Copies next byte after call into high byte of dataPtr
  void movDL_Next(); // 01101100 - Copies next byte after call into low byte of dataPtr
  void movA_Next(); // 01101101 - Copies next byte after call into acc
  void cplC(); // 01101110 - Inverts value of carry flag
  void inc_A(); // 01101111 - Increments value of acc
  void inc_R(unsigned char r); // 01110 - Increments value of a given register
  void dec_R(unsigned char r); // 01111 - Decrements value of a given register
  void dec_A(); // 10000000 - Decrements value of acc
  void inc_D(); // 10000001 - Increments value of dataPtr
  void dec_D(); // 10000010 - Decrements value of dataPtr
  void cplA(); // 10000011 - Inverts value of acc bitwise
  void anlA_Next(); // 10000100 - Performs bitwise and between acc and next byte after call
  void orlA_Next(); // 10000101 - Performs bitwise or between acc and next byte after call
  void anlA_DPtr(); // 10000110 - Performs bitwise and between acc and memory where dataPtr points
  void orlA_DPtr(); // 10000111 - Performs bitwise or between acc and memory where dataPtr points
  void anlA_R(unsigned char r); // 10001 - Performs bitwise and between acc and given register
  void orlA_R(unsigned char r); // 10010 - Performs bitwise or between acc and given register
  void addA_R(unsigned char r); // 10011 - Adds value of given register to acc
  void addcA_R(unsigned char r); // 10100 - Adds value of given register to acc, with carry
  void subA_R(unsigned char r); // 10101 - Subtracts value of given register from acc
  void subbA_R(unsigned char r); // 10110 - Subtracts value of given register from acc, with borrow
  void addA_Next(); // 10111000 - Adds value of next byte after call to acc
  void addcA_Next(); // 10111001 - Adds value of next byte after call to acc, with carry
  void subA_Next(); // 10111010 - Subtracts value of next byte after call from acc
  void subbA_Next(); // 10111011 - Subtracts value of next byte after call from acc, with borrow
  void addA_DPtr(); // 10111100 - Adds value of memory where dataPtr points to acc
  void addcA_DPtr(); // 10111101 - Adds value of memory where dataPtr points to acc, with carry
  void subA_DPtr(); // 10111110 - Subtracts value of memory where dataPtr points from acc
  void subbA_DPtr(); // 10111111 - Subtracts value of memory where dataPtr points from acc, with borrow
  void rlA(); // 11000000 - Rotates acc left with 1 bit
  void rrA(); // 11000001 - Rotates acc right with 1 bit
  void rlcA(); // 11000010 - Rotates acc left with 1 bit, using carry flag
  void rrcA(); // 11000011 - Rotates acc right with 1 bit, using carry flag
  void pushDH(); // 11000100 - Pushes high byte of dataPtr to stack
  void popDH(); // 11000101 - Pops high byte of dataPtr from stack
  void pushDL(); // 11000110 - Pushes low byte of dataPtr to stack
  void popDL(); // 11000111 - Pops low byte of dataPtr from stack
  void pushA(); // 11001000 - Pushes value of acc to stack
  void popA(); // 11001001 - Pops value of acc from stack
  void sjmpNext(); // 11001010 - Short jumps program counter with value of next byte
  void jmpNext(); // 11001011 - Absolute jumps to memory address given by next 2 bytes
  void jmpD(); // 11001100 - Absolute jumps to value of dataPtr
  void callD(); // 11001101 - Pushes program counter, and then jmpD
  void callNext(); // 11001110 - Pushes program counter, and then jmpNext
  void ret(); // 11001111 - Pops program counter from stack
  void jnc_D(); // 11010000 - jmpD if carry bit is not set
  void jc_D(); // 11010001 - jmpD if carry bit is set
  void sjnc_Next(); // 11010010 - sjmpNext if carry bit is not set
  void sjc_Next(); // 11010011 - sjmpNext if carry bit is set
  void jnc_Next(); // 11010100 - jmpNext if carry bit is not set
  void jc_Next(); // 11010101 - jmpNext if carry bit is set
  void jnzA_D(); // 11010110 - jmpD if acc is not zero
  void jzA_D(); // 11010111 - jmpD if acc is zero
  void sjnzA_Next(); // 11011000 - sjmpNext if acc is not zero
  void sjzA_Next(); // 11011001 - sjmpNext if acc is zero
  void jnzA_Next(); // 11011010 - jmpNext if acc is not zero
  void jzA_Next(); // 11011011 - jmpNext if acc is zero
  void csjneA_Next_Next(); // 11011100 - sjmpNext if acc and next byte are not equal
  void cjneA_Next_Next(); // 11011101 - jmpNext if acc and next byte are not equal
  void cjneA_Next_D(); // 11011110 - jmpD if acc and next byte are not equal
  void halt(); // 11011111 - Signals the VM to halt
  void outR(unsigned char r); // 11100 - Outputs the value of a given register
  void outDPtr(unsigned char n); // 11101 - Outputs next n bytes from where dataPtr points
  void outiDPtr(unsigned char n); // 11110 - Outputs next n bytes from where dataPtr points, and increases dataPtr with n
  void outNext(unsigned char n); // 11111 - Outputs next n bytes from memory


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
  unsigned char* _rom;
  unsigned int _romSize;
  unsigned int _romMask;
  
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
  
  void _interpret_01100(unsigned char cmd);
  void _interpret_01101(unsigned char cmd);
  void _interpret_10000(unsigned char cmd);
  void _interpret_10111(unsigned char cmd);
  void _interpret_11000(unsigned char cmd);
  void _interpret_11001(unsigned char cmd);
  void _interpret_11010(unsigned char cmd);
  void _interpret_11011(unsigned char cmd);


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
