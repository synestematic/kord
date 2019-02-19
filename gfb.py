from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

_SHARP = 1
_FLAT = -1

_TONE = 2
_SEMITONE = 1

_UNISON = 0
_DIMINISHED_SECOND = 0

_MINOR_SECOND = 1
_AUGMENTED_UNISON = 1

_MAJOR_SECOND = 2
_DIMINISHED_THIRD = 2

_MINOR_THIRD = 3
_AUGMENTED_SECOND = 3

_DIMINISHED_FOURTH = 4
_MAJOR_THIRD = 4

_PERFECT_FOURTH = 5
_AUGMENTED_THIRD = 5

_AUGMENTED_FOURTH = 6
_DIMINISHED_FIFTH = 6

_PERFECT_FIFTH = 7
_DIMINISHED_SIXTH = 7

_MINOR_SIXTH = 8
_AUGMENTED_FIFTH = 8

_MAJOR_SIXTH = 9
_DIMINISHED_SEVENTH = 9

_MINOR_SEVENTH = 10
_AUGMENTED_SIXTH = 10

_MAJOR_SEVENTH = 11
_DIMINISHED_OCTAVE = 11

_OCTAVE = 12
_AUGMENTED_SEVENTH = 12


class Note(object):

    _ORDER = ('C', 'D', 'E', 'F', 'G', 'A', 'B')

    def __init__(self, tone=' ', alt=' ', octave=' '):
        self.tone = tone.upper()
        self.alt = alt.lower()
        self.octave = octave

    def matrix_coordinates(self):
        for t_i, _columns in enumerate(_NOTE_MATRIX):
            for a_i, _rows in enumerate(_columns):
                if self.tone == _rows.tone and self.alt == _rows.alt:
                    return (t_i, a_i)

    def tone_index(self):
        return self.matrix_coordinates()[0]

    def alt_index(self):
        return self.matrix_coordinates()[1]

    def next(self):
        my_index = self._ORDER.index(self.tone)
        note_string = looped_list_item(my_index +1, self._ORDER)
        return Note(note_string)

    def __repr__(self):
        return '{}{}'.format(self.tone, self.alt)

_NOTE_MATRIX = [
    [ Note('B', '#' ), Note('C', ''  ), Note('D', 'bb') ],
    [ Note('B', '##'), Note('C', '#' ), Note('D', 'b' ) ],
    [ Note('C', '##'), Note('D', ''  ), Note('E', 'bb') ],
    [ Note('F', 'bb'), Note('D', '#' ), Note('E', 'b' ) ],
    [ Note('D', '##'), Note('E', ''  ), Note('F', 'b' ) ],
    [ Note('G', 'bb'), Note('F', ''  ), Note('E', '#' ) ],
    [ Note('E', '##'), Note('F', '#' ), Note('G', 'b' ) ],
    [ Note('F', '##'), Note('G', ''  ), Note('A', 'bb') ],
    [ Note('?', '??'), Note('G', '#' ), Note('A', 'b' ) ],
    [ Note('G', '##'), Note('A', ''  ), Note('B', 'bb') ],
    [ Note('C', 'bb'), Note('A', '#' ), Note('B', 'b' ) ],
    [ Note('A', '##'), Note('B', ''  ), Note('C', 'b' ) ],
]


class Fret(object):

    def __init__(self, note='', fret=12):
        self.fret = fret
        self.note = Note() if not note else note

    def __repr__(self):
        f = '||' if self.fret == 0 else '|'
        fret = FString(
            '{}{}{} {}'.format(self.note.tone, self.note.alt, self.note.octave, f),
            size=6, align='r', colors=['red']
        )
        return str(fret)


class String(object):

    fret = []

    def __init__(self, open_note='Abb3'):

        self.init_frets()

        tone = open_note[0]
        alt = open_note[1:-1]
        octave = int(open_note[-1])

        open_note = Note(tone, alt, octave)
        self.fret[0] = Fret(open_note, fret=0)

    def init_frets(self):
        for n in range(12):
            self.fret.append(Fret())


    def __repr__(self):
        string_line = Row()
        for i in range(12):
            string_line.append(self.fret[i])
        return str(string_line)


class Tuning(object):

    def __init__(self, *arg, **kwargs):
        for k, v in kwargs.items():
            if k.startswith('string'):
                setattr(self, k, String(v))


class Scale(object):

    def __init__(self, key='C', alt=''):

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
        _UNISON,
        _AUGMENTED_UNISON,

        _MAJOR_SECOND,
        _AUGMENTED_SECOND,

        _MAJOR_THIRD,

        _PERFECT_FOURTH,
        _AUGMENTED_FOURTH,

        _PERFECT_FIFTH,
        _AUGMENTED_FIFTH,

        _MAJOR_SIXTH,
        _AUGMENTED_SIXTH,

        _MAJOR_SEVENTH,
        _OCTAVE,
    ]

    def calculate_degree(self, d):
        row_index = self.tonic.tone_index() +self.interval[d]

        next_degrees = [note for note in looped_list_item(row_index, _NOTE_MATRIX) if note.alt == self.tonic.alt[:-1]]
        if not next_degrees:
            chosen_alt = '#' if self.tonic.alt == '' else self.tonic.alt
            next_degrees = [note for note in looped_list_item(row_index, _NOTE_MATRIX) if note.alt == chosen_alt]
        
        self.add_degree(d, next_degrees)


class DiatonicScale(Scale):

    _PITCHES = 7

    def calculate_degree(self, d):
        row_index = self.tonic.tone_index() +self.interval[d]
        next_degrees = [note for note in looped_list_item(row_index, _NOTE_MATRIX) if note.tone == self.degree[d -1].next().tone]
        self.add_degree(d, next_degrees)


class MajorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MAJOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MAJOR_SIXTH,
        _MAJOR_SEVENTH,
        _OCTAVE,
    ]

class IonianScale(MajorScale):
    pass

class MinorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MINOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MINOR_SIXTH,
        _MINOR_SEVENTH,
        _OCTAVE,
    ]

class AeolianScale(MinorScale):
    pass

class NaturalMinorScale(MinorScale):
    pass

class MelodicMinorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MINOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MAJOR_SIXTH,
        _MINOR_SEVENTH,
        _OCTAVE,
    ]

class HarmonicMinorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MINOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MINOR_SIXTH,
        _MAJOR_SEVENTH,
        _OCTAVE,
    ]

def unit_test(s):
    for _row in _NOTE_MATRIX:
        for _column in _row:
            if len(_column.alt) >1 or '?' in _column.alt:
                continue
            echo(_column, 'blue')
            echo(s(_column.tone, _column.alt), 'cyan')

if __name__ == '__main__':

    try:
        # b_minor = NaturalMinorScale('B')
        # print(b_minor)

        # a_minor = MelodicMinorScale('A')
        # print(a_minor)

        # d_minor = HarmonicMinorScale('D')
        # print(d_minor)

        std_tuning = Tuning(
            string1='E4',
            string2='B3',
            string3='G3',
            string4='D3',
            string5='A2',
            string6='E2'
        )
        # echo(std_tuning.string5)

        empty_fret = Fret(fret=6)
        string1 = Row(
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            width=72
        ).echo()

        Bb3 = Note('B', 'b', 3)
        # new_fret = Fret(Bb3, fret=12)
        # print(new_fret)

        unit_test(ChromaticScale)
        unit_test(MajorScale)
        unit_test(NaturalMinorScale)
        unit_test(MelodicMinorScale)
        unit_test(HarmonicMinorScale)

    except KeyboardInterrupt:
        echo()


# JUST FINISHED BASIC CHROMATIC SCALE DEFINITION TO OUTPUT ALL FRETS OF STRING
