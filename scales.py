from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

from notes import *

class Scale(object):

    def __init__(self, root_note):
        # ACCEPT ONLY SINGLE ALT NOTES?
        # Major F##, C## work - G## dies...
        self.current_oct = 0

        self.current_note = Note(
            # ALWAYS init new note
            root_note.tone, 
            root_note.alt, 
            self.current_oct
        )

        self._degrees = [
            self.current_note
        ]

    def __repr__(self):
        spell_line = Row()
        for d in self.scale():
            if not d:
                continue
            spell_line.append(FString(d, size=5, fg='yellow'))
        return str(spell_line)

    def interval(self, i):
        ''' returns delta semitones from scale root note '''
        if i > len(self._intervals):
            next_i = i -len(self._intervals)
            return self.interval(next_i) + OCTAVE
        return self._intervals[i -1]

    def degree(self, d):
        return self._degrees[d -1]

    def scale(self, notes=0, start_note=None):

        if not notes:
            notes = len(self._intervals)

        if not start_note:
            start_note = self.degree(1)

        yield_enabled = False
        d = 1 # ignore 0
        while True:

            if not notes:
                self.reset_oct()
                return

            last_note_delta = self.interval(d) -self.interval(d -1)
            if last_note_delta > SEMITONE:
                for st in range(last_note_delta -1):
                    yield None

            degree = self.calc_degree(d)
            if degree >= start_note:
                yield_enabled = True
            if yield_enabled:
                notes -= 1
                yield degree

            d += 1

    def reset_oct(self):
        self.current_oct = 0
        self.current_note = self.degree(1)


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
    ]

    def calc_degree(self, d):
        if d == 1:
            return self.degree(1)

        row_index = self.degree(1).enharmonic_row() + self.interval(d)

        next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.is_note(self.degree(1), ignore_oct=True)]
        if not next_degrees:
            next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == self.degree(1).alt[:-1]]
            if not next_degrees:
                chosen_alt = '#' if self.degree(1).alt == '' else self.degree(1).alt
                next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == chosen_alt]

        if len(next_degrees) == 1:
            deg = next_degrees[0]
            if deg.tone == 'C' and deg.alt == '':
                self.current_oct += 1

            # init new note, DO NOT change octave of ENHARMONIC_MATRIX note!
            self.current_note = Note(deg.tone, deg.alt, self.current_oct)
            return self.current_note

        echo(next_degrees, 'red')
        input()


class DiatonicScale(Scale):

    def calc_degree(self, d):
        if d == 1:
            return self.degree(1)

        row_index = self.degree(1).enharmonic_row() + self.interval(d)
        expected_tone = self.degree(1).next_tone(d -1)

        next_degrees = [note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.tone == expected_tone]

        if len(next_degrees) == 1:
            deg = next_degrees[0]
            if deg.tone == 'C': # large intervals that do not hace C will need to compare last and next
                self.current_oct += 1

            # init new note, DO NOT change octave of ENHARMONIC_MATRIX note!
            self.current_note = Note(deg.tone, deg.alt, self.current_oct)
            return self.current_note

        echo(next_degrees, 'red')
        input()


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
        MAJOR_SEVENTH,
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
    ]
