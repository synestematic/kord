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
        if self.is_exact_note(other):
            # C3 == C3
            return 1

        if not self.tone_is_enharmonic(other):
            # C3 == D3
            return False

        # enharmonic, but not equal
        oct_delta = abs(self.octave - other.octave)

        ### notes in separate octaves ###
        if oct_delta > 1:
            # E#3 == F5
            return False

        ### notes in adjacent octaves ###
        elif oct_delta == 1:
            if not self.bioctave_enharmony():
                # E#3 == F4
                return False

            if self.tone_index() in (8, 9):
                if self.tone != 'C' and other.tone != 'C':
                    # A#3 == Bb4 | A##3 == B4
                    return False

            elif self.tone_index() in (10, 11):
                if self.tone != 'B' and other.tone != 'B':
                    # C3 == Dbb4 | C#3 == Db4
                    return False

            # notes are in last 4 EHM rows
            if self.octave < other.octave:
                if input_alterations().index(self.alt) > input_alterations().index(other.alt):
                    # B3 == Cb4
                    return 2

            elif self.octave > other.octave:
                if input_alterations().index(self.alt) < input_alterations().index(other.alt):
                    # Cb4 == B3
                    return 3

            # B4 == Cb3
            return False

        ### notes in same octave ###
        elif not oct_delta:

            if self.bioctave_enharmony():
            
                if self.tone_index() in (8, 9):
                    if self.tone != 'C' and other.tone != 'C':
                        # A#3 == Bb3 | A##3 == B3
                        return True

                elif self.tone_index() in (10, 11):
                    if self.tone != 'B' and other.tone != 'B':
                        # C3 == Dbb3 | C#3 == Db3
                        return True

                # B3 == Cb3
                return False

            # E#3 == F3
            return 4

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
    (  Note('D',     ), Note('C', '##'), Note('E', 'bb')  ), # NHH
    (  Note('D', '#' ), Note('E', 'b' ), Note('F', 'bb')  ), # AAH
    (  Note('E',     ), Note('F', 'b' ), Note('D', '##')  ), # NAH
    (  Note('F',     ), Note('E', '#' ), Note('G', 'bb')  ), # NAH
    (  Note('F', '#' ), Note('G', 'b' ), Note('E', '##')  ), # AAH
    (  Note('G',     ), Note('F', '##'), Note('A', 'bb')  ), # NHH
    (  Note('G', '#' ), Note('A', 'b' ),                  ), # AA
    (  Note('A',     ), Note('G', '##'), Note('B', 'bb')  ), # NHH
    
    ## 2-octave enharmonic relationships
    (  Note('A', '#' ), Note('B', 'b' ), Note('C', 'bb')  ), # AAH
    (  Note('B',     ), Note('C', 'b' ), Note('A', '##')  ), # NAH
    (  Note('C',     ), Note('B', '#' ), Note('D', 'bb')  ), # NAH
    (  Note('C', '#' ), Note('D', 'b' ), Note('B', '##')  ), # AAH

)
