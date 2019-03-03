from bestia.iterate import looped_list_item
from bestia.output import echo

SHARP = 1
FLAT = -1

TONE = 2
SEMITONE = 1

UNISON = 0
DIMINISHED_SECOND = 0

MINOR_SECOND = 1
AUGMENTED_UNISON = 1

MAJOR_SECOND = 2
DIMINISHED_THIRD = 2

MINOR_THIRD = 3
AUGMENTED_SECOND = 3

DIMINISHED_FOURTH = 4
MAJOR_THIRD = 4

PERFECT_FOURTH = 5
AUGMENTED_THIRD = 5

AUGMENTED_FOURTH = 6
DIMINISHED_FIFTH = 6

PERFECT_FIFTH = 7
DIMINISHED_SIXTH = 7

MINOR_SIXTH = 8
AUGMENTED_FIFTH = 8

MAJOR_SIXTH = 9
DIMINISHED_SEVENTH = 9

MINOR_SEVENTH = 10
AUGMENTED_SIXTH = 10

MAJOR_SEVENTH = 11
DIMINISHED_OCTAVE = 11

OCTAVE = 12
AUGMENTED_SEVENTH = 12

NOTE_ORDER = ('C', 'D', 'E', 'F', 'G', 'A', 'B')

class Note(object):

    _SHARPS = [
        '#',
        '♯',
        '⌗',
        '⋕',
        'ₓ',
        '𝄪',
    ]

    _FLATS = [
        'ᵇ',
        '♭'
    ]

    _ALTERATIONS = ('', '#', 'b', '##', 'bb')

    _REPR_ALTS = {'' : '', '#' : '♯', '##' : '𝄪', 'b' : '♭', 'bb' : '♭♭'}
    _REPR_OCTS = ('⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹')

    def __init__(self, *args):
        self.tone = args[0].upper()

        self.alt = ''
        for a in args:
            if a in self._ALTERATIONS:
                self.alt = a

        self.octave = 3
        for a in args:
            if type(a) == int:
                self.octave = a

    def repr_octave(self):
        return self._REPR_OCTS[self.octave]

    def repr_alt(self):
        return self._REPR_ALTS[self.alt]

    def __repr__(self):
        return '{}{}{}'.format(self.tone, self.repr_alt(), self.repr_octave())

    def __eq__(self, other):
        if type(other) != self.__class__:
            return False
        if self.tone != other.tone:
            return False
        if self.alt != other.alt:
            return False
        if self.octave != other.octave:
            return False
        return True

    ### MATRIX METHODS
    def matrix_coordinates(self):
        for _row_index, _row in enumerate(ENHARMONIC_MATRIX):
            for _note_index, _enharmonic_note in enumerate(_row):
                if self.tone == _enharmonic_note.tone and self.alt == _enharmonic_note.alt:
                    return (_row_index, _note_index)

    def tone_index(self):
        return self.matrix_coordinates()[0]

    def alt_index(self):
        return self.matrix_coordinates()[1]

    ### NOTE_ORDER METHODS
    def _relative_note(self, n):
        my_index = NOTE_ORDER.index(self.tone)
        note_string = looped_list_item(my_index +n, NOTE_ORDER)
        return Note(note_string)

    def next(self, n=1):
        return self._relative_note(n)

    def previous(self, n=1):
        n = 0 - abs(n)
        return self._relative_note(n)

ENHARMONIC_MATRIX = (
    (  Note('B', '#' ), Note('C', ''  ), Note('D', 'bb')  ),
    (  Note('B', '##'), Note('C', '#' ), Note('D', 'b' )  ),
    (  Note('C', '##'), Note('D', ''  ), Note('E', 'bb')  ),
    (  Note('F', 'bb'), Note('D', '#' ), Note('E', 'b' )  ),
    (  Note('D', '##'), Note('E', ''  ), Note('F', 'b' )  ),
    (  Note('G', 'bb'), Note('F', ''  ), Note('E', '#' )  ),
    (  Note('E', '##'), Note('F', '#' ), Note('G', 'b' )  ),
    (  Note('F', '##'), Note('G', ''  ), Note('A', 'bb')  ),
    (  Note('G', '#' ), Note('A', 'b' ),                  ),
    (  Note('G', '##'), Note('A', ''  ), Note('B', 'bb')  ),
    (  Note('C', 'bb'), Note('A', '#' ), Note('B', 'b' )  ),
    (  Note('A', '##'), Note('B', ''  ), Note('C', 'b' )  ),
)
