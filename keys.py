from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

from notes import *

class Key(object):

    # def __init__(self, key, alt='', octave=0):
    def __init__(self, key, alt=''):
        self._degrees = [
            Note(key, alt, 0)
        ]

    def __repr__(self):
        spell_line = Row()
        for d in self.scale():
            spell_line.append(FString(d, size=4, colors=['yellow']))
        return str(spell_line)

    def interval(self, i):
        return self._intervals[i -1]

    def degree(self, d):
        return self._degrees[d -1]

    def scale(self, notes=0):
        # current_octave = self._degrees[0].octave
        for d in range(1, notes +1 if notes else len(self._intervals)):
            yield self.calc_degree(d)


class ChromaticKey(Key):

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
        OCTAVE,
    ]

    def calc_degree(self, d):
        if d == 1:
            return self.degree(1)

        row_index = self.degree(1).tone_index() +self.interval(d)

        next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == self.degree(1).alt[:-1]]
        if not next_degrees:
            chosen_alt = '#' if self.degree(1).alt == '' else self.degree(1).alt
            next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == chosen_alt]

        if len(next_degrees) == 1:
            return next_degrees[0]

        echo(next_degrees, 'red')
        input()


class DiatonicKey(Key):

    _intervals = [
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
        OCTAVE,
    ]

    def calc_degree(self, d):
        if d == 1:
            return self.degree(1)

        row_index = self.degree(1).tone_index() + self.interval(d)
        expected_tone = self.degree(1).next(d-1).tone

        next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.tone == expected_tone]

        if len(next_degrees) == 1:
            return next_degrees[0]

