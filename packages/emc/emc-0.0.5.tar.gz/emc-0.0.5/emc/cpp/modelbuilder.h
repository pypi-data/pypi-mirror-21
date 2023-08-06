/**
 * C++ library for building a musical model from a bytearray.
 *
 * \author Csaba Sulyok
 */


#pragma once


// 1 note is defined by 6 properties, 16bits per property, i.e. 6*2=12 bytes
#define props_per_note 6u


/**
 * C++ library which interprets the output information of a virtual machine
 * and build a musical model's data from it.
 *
 * Provides adding notes from byte array & updating length.
 */
class ModelBuilder
{
public:

  ModelBuilder(unsigned char numTracks = 4, bool restsEnabled = false, bool velocityEnabled = false,
               bool omitZeroDurations = true, bool omitZeroPitches = true, bool omitZeroVelocities = true,
               unsigned char ioiMask = 0xFF, unsigned char durationMask = 0xFF,
               unsigned char pitchMask = 0x7F, unsigned char velocityMask = 0x7F,
               bool debug = false);


  ~ModelBuilder();


  // ===========================
  // externally callable methods
  // ===========================

  /**
   * Main input method
   * -----------------
   * Given a byte array of arbitrary size, this method chops it up
   * and adds notes for each 5 bytes it can fully read from it.
   */
  void addNotesFromBytes(unsigned char* inp, int inp_size);

  /**
   * Clear model builder.
   * Resets all read/write pointers.
   * Doesn't deallocate/delete, but old data becomes inaccesible without overwriting.
   */
  void clear();

  /**
   * Returns the number of notes present on a given track.
   */
  unsigned int numNotes(unsigned char trackIdx);

  /**
   * Returns the length in ticks of a given track.
   * This property is updated when reading from byte array.
   */
  unsigned int length();

  /**
   * Returns the length in ticks of the whole piece.
   * Is the maximum of the track lengths.
   */
  unsigned int length(unsigned char trackIdx);

  /**
   * Returns how many bytes are needed for one note.
   */
  unsigned int bytesPerNote();

  /**
   * Main output method
   * ------------------
   * Copies accumulated notes for a track into an array.
   * This array must be 1-D because of swig-numpy limitations,
   * but can be safely reshaped to props_per_note * numNotes
   */
  void notes(unsigned short* outp, int outp_size, unsigned char trackIdx);

  /**
   * Setter of debug flag.
   * For info on every note added, enable this.
   * By default, debug flag is false.
   */
  void setDebug(bool debug);


private:


  // =======================
  // Internal helper methods
  // =======================

  /**
   * Since the number of notes cannot be known in advance,
   * it must be dynamically allocated/extended.
   * This method extends the note buffer for a given track if necessary.
   */
  void _checkAndExtendData(unsigned char trackIdx, unsigned char num = 1);

  /**
   * Add a note from bytes and increase read/write pointers.
   * Helper for main input method.
   */
  void _addNoteFromBytes(unsigned char* bytes);


  // =======
  // members
  // =======

  /**
   * Main data object
   * ----------------
   * 3-D array with the musical score information.
   *   Dimension 1: Track index
   *   Dimension 2: Property index
   *   Dimension 3: Note index
   *
   * Example: _data[i][0][j] = onset of j-th note of track i
   */
  unsigned short*** _data;

  unsigned short _numTracks;

  unsigned int* _allocatedPerTrack;
  unsigned short* _onsetShiftByRests;
  unsigned short* _length;


  /**
   * Debug flag. The process prints info about every added note when this is enabled.
   */
  bool _debug;


  /**
   * Number of bytes allocated for a note.
   * Changes based on velocity enablement flag.
   */
  unsigned int _bytesPerNote;


  /**
   * Enablement flags.
   */
  bool _restsEnabled;
  bool _velocityEnabled;


  /**
   * Ommission flags for 0-values.
   */
  bool _omitZeroDurations;
  bool _omitZeroPitches;
  bool _omitZeroVelocities;


  /**
   * Property masks.
   */
  unsigned char _ioiMask;
  unsigned char _durationMask;
  unsigned char _pitchMask;
  unsigned char _velocityMask;


  /**
   * Position of read pointer from input byte array.
   */
  unsigned int _readPtr;


  /**
   * Position of write pointer to data matrix.
   * Has one value per track, one of these is updated on each valid note.
   */
  unsigned int* _writePtr;
};
