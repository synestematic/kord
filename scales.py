from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

from notes import *

class Scale(object):

    def __init__(self, key, alt=''):

        self.degrees = []

        self.init_degrees()
        self.degrees[0] = Note(key, alt)
        self.tonic = self.degrees[0]

        self.calculate_degrees()

    def __repr__(self):
        spell_line = Row()
        for i in range(self._PITCHES):
            spell_line.append(FString(self.degrees[i], size=4, colors=['yellow']))
        return str(spell_line)

    ### INIT FUNCTIONS

    def init_degrees(self):
        for n in range(self._PITCHES):
            self.degrees.append(None)

    def add_degree(self, d, notes):
        if len(notes) == 1:
            self.degrees[d] = notes[0]
        else:
            echo('Failed to get degree[{}] of {} {}'.format(d, self.tonic, self.__class__.__name__), 'red')
            expected_tone = self.degrees[d -1].next().tone # this assumes diatonic scale...
            self.degrees[d] = Note(expected_tone, 'xx')

    def calculate_degrees(self):
        for d in range(1, self._PITCHES): # first degree added at init
            self.calculate_degree(d)

    ### SPELL FUNCTIONS

    def degree(self, d):
        return looped_list_item(d -1, self.degrees)

    def scale(self, notes=None):
        for d in range(notes if notes else self._PITCHES):
            yield looped_list_item(d, self.degrees)

class ChromaticScale(Scale):

    _PITCHES = 12

    interval = [
        UNISON,
        # AUGMENTED_UNISON,
        MINOR_SECOND,
        MAJOR_SECOND,
        # AUGMENTED_SECOND,
        MINOR_THIRD,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        AUGMENTED_FOURTH,
        PERFECT_FIFTH,
        # AUGMENTED_FIFTH,
        MINOR_SIXTH,
        MAJOR_SIXTH,
        # AUGMENTED_SIXTH,
        MINOR_SEVENTH,
        MAJOR_SEVENTH,
        OCTAVE,
    ]

    def calculate_degree(self, d):
        row_index = self.tonic.tone_index() +self.interval[d]

        next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == self.tonic.alt[:-1]]
        if not next_degrees:
            chosen_alt = '#' if self.tonic.alt == '' else self.tonic.alt
            next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == chosen_alt]
        
        self.add_degree(d, next_degrees)


class DiatonicScale(Scale):

    _PITCHES = 7

    def calculate_degree(self, d):
        row_index = self.tonic.tone_index() +self.interval[d]
        next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.tone == self.degrees[d -1].next().tone]
        self.add_degree(d, next_degrees)

    def _chord(self, root=1, count=3):
        n = root
        for c in range(count):
            yield self.degree(n)
            n += 2

    def triad(self, root=1):
        return self._chord(root, count=3)

    def seventh(self, root=1):
        return self._chord(root, count=4)

    def ninth(self, root=1):
        return self._chord(root, count=5)

    def eleventh(self, root=1):
        return self._chord(root, count=6)

    def thirteenth(self, root=1):
        return self._chord(root, count=7)


class MajorScale(DiatonicScale):

    interval = [
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
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SEVENTH,
        OCTAVE,
    ]
