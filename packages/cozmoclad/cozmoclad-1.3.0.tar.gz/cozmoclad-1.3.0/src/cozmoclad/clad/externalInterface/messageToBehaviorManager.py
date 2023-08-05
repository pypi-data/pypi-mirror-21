# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Autogenerated python message buffer code.
Source: clad/externalInterface/messageToBehaviorManager.clad
Full command line: ../tools/message-buffers/emitters/Python_emitter.py -C ./src/ -I ../robot/clad/src/ ../coretech/vision/clad/src/ ../coretech/common/clad/src/ -o ../generated/cladPython// clad/externalInterface/messageToBehaviorManager.clad
"""

from __future__ import absolute_import
from __future__ import print_function

def _modify_path():
  import inspect, os, sys
  search_paths = [
    '../..',
    '../../../../tools/message-buffers/support/python',
  ]
  currentpath = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
  for search_path in search_paths:
    search_path = os.path.normpath(os.path.abspath(os.path.realpath(os.path.join(currentpath, search_path))))
    if search_path not in sys.path:
      sys.path.insert(0, search_path)
_modify_path()

import msgbuffers

Anki = msgbuffers.Namespace()
Anki.Cozmo = msgbuffers.Namespace()
Anki.Cozmo.Audio = msgbuffers.Namespace()
Anki.Cozmo.Audio.GameState = msgbuffers.Namespace()
Anki.Cozmo.Audio.SwitchState = msgbuffers.Namespace()
Anki.Cozmo.ExternalInterface = msgbuffers.Namespace()

from clad.audio.audioStateTypes import Anki as _Anki
Anki.update(_Anki.deep_clone())

from clad.audio.audioSwitchTypes import Anki as _Anki
Anki.update(_Anki.deep_clone())

from clad.types.behaviorTypes import Anki as _Anki
Anki.update(_Anki.deep_clone())

from clad.types.unlockTypes import Anki as _Anki
Anki.update(_Anki.deep_clone())

class SetAvailableGames(object):
  "Generated message-passing structure."

  __slots__ = (
    '_availableGames', # Anki.Cozmo.BehaviorGameFlag
  )

  @property
  def availableGames(self):
    "Anki.Cozmo.BehaviorGameFlag availableGames struct property."
    return self._availableGames

  @availableGames.setter
  def availableGames(self, value):
    self._availableGames = msgbuffers.validate_integer(
      'SetAvailableGames.availableGames', value, 0, 255)

  def __init__(self, availableGames=Anki.Cozmo.BehaviorGameFlag.NoGame):
    self.availableGames = availableGames

  @classmethod
  def unpack(cls, buffer):
    "Reads a new SetAvailableGames from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('SetAvailableGames.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new SetAvailableGames from the given BinaryReader."
    _availableGames = reader.read('B')
    return cls(_availableGames)

  def pack(self):
    "Writes the current SetAvailableGames, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current SetAvailableGames to the given BinaryWriter."
    writer.write(self._availableGames, 'B')

  def __eq__(self, other):
    if type(self) is type(other):
      return self._availableGames == other._availableGames
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._availableGames, 'B'))

  def __str__(self):
    return '{type}(availableGames={availableGames})'.format(
      type=type(self).__name__,
      availableGames=self._availableGames)

  def __repr__(self):
    return '{type}(availableGames={availableGames})'.format(
      type=type(self).__name__,
      availableGames=repr(self._availableGames))

Anki.Cozmo.ExternalInterface.SetAvailableGames = SetAvailableGames
del SetAvailableGames


class ActivateSpark(object):
  "Generated message-passing structure."

  __slots__ = (
    '_behaviorSpark', # Anki.Cozmo.UnlockId
  )

  @property
  def behaviorSpark(self):
    "Anki.Cozmo.UnlockId behaviorSpark struct property."
    return self._behaviorSpark

  @behaviorSpark.setter
  def behaviorSpark(self, value):
    self._behaviorSpark = msgbuffers.validate_integer(
      'ActivateSpark.behaviorSpark', value, -2147483648, 2147483647)

  def __init__(self, behaviorSpark=Anki.Cozmo.UnlockId.Invalid):
    self.behaviorSpark = behaviorSpark

  @classmethod
  def unpack(cls, buffer):
    "Reads a new ActivateSpark from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('ActivateSpark.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new ActivateSpark from the given BinaryReader."
    _behaviorSpark = reader.read('i')
    return cls(_behaviorSpark)

  def pack(self):
    "Writes the current ActivateSpark, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current ActivateSpark to the given BinaryWriter."
    writer.write(self._behaviorSpark, 'i')

  def __eq__(self, other):
    if type(self) is type(other):
      return self._behaviorSpark == other._behaviorSpark
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._behaviorSpark, 'i'))

  def __str__(self):
    return '{type}(behaviorSpark={behaviorSpark})'.format(
      type=type(self).__name__,
      behaviorSpark=self._behaviorSpark)

  def __repr__(self):
    return '{type}(behaviorSpark={behaviorSpark})'.format(
      type=type(self).__name__,
      behaviorSpark=repr(self._behaviorSpark))

Anki.Cozmo.ExternalInterface.ActivateSpark = ActivateSpark
del ActivateSpark


class SparkUnlocked(object):
  "Generated message-passing structure."

  __slots__ = (
    '_behaviorSpark', # Anki.Cozmo.UnlockId
  )

  @property
  def behaviorSpark(self):
    "Anki.Cozmo.UnlockId behaviorSpark struct property."
    return self._behaviorSpark

  @behaviorSpark.setter
  def behaviorSpark(self, value):
    self._behaviorSpark = msgbuffers.validate_integer(
      'SparkUnlocked.behaviorSpark', value, -2147483648, 2147483647)

  def __init__(self, behaviorSpark=Anki.Cozmo.UnlockId.Invalid):
    self.behaviorSpark = behaviorSpark

  @classmethod
  def unpack(cls, buffer):
    "Reads a new SparkUnlocked from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('SparkUnlocked.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new SparkUnlocked from the given BinaryReader."
    _behaviorSpark = reader.read('i')
    return cls(_behaviorSpark)

  def pack(self):
    "Writes the current SparkUnlocked, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current SparkUnlocked to the given BinaryWriter."
    writer.write(self._behaviorSpark, 'i')

  def __eq__(self, other):
    if type(self) is type(other):
      return self._behaviorSpark == other._behaviorSpark
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._behaviorSpark, 'i'))

  def __str__(self):
    return '{type}(behaviorSpark={behaviorSpark})'.format(
      type=type(self).__name__,
      behaviorSpark=self._behaviorSpark)

  def __repr__(self):
    return '{type}(behaviorSpark={behaviorSpark})'.format(
      type=type(self).__name__,
      behaviorSpark=repr(self._behaviorSpark))

Anki.Cozmo.ExternalInterface.SparkUnlocked = SparkUnlocked
del SparkUnlocked


class ActivateSparkedMusic(object):
  "Generated message-passing structure."

  __slots__ = (
    '_behaviorSpark',     # Anki.Cozmo.UnlockId
    '_musicSate',         # Anki.Cozmo.Audio.GameState.Music
    '_sparkedMusicState', # Anki.Cozmo.Audio.SwitchState.Sparked
  )

  @property
  def behaviorSpark(self):
    "Anki.Cozmo.UnlockId behaviorSpark struct property."
    return self._behaviorSpark

  @behaviorSpark.setter
  def behaviorSpark(self, value):
    self._behaviorSpark = msgbuffers.validate_integer(
      'ActivateSparkedMusic.behaviorSpark', value, -2147483648, 2147483647)

  @property
  def musicSate(self):
    "Anki.Cozmo.Audio.GameState.Music musicSate struct property."
    return self._musicSate

  @musicSate.setter
  def musicSate(self, value):
    self._musicSate = msgbuffers.validate_integer(
      'ActivateSparkedMusic.musicSate', value, 0, 4294967295)

  @property
  def sparkedMusicState(self):
    "Anki.Cozmo.Audio.SwitchState.Sparked sparkedMusicState struct property."
    return self._sparkedMusicState

  @sparkedMusicState.setter
  def sparkedMusicState(self, value):
    self._sparkedMusicState = msgbuffers.validate_integer(
      'ActivateSparkedMusic.sparkedMusicState', value, 0, 4294967295)

  def __init__(self, behaviorSpark=Anki.Cozmo.UnlockId.Invalid, musicSate=Anki.Cozmo.Audio.GameState.Music.Alarm_Clock, sparkedMusicState=Anki.Cozmo.Audio.SwitchState.Sparked.Fun):
    self.behaviorSpark = behaviorSpark
    self.musicSate = musicSate
    self.sparkedMusicState = sparkedMusicState

  @classmethod
  def unpack(cls, buffer):
    "Reads a new ActivateSparkedMusic from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('ActivateSparkedMusic.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new ActivateSparkedMusic from the given BinaryReader."
    _behaviorSpark = reader.read('i')
    _musicSate = reader.read('I')
    _sparkedMusicState = reader.read('I')
    return cls(_behaviorSpark, _musicSate, _sparkedMusicState)

  def pack(self):
    "Writes the current ActivateSparkedMusic, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current ActivateSparkedMusic to the given BinaryWriter."
    writer.write(self._behaviorSpark, 'i')
    writer.write(self._musicSate, 'I')
    writer.write(self._sparkedMusicState, 'I')

  def __eq__(self, other):
    if type(self) is type(other):
      return (self._behaviorSpark == other._behaviorSpark and
        self._musicSate == other._musicSate and
        self._sparkedMusicState == other._sparkedMusicState)
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._behaviorSpark, 'i') +
      msgbuffers.size(self._musicSate, 'I') +
      msgbuffers.size(self._sparkedMusicState, 'I'))

  def __str__(self):
    return '{type}(behaviorSpark={behaviorSpark}, musicSate={musicSate}, sparkedMusicState={sparkedMusicState})'.format(
      type=type(self).__name__,
      behaviorSpark=self._behaviorSpark,
      musicSate=self._musicSate,
      sparkedMusicState=self._sparkedMusicState)

  def __repr__(self):
    return '{type}(behaviorSpark={behaviorSpark}, musicSate={musicSate}, sparkedMusicState={sparkedMusicState})'.format(
      type=type(self).__name__,
      behaviorSpark=repr(self._behaviorSpark),
      musicSate=repr(self._musicSate),
      sparkedMusicState=repr(self._sparkedMusicState))

Anki.Cozmo.ExternalInterface.ActivateSparkedMusic = ActivateSparkedMusic
del ActivateSparkedMusic


class DeactivateSparkedMusic(object):
  "Generated message-passing structure."

  __slots__ = (
    '_behaviorSpark', # Anki.Cozmo.UnlockId
    '_musicSate',     # Anki.Cozmo.Audio.GameState.Music
  )

  @property
  def behaviorSpark(self):
    "Anki.Cozmo.UnlockId behaviorSpark struct property."
    return self._behaviorSpark

  @behaviorSpark.setter
  def behaviorSpark(self, value):
    self._behaviorSpark = msgbuffers.validate_integer(
      'DeactivateSparkedMusic.behaviorSpark', value, -2147483648, 2147483647)

  @property
  def musicSate(self):
    "Anki.Cozmo.Audio.GameState.Music musicSate struct property."
    return self._musicSate

  @musicSate.setter
  def musicSate(self, value):
    self._musicSate = msgbuffers.validate_integer(
      'DeactivateSparkedMusic.musicSate', value, 0, 4294967295)

  def __init__(self, behaviorSpark=Anki.Cozmo.UnlockId.Invalid, musicSate=Anki.Cozmo.Audio.GameState.Music.Alarm_Clock):
    self.behaviorSpark = behaviorSpark
    self.musicSate = musicSate

  @classmethod
  def unpack(cls, buffer):
    "Reads a new DeactivateSparkedMusic from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('DeactivateSparkedMusic.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new DeactivateSparkedMusic from the given BinaryReader."
    _behaviorSpark = reader.read('i')
    _musicSate = reader.read('I')
    return cls(_behaviorSpark, _musicSate)

  def pack(self):
    "Writes the current DeactivateSparkedMusic, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current DeactivateSparkedMusic to the given BinaryWriter."
    writer.write(self._behaviorSpark, 'i')
    writer.write(self._musicSate, 'I')

  def __eq__(self, other):
    if type(self) is type(other):
      return (self._behaviorSpark == other._behaviorSpark and
        self._musicSate == other._musicSate)
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    return (msgbuffers.size(self._behaviorSpark, 'i') +
      msgbuffers.size(self._musicSate, 'I'))

  def __str__(self):
    return '{type}(behaviorSpark={behaviorSpark}, musicSate={musicSate})'.format(
      type=type(self).__name__,
      behaviorSpark=self._behaviorSpark,
      musicSate=self._musicSate)

  def __repr__(self):
    return '{type}(behaviorSpark={behaviorSpark}, musicSate={musicSate})'.format(
      type=type(self).__name__,
      behaviorSpark=repr(self._behaviorSpark),
      musicSate=repr(self._musicSate))

Anki.Cozmo.ExternalInterface.DeactivateSparkedMusic = DeactivateSparkedMusic
del DeactivateSparkedMusic


class BehaviorManagerMessageUnion(object):
  "Generated message-passing union."

  __slots__ = ('_tag', '_data')

  class Tag(object):
    "The type indicator for this union."
    SetAvailableGames      = 0 # Anki.Cozmo.ExternalInterface.SetAvailableGames
    ActivateSpark          = 1 # Anki.Cozmo.ExternalInterface.ActivateSpark
    SparkUnlocked          = 2 # Anki.Cozmo.ExternalInterface.SparkUnlocked
    ActivateSparkedMusic   = 3 # Anki.Cozmo.ExternalInterface.ActivateSparkedMusic
    DeactivateSparkedMusic = 4 # Anki.Cozmo.ExternalInterface.DeactivateSparkedMusic

  @property
  def tag(self):
    "The current tag for this union."
    return self._tag

  @property
  def tag_name(self):
    "The name of the current tag for this union."
    if self._tag in self._tags_by_value:
      return self._tags_by_value[self._tag]
    else:
      return None

  @property
  def data(self):
    "The data held by this union. None if no data is set."
    return self._data

  @property
  def SetAvailableGames(self):
    "Anki.Cozmo.ExternalInterface.SetAvailableGames SetAvailableGames union property."
    msgbuffers.safety_check_tag('SetAvailableGames', self._tag, self.Tag.SetAvailableGames, self._tags_by_value)
    return self._data

  @SetAvailableGames.setter
  def SetAvailableGames(self, value):
    self._data = msgbuffers.validate_object(
      'BehaviorManagerMessageUnion.SetAvailableGames', value, Anki.Cozmo.ExternalInterface.SetAvailableGames)
    self._tag = self.Tag.SetAvailableGames

  @property
  def ActivateSpark(self):
    "Anki.Cozmo.ExternalInterface.ActivateSpark ActivateSpark union property."
    msgbuffers.safety_check_tag('ActivateSpark', self._tag, self.Tag.ActivateSpark, self._tags_by_value)
    return self._data

  @ActivateSpark.setter
  def ActivateSpark(self, value):
    self._data = msgbuffers.validate_object(
      'BehaviorManagerMessageUnion.ActivateSpark', value, Anki.Cozmo.ExternalInterface.ActivateSpark)
    self._tag = self.Tag.ActivateSpark

  @property
  def SparkUnlocked(self):
    "Anki.Cozmo.ExternalInterface.SparkUnlocked SparkUnlocked union property."
    msgbuffers.safety_check_tag('SparkUnlocked', self._tag, self.Tag.SparkUnlocked, self._tags_by_value)
    return self._data

  @SparkUnlocked.setter
  def SparkUnlocked(self, value):
    self._data = msgbuffers.validate_object(
      'BehaviorManagerMessageUnion.SparkUnlocked', value, Anki.Cozmo.ExternalInterface.SparkUnlocked)
    self._tag = self.Tag.SparkUnlocked

  @property
  def ActivateSparkedMusic(self):
    "Anki.Cozmo.ExternalInterface.ActivateSparkedMusic ActivateSparkedMusic union property."
    msgbuffers.safety_check_tag('ActivateSparkedMusic', self._tag, self.Tag.ActivateSparkedMusic, self._tags_by_value)
    return self._data

  @ActivateSparkedMusic.setter
  def ActivateSparkedMusic(self, value):
    self._data = msgbuffers.validate_object(
      'BehaviorManagerMessageUnion.ActivateSparkedMusic', value, Anki.Cozmo.ExternalInterface.ActivateSparkedMusic)
    self._tag = self.Tag.ActivateSparkedMusic

  @property
  def DeactivateSparkedMusic(self):
    "Anki.Cozmo.ExternalInterface.DeactivateSparkedMusic DeactivateSparkedMusic union property."
    msgbuffers.safety_check_tag('DeactivateSparkedMusic', self._tag, self.Tag.DeactivateSparkedMusic, self._tags_by_value)
    return self._data

  @DeactivateSparkedMusic.setter
  def DeactivateSparkedMusic(self, value):
    self._data = msgbuffers.validate_object(
      'BehaviorManagerMessageUnion.DeactivateSparkedMusic', value, Anki.Cozmo.ExternalInterface.DeactivateSparkedMusic)
    self._tag = self.Tag.DeactivateSparkedMusic

  def __init__(self, **kwargs):
    if not kwargs:
      self._tag = None
      self._data = None

    elif len(kwargs) == 1:
      key, value = next(iter(kwargs.items()))
      if key not in self._tags_by_name:
        raise TypeError("'{argument}' is an invalid keyword argument for this method.".format(argument=key))
      # calls the correct property
      setattr(self, key, value)

    else:
      raise TypeError('This method only accepts up to one keyword argument.')

  @classmethod
  def unpack(cls, buffer):
    "Reads a new BehaviorManagerMessageUnion from the given buffer."
    reader = msgbuffers.BinaryReader(buffer)
    value = cls.unpack_from(reader)
    if reader.tell() != len(reader):
      raise msgbuffers.ReadError(
        ('BehaviorManagerMessageUnion.unpack received a buffer of length {length}, ' +
        'but only {position} bytes were read.').format(
        length=len(reader), position=reader.tell()))
    return value

  @classmethod
  def unpack_from(cls, reader):
    "Reads a new BehaviorManagerMessageUnion from the given BinaryReader."
    tag = reader.read('B')
    if tag in cls._tags_by_value:
      value = cls()
      setattr(value, cls._tags_by_value[tag], cls._tag_unpack_methods[tag](reader))
      return value
    else:
      raise ValueError('BehaviorManagerMessageUnion attempted to unpack unknown tag {tag}.'.format(tag=tag))

  def pack(self):
    "Writes the current BehaviorManagerMessageUnion, returning bytes."
    writer = msgbuffers.BinaryWriter()
    self.pack_to(writer)
    return writer.dumps()

  def pack_to(self, writer):
    "Writes the current SampleUnion to the given BinaryWriter."
    if self._tag in self._tags_by_value:
      writer.write(self._tag, 'B')
      self._tag_pack_methods[self._tag](writer, self._data)
    else:
      raise ValueError('Cannot pack an empty BehaviorManagerMessageUnion.')

  def clear(self):
    self._tag = None
    self._data = None

  @classmethod
  def typeByTag(cls, tag):
    return cls._type_by_tag_value[tag]()

  def __eq__(self, other):
    if type(self) is type(other):
      return self._tag == other._tag and self._data == other._data
    else:
      return NotImplemented

  def __ne__(self, other):
    if type(self) is type(other):
      return not self.__eq__(other)
    else:
      return NotImplemented

  def __len__(self):
    if 0 <= self._tag < 5:
      return self._tag_size_methods[self._tag](self._data)
    else:
      return 1

  def __str__(self):
    if 0 <= self._tag < 5:
      return '{type}({name}={value})'.format(
        type=type(self).__name__,
        name=self.tag_name,
        value=self._data)
    else:
      return '{type}()'.format(
        type=type(self).__name__)

  def __repr__(self):
    if 0 <= self._tag < 5:
      return '{type}({name}={value})'.format(
        type=type(self).__name__,
        name=self.tag_name,
        value=repr(self._data))
    else:
      return '{type}()'.format(
        type=type(self).__name__)

  _tags_by_name = dict(
    SetAvailableGames=0,
    ActivateSpark=1,
    SparkUnlocked=2,
    ActivateSparkedMusic=3,
    DeactivateSparkedMusic=4,
  )

  _tags_by_value = dict()
  _tags_by_value[0] = 'SetAvailableGames'
  _tags_by_value[1] = 'ActivateSpark'
  _tags_by_value[2] = 'SparkUnlocked'
  _tags_by_value[3] = 'ActivateSparkedMusic'
  _tags_by_value[4] = 'DeactivateSparkedMusic'
  

  _tag_unpack_methods = dict()
  _tag_unpack_methods[0] = lambda reader: reader.read_object(Anki.Cozmo.ExternalInterface.SetAvailableGames.unpack_from)
  _tag_unpack_methods[1] = lambda reader: reader.read_object(Anki.Cozmo.ExternalInterface.ActivateSpark.unpack_from)
  _tag_unpack_methods[2] = lambda reader: reader.read_object(Anki.Cozmo.ExternalInterface.SparkUnlocked.unpack_from)
  _tag_unpack_methods[3] = lambda reader: reader.read_object(Anki.Cozmo.ExternalInterface.ActivateSparkedMusic.unpack_from)
  _tag_unpack_methods[4] = lambda reader: reader.read_object(Anki.Cozmo.ExternalInterface.DeactivateSparkedMusic.unpack_from)
  

  _tag_pack_methods = dict()
  _tag_pack_methods[0] = lambda writer, value: writer.write_object(value)
  _tag_pack_methods[1] = lambda writer, value: writer.write_object(value)
  _tag_pack_methods[2] = lambda writer, value: writer.write_object(value)
  _tag_pack_methods[3] = lambda writer, value: writer.write_object(value)
  _tag_pack_methods[4] = lambda writer, value: writer.write_object(value)
  

  _tag_size_methods = dict()
  _tag_size_methods[0] = lambda value: msgbuffers.size_object(value)
  _tag_size_methods[1] = lambda value: msgbuffers.size_object(value)
  _tag_size_methods[2] = lambda value: msgbuffers.size_object(value)
  _tag_size_methods[3] = lambda value: msgbuffers.size_object(value)
  _tag_size_methods[4] = lambda value: msgbuffers.size_object(value)
  

  _type_by_tag_value = dict()
  _type_by_tag_value[0] = lambda : Anki.Cozmo.ExternalInterface.SetAvailableGames
  _type_by_tag_value[1] = lambda : Anki.Cozmo.ExternalInterface.ActivateSpark
  _type_by_tag_value[2] = lambda : Anki.Cozmo.ExternalInterface.SparkUnlocked
  _type_by_tag_value[3] = lambda : Anki.Cozmo.ExternalInterface.ActivateSparkedMusic
  _type_by_tag_value[4] = lambda : Anki.Cozmo.ExternalInterface.DeactivateSparkedMusic
  

Anki.Cozmo.ExternalInterface.BehaviorManagerMessageUnion = BehaviorManagerMessageUnion
del BehaviorManagerMessageUnion


