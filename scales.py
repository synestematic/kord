from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

from notes import *

class Scale(object):

    def __init__(self, key, alt=''):

        self.degree = []
        self.init_degrees()

        self.degree[1] = Note(key, alt)
        self.tonic = self.degree[1]

        self.calculate_degrees()

    def __repr__(self):
        spell_line = Row()
        for i in range(1, self._PITCHES +2):
            spell_line.append(FString(self.degree[i], size=4, colors=['yellow']))
        return str(spell_line)

    def init_degrees(self):
        for n in range(self._PITCHES +2): # used to be static at 12... why ?
            self.degree.append(None)

    def add_degree(self, d, notes):
        if len(notes) == 1:
            self.degree[d] = notes[0]
        else:
            echo('Failed to get degree[{}] of {} {}'.format(d, self.tonic, self.__class__.__name__), 'red')
            expected_tone = self.degree[d -1].next().tone # this assumes diatonic scale...
            self.degree[d] = Note(expected_tone, 'xx')

    def calculate_degrees(self):
        for d in range(2, self._PITCHES +2):
            self.calculate_degree(d)


class ChromaticScale(Scale):

    _PITCHES = 12

    interval = [
        None,
        UNISON,
        AUGMENTED_UNISON,

        MAJOR_SECOND,
        AUGMENTED_SECOND,

        MAJOR_THIRD,

        PERFECT_FOURTH,
        AUGMENTED_FOURTH,

        PERFECT_FIFTH,
        AUGMENTED_FIFTH,

        MAJOR_SIXTH,
        AUGMENTED_SIXTH,

        MAJOR_SEVENTH,
        OCTAVE,
    ]

    def calculate_degree(self, d):
        row_index = self.tonic.tone_index() +self.interval[d]

        next_degrees = [note for note in looped_list_item(row_index, NOTE_MATRIX) if note.alt == self.tonic.alt[:-1]]
        if not next_degrees:
            chosen_alt = '#' if self.tonic.alt == '' else self.tonic.alt
            next_degrees = [note for note in looped_list_item(row_index, NOTE_MATRIX) if note.alt == chosen_alt]
        
        self.add_degree(d, next_degrees)


class DiatonicScale(Scale):

    _PITCHES = 7

    def calculate_degree(self, d):
        row_index = self.tonic.tone_index() +self.interval[d]
        next_degrees = [note for note in looped_list_item(row_index, NOTE_MATRIX) if note.tone == self.degree[d -1].next().tone]
        self.add_degree(d, next_degrees)


class MajorScale(DiatonicScale):

    interval = [
        None,
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
        OCTAVE,
    ]

class IonianScale(MajorScale):
    pass

class MinorScale(DiatonicScale):

    interval = [
        None,
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
        OCTAVE,
    ]

class AeolianScale(MinorScale):
    pass

class NaturalMinorScale(MinorScale):
    pass

class MelodicMinorScale(DiatonicScale):

    interval = [
        None,
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH,
        OCTAVE,
    ]

class HarmonicMinorScale(DiatonicScale):

    interval = [
        None,
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SEVENTH,
        OCTAVE,
    ]
