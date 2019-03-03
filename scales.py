from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

from notes import *

MAX_NOTES = 88

class Scale(object):

    def __init__(self, root_note):
        # ALWAYS INIT NEW NOTe
        self._degrees = [
            Note(root_note.tone, root_note.alt, 0)
        ]
        self.current_octave = 0
        self.reset_octave()

    def __repr__(self):
        spell_line = Row()
        for d in self.scale():
            spell_line.append(FString(d, size=5, colors=['yellow']))
        return str(spell_line)

    def interval(self, i):
        if i > len(self._intervals):
            next_i = i -len(self._intervals)
            v = self.interval(next_i)
            return v + OCTAVE

        v = self._intervals[i -1]
        return v

    def degree(self, d):
        return self._degrees[d -1]

    def scale(self, notes=0, start_note=None):
        if not notes:
            notes = len(self._intervals)

        if not start_note:
            start_note = self.degree(1)

        yield_enabled = False
        for d in range(1, MAX_NOTES):   # ignore 0
            if not notes:
                break
            degree = self.calc_degree(d)
            if degree == start_note:
                yield_enabled = True
            if yield_enabled:
                notes -= 1
                yield degree

        self.reset_octave()

    def reset_octave(self):
        self.current_octave = self._degrees[0].octave

class ChromaticScale(Scale):

    _intervals = [
        UNISON,
        MINOR_SECOND,
        MAJOR_SECOND,
        MINOR_THIRD,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        AUGMENTED_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH,
        MAJOR_SEVENTH,
        # OCTAVE,
    ]

    def calc_degree(self, d):
        if d == 1:
            return self.degree(1)

        row_index = self.degree(1).tone_index() + self.interval(d)

        next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == self.degree(1).alt[:-1]]
        if not next_degrees:
            chosen_alt = '#' if self.degree(1).alt == '' else self.degree(1).alt
            next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == chosen_alt]

        if len(next_degrees) == 1:
            # init new note, DO NOT change octave of ENHARMONIC_MATRIX note !
            degree = Note(next_degrees[0].tone, next_degrees[0].alt, next_degrees[0].octave)
            return self.calc_degree_octave(degree)
        # echo(next_degrees, 'red')
        # input()

    def calc_degree_octave(self, degree):
        if degree.tone == 'C' and degree.alt == '':
            self.current_octave += 1
            
        degree.octave = self.current_octave
        return degree


class DiatonicScale(Scale):

    def calc_degree(self, d):
        if d == 1:
            return self.degree(1)

        row_index = self.degree(1).tone_index() + self.interval(d)
        expected_tone = self.degree(1).next(d-1).tone

        next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.tone == expected_tone]

        if len(next_degrees) == 1:
            # init new note, DO NOT change octave of ENHARMONIC_MATRIX note ! maybe doing same mistake in String?
            degree = Note(next_degrees[0].tone, next_degrees[0].alt, next_degrees[0].octave)
            return self.calc_degree_octave(degree)
        # echo(next_degrees, 'red')
        # input()

    def calc_degree_octave(self, degree):
        ''' large interval scales that NEVER have C ?
            scales with Cb work good

            Cb0  Db0  Ebb0 Fb0  Gb0  Ab0  Bbb0 melodic minor...

        '''
        if degree.tone == 'C':
            self.current_octave += 1

        degree.octave = self.current_octave
        return degree

    # def _chord(self, root=1, count=3):
    #     while count > 0:
    #         for n, degree in enumerate(self.scale()):
    #             if n % 2 == 0:
    #                 count -= 1
    #                 input(count)
    #                 yield degree


    # def triad(self, root=1):
    #     return self._chord(root, count=3)

#####################################################

class MajorScale(DiatonicScale):

    _intervals = [
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
        # OCTAVE,
    ]

class IonianScale(MajorScale):
    pass

class MinorScale(DiatonicScale):

    _intervals = [
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
        # OCTAVE,
    ]

class AeolianScale(MinorScale):
    pass

class NaturalMinorScale(MinorScale):
    pass

class MelodicMinorScale(DiatonicScale):

    _intervals = [
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH,
        # OCTAVE,
    ]

class HarmonicMinorScale(DiatonicScale):

    _intervals = [
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SEVENTH,
        # OCTAVE,
    ]
