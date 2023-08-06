#include "modelbuilder.h"

#include <iostream>
using namespace std;

#define ALLOCATION_UNIT 1024


ModelBuilder::ModelBuilder(unsigned char numTracks, bool restsEnabled, bool velocityEnabled,
                           bool omitZeroDurations, bool omitZeroPitches, bool omitZeroVelocities,
                           unsigned char ioiMask, unsigned char durationMask, unsigned char pitchMask, unsigned char velocityMask,
                           bool debug) :
    _numTracks(numTracks), _debug(debug), _readPtr(0), _bytesPerNote(velocityEnabled + 4u),
    _restsEnabled(restsEnabled), _velocityEnabled(velocityEnabled),
    _omitZeroDurations(omitZeroDurations), _omitZeroPitches(omitZeroPitches), _omitZeroVelocities(omitZeroVelocities),
    _ioiMask(ioiMask), _durationMask(durationMask), _pitchMask(pitchMask), _velocityMask(velocityMask)
{
  _allocatedPerTrack = new unsigned int[_numTracks];
  _onsetShiftByRests = new unsigned short[_numTracks];
  _length = new unsigned short[_numTracks];
  _writePtr = new unsigned int[_numTracks];

  _data = new unsigned short**[_numTracks];

  for (unsigned int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
  {
    _allocatedPerTrack[trackIdx] = ALLOCATION_UNIT;
    _onsetShiftByRests[trackIdx] = 0;
    _length[trackIdx] = 0;
    _writePtr[trackIdx] = 0;
    _data[trackIdx] = new unsigned short*[props_per_note];

    for (unsigned int propIdx = 0; propIdx < props_per_note; ++propIdx)
    {
      _data[trackIdx][propIdx] = new unsigned short[_allocatedPerTrack[trackIdx]];
    }
  }
}


ModelBuilder::~ModelBuilder()
{
  for (unsigned int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
  {
    for (unsigned int propIdx = 0; propIdx < props_per_note; ++propIdx)
    {
      delete [] _data[trackIdx][propIdx];
    }

    delete [] _data[trackIdx];
  }

  delete [] _allocatedPerTrack;
  delete [] _onsetShiftByRests;
  delete [] _length;
  delete [] _writePtr;

  delete [] _data;
}


void ModelBuilder::_checkAndExtendData(unsigned char trackIdx, unsigned char num)
{
  if (_writePtr[trackIdx] + num > _allocatedPerTrack[trackIdx])
  {
    // TODO implement paging for efficiency
    _allocatedPerTrack[trackIdx] += ALLOCATION_UNIT;

    unsigned short** newData = new unsigned short*[props_per_note];
    for (unsigned int propIdx = 0; propIdx < props_per_note; ++propIdx)
    {
      newData[propIdx] = new unsigned short[_allocatedPerTrack[trackIdx]];
    }

    for (unsigned int propIdx = 0; propIdx < props_per_note; ++propIdx)
    {
      for (unsigned int noteIdx = 0; noteIdx < _writePtr[trackIdx]; ++noteIdx)
      {
        newData[propIdx][noteIdx] = _data[trackIdx][propIdx][noteIdx];
      }
    }

    delete _data[trackIdx];
    _data[trackIdx] = newData;
  }
}


void ModelBuilder::setDebug(bool debug)
{
  _debug = debug;
}


void ModelBuilder::clear()
{
  _readPtr = 0;
  for (unsigned int trackIdx = 0; trackIdx < _numTracks; ++trackIdx)
  {
    _length[trackIdx] = 0;
    _onsetShiftByRests[trackIdx] = 0;
    _writePtr[trackIdx] = 0;
  }
}


unsigned int ModelBuilder::numNotes(unsigned char trackIdx)
{
  return trackIdx >= 0 && trackIdx < _numTracks ?
      _writePtr[trackIdx] : 0;
}


void ModelBuilder::notes(unsigned short* notes, int notes_size, unsigned char trackIdx)
{
  unsigned int numNotes = _writePtr[trackIdx];
  for (unsigned int propIdx = 0; propIdx < props_per_note; ++propIdx)
  {
    for (unsigned int noteIdx = 0; noteIdx < numNotes; ++noteIdx)
    {
      notes[noteIdx * props_per_note + propIdx] = _data[trackIdx][propIdx][noteIdx];
    }
  }
}


unsigned int ModelBuilder::length()
{
  unsigned int ret = length(0);
  unsigned int other;

  for (unsigned int trackIdx = 1; trackIdx < _numTracks; ++trackIdx)
  {
    other = _length[trackIdx];
    if (ret < other)
    {
      ret = other;
    }
  }

  return ret;
}


unsigned int ModelBuilder::length(unsigned char trackIdx)
{
  if (trackIdx < 0 || trackIdx >= _numTracks || _writePtr[trackIdx] == 0)
  {
    return 0;
  }

  return _length[trackIdx];
}


unsigned int ModelBuilder::bytesPerNote()
{
  return _bytesPerNote;
}



// ============
// adding notes
// ============


void ModelBuilder::addNotesFromBytes(unsigned char* bytes, int bytes_size)
{
  _readPtr = 0;

  if (_debug)
  {
    cout << "Adding as many notes as possible from " << bytes_size << " bytes" << endl;
  }
  while (_readPtr + _bytesPerNote <= bytes_size)
  {
    _addNoteFromBytes(bytes);
  }
}


void ModelBuilder::_addNoteFromBytes(unsigned char* bytes)
{
  unsigned char trackIdx = bytes[_readPtr] % _numTracks;

  /**
   * Need a rest if it is enabled, the pitch is showing a rest flag (MSB)
   * and the velocity either also shows it or is not enabled.
   */
  bool restFlag = _restsEnabled &&
      (bytes[_readPtr + 3] >> 7) &&
      (!_velocityEnabled || (bytes[_readPtr + 4] >> 7));

  /**
   * Omit note if 0s are omitted and note has 0s masking provides 0 or
   */
  bool omitFlag =
      (_omitZeroDurations  && (bytes[_readPtr + 2] & _durationMask) == 0) ||
      (_omitZeroPitches    && (bytes[_readPtr + 3] & _pitchMask   ) == 0) ||
      (_velocityEnabled    &&
       _omitZeroVelocities && (bytes[_readPtr + 4] & _velocityMask) == 0);


  /**
   * Prints bytes used to construct new note.
   */
  if (_debug)
  {
    cout << "Adding note from bytes: [" << (short) bytes[_readPtr];
    for (unsigned int i = 1; i < _bytesPerNote; ++i)
    {
      cout << ", " << (short) bytes[_readPtr + i];
    }
    cout << "]" << endl;
  }


  if (restFlag)
  {
    _onsetShiftByRests[trackIdx] += bytes[_readPtr + 1];
    if (_debug)
    {
      cout << "Rest detected. Shifting onset on track " << (short) trackIdx << " to " << _onsetShiftByRests[trackIdx] << endl;
    }
  }
  else if (omitFlag)
  {
    if (_debug)
    {
      cout << "Bytes ignored because zero. Duration = " << (bytes[_readPtr + 2] & _durationMask)
           << ", pitch = " << (bytes[_readPtr + 3] & _pitchMask) << endl;
    }
  }
  else
  {
    _checkAndExtendData(trackIdx);

    unsigned int noteIdx = _writePtr[trackIdx];
    
    _data[trackIdx][0][noteIdx] = _onsetShiftByRests[trackIdx] + (bytes[_readPtr + 1] & _ioiMask);  // inter-onset interval
    _data[trackIdx][1][noteIdx] = bytes[_readPtr + 2] & _durationMask;                              // duration
    _data[trackIdx][2][noteIdx] = (noteIdx == 0 ? 0 : _data[trackIdx][2][noteIdx - 1])
                                  + _data[trackIdx][0][noteIdx];                                    // onset
    _data[trackIdx][3][noteIdx] = _data[trackIdx][2][noteIdx] + _data[trackIdx][1][noteIdx];        // offset
    _data[trackIdx][4][noteIdx] = bytes[_readPtr + 3] & _pitchMask;                                 // pitch
    _data[trackIdx][5][noteIdx] = _velocityEnabled ? (bytes[_readPtr + 4] & _velocityMask) : 127;   // velocity

    _onsetShiftByRests[trackIdx] = 0;

    if (_length[trackIdx] < _data[trackIdx][3][noteIdx])
    {
      _length[trackIdx] = _data[trackIdx][3][noteIdx];
    }

    if (_debug)
    {
      // if onset smaller than previous one, overflow occurred
      if (noteIdx > 0 && _data[trackIdx][2][noteIdx] < _data[trackIdx][2][noteIdx - 1])
      {
        cout << "WARNING: Overflow occurred when building model. Behavior unpredictable." << endl;
      }

      cout << "New note added. TrackIdx = " << (short) trackIdx << ", NoteIdx = " << noteIdx;
      cout << ", Interonset = "  << _data[trackIdx][0][noteIdx] << ", Duration = " << _data[trackIdx][1][noteIdx];
      cout << ", Onset = "       << _data[trackIdx][2][noteIdx] << ", Offset = " << _data[trackIdx][3][noteIdx];
      cout << ", Pitch = "       << _data[trackIdx][4][noteIdx] << ", Velocity = " << _data[trackIdx][5][noteIdx] << endl;
      cout << "New length "      << (short) trackIdx << ": " << _length[trackIdx] << endl;
    }

    _writePtr[trackIdx]++;
  }

  _readPtr += _bytesPerNote;
}
