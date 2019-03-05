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

_TONES = (
    'C', 
    None,
    'D', 
    None,
    'E', 
    'F', 
    None,
    'G', 
    None,
    'A', 
    None,
    'B',
)

_OCTS = ('⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹')
_ALTS = {
    'bb': 'ᵇᵇ',
    # 'b': 'ᵇ', 
    'b': '♭', 
    '': '', 
    '#': '♯', 
    # '#': '⌗', 
    # '#': '⋕', 
    '##': '𝄪', 
}

def input_alterations():
    return list(_ALTS.keys())

def output_alterations():
    return list(_ALTS.values())

class Note(object):

    def __init__(self, *args):
        self.tone = args[0].upper()
        assert  self.tone in _TONES

        self.alt = ''
        for a in args[1:]:
            if a in input_alterations():
                self.alt = a

        self.octave = 3
        for a in args[1:]:
            if type(a) == int:
                self.octave = a

    def repr_oct(self, verbose=1):
        output = ''
        if verbose:
            for char in str(self.octave):
                output += _OCTS[int(char)]
        return output

    def repr_alt(self):
        return _ALTS[self.alt]

    def __repr__(self):
        return '{}{}{}'.format(self.tone, self.repr_alt(), self.repr_oct())


    def __eq__(self, other):
        # if self.is_exact_note(other):
        #     # C1 == C1
        #     return True
        if not self.tone_is_enharmonic(other):
            return False    # C1 == D1

        oct_delta = abs(self.octave - other.octave)

        ### notes in same octave ###
        if not oct_delta:

            if not self.bioctave_enharmony():
                return 1        # E#1 == F1
            
            if self.tone_index() in (8, 9):
                if self.tone != 'C' and other.tone != 'C':
                    return 2    # A#1 == Bb1 | A##1 == B1

            elif self.tone_index() in (10, 11):
                if self.tone != 'B' and other.tone != 'B':
                    return 3    # C1 == Dbb1 | C#1 == Db1

            return False        # B1 == Cb1

        ### notes in adjacent octaves ###
        elif oct_delta == 1:

            if not self.bioctave_enharmony():
                return False        # E#1 == F2

            if self.tone_index() in (8, 9):
                if self.tone != 'C' and other.tone != 'C':
                    return False    # A#1 == Bb2 | A##1 == B2

            elif self.tone_index() in (10, 11):
                if self.tone != 'B' and other.tone != 'B':
                    return False    # C1 == Dbb2 | C#1 == Db2

            if self.octave < other.octave:
                if input_alterations().index(self.alt) > input_alterations().index(other.alt):
                    return 4        # B1 == Cb2

            elif self.octave > other.octave:
                if input_alterations().index(self.alt) < input_alterations().index(other.alt):
                    return 5        # Cb2 == B1

            return False   # B2 == Cb1

        ### notes in separate octaves ###
        elif oct_delta > 1:
            return False   # E#1 == F3


    def bioctave_enharmony(self):
        return self.tone_index() > 7

    def tone_is_enharmonic(self, other):
        return self.tone_index() == other.tone_index()

    def is_exact_note(self, other):
        if self.__class__ == type(other):
            if self.octave == other.octave:
                if self.tone == other.tone:
                    if self.alt == other.alt:
                        return True
        return False

    ### HIERARCHY METHODS
    def _relative_tone(self, n):
        my_index = _TONES.index(self.tone)
        return looped_list_item(my_index +n, _TONES)

    def next_tone(self, n=1):
        tone = None
        tone_count = 0
        iteration = 1

        while True:
            if tone_count == n:
                return tone

            tone = self._relative_tone(iteration)
            if tone:
                tone_count += 1

            iteration += 1

    ### ENHARMONIC METHODS
    def _matrix_coordinates(self):
        for _row_index, _row in enumerate(ENHARMONIC_MATRIX):
            for _note_index, _enharmonic_note in enumerate(_row):
                if self.tone == _enharmonic_note.tone and self.alt == _enharmonic_note.alt:
                    return (_row_index, _note_index)

    def tone_index(self):
        return self._matrix_coordinates()[0]

    def alt_index(self):
        return self._matrix_coordinates()[1]

ENHARMONIC_MATRIX = (
    ## 1-octave enharmonic relationships
    (  Note('D', '' , 1), Note('C', '##', 1), Note('E', 'bb', 1)  ), # NHH
    (  Note('D', '#', 1), Note('E', 'b' , 1), Note('F', 'bb', 1)  ), # AAH
    (  Note('E', '' , 1), Note('F', 'b' , 1), Note('D', '##', 1)  ), # NAH
    (  Note('F', '' , 1), Note('E', '#' , 1), Note('G', 'bb', 1)  ), # NAH
    (  Note('F', '#', 1), Note('G', 'b' , 1), Note('E', '##', 1)  ), # AAH
    (  Note('G', '' , 1), Note('F', '##', 1), Note('A', 'bb', 1)  ), # NHH
    (  Note('G', '#', 1), Note('A', 'b' , 1), Note('G', '#' , 1)  ), # AAa
    (  Note('A', '' , 1), Note('G', '##', 1), Note('B', 'bb', 1)  ), # NHH
    ## 2-octave enharmonic relationships
    (  Note('A', '#', 1), Note('B', 'b' , 1), Note('C', 'bb', 2)  ), # AAH
    (  Note('B', '' , 1), Note('C', 'b' , 2), Note('A', '##', 1)  ), # NAH
    (  Note('C', '' , 2), Note('B', '#' , 1), Note('D', 'bb', 2)  ), # NAH
    (  Note('C', '#', 2), Note('D', 'b' , 2), Note('B', '##', 1)  ), # AAH
)
