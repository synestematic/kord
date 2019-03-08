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

_OCTS = (
    '₀',
    '₁',
    '₂',
    '₃',
    '₄',
    '₅',
    '₆',
    '₇',
    '₈',
    '₉',
)

# _OCTS = (
#     '⁰',
#     '¹',
#     '²',
#     '³',
#     '⁴',
#     '⁵',
#     '⁶',
#     '⁷',
#     '⁸',
#     '⁹'
# )

_ALTS = {
    'bb': 'ᵇᵇ',
    'b': 'ᵇ',
    # 'b': '♭',
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

    ### INIT METHODS
    def __init__(self, *args):
        self.tone = args[0].upper()
        assert self.tone in _TONES

        self.alt = ''
        for a in args[1:]:
            if a in input_alterations():
                self.alt = a
        # assert self.alt in input_alterations()

        self.oct = 3
        for a in args[1:]:
            if type(a) == int:
                self.oct = a

    ### REPR METHODS
    def __repr__(self):
        return '{}{}{}'.format(self.tone, self.repr_alt(), self.repr_oct())

    def repr_oct(self, verbose=True):
        output = ''
        if verbose:
            for char in str(self.oct):
                output += _OCTS[int(char)]
        return output

    def repr_alt(self):
        return _ALTS[self.alt]

    ### COMPARE METHODS
    def is_note(self, other, ignore_oct=False):
        if self.__class__ == type(other):
            if self.tone == other.tone:
                if self.alt == other.alt:
                    return True if ignore_oct else self.oct == other.oct
    
    def __eq__(self, other):
        return self.delta_semitones(other) == 0

    def __gt__(self, other):
        return self.delta_semitones(other) > 0

    def __ge__(self, other):
        return self.delta_semitones(other) >= 0

    ### TONE METHODS
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

    def delta_semitones(self, other):
        # 0  :  self == other
        # >1 :  self >  other
        # <1 :  self  < other
        oct_delta = self.oct - other.oct
        tone_delta = self.tone_delta(other)
        alt_delta  = self.alt_delta(other)
        tone_alt_delta = tone_delta + alt_delta
        return tone_alt_delta + oct_delta * OCTAVE

    def tone_delta(self, other):
        return _TONES.index(self.tone) - _TONES.index(other.tone)

    def alt_delta(self, other):
        return input_alterations().index(self.alt) - input_alterations().index(other.alt)

    ### ENHARMONIC METHODS
    def _matrix_coordinates(self):
        for _row_index, _row in enumerate(ENHARMONIC_MATRIX):
            for _note_index, _enharmonic_note in enumerate(_row):
                if self.tone == _enharmonic_note.tone and self.alt == _enharmonic_note.alt:
                    return (_row_index, _note_index)

    def enharmonic_row(self):
        return self._matrix_coordinates()[0]

    def has_adjacent_oct_enharmony(self):
        ''' only  Cbb, Cb, B#, B##  return True
            these notes lay on adjacent octaves
            relative to their 2 enharmonic notes
        '''
        if self.enharmonic_row() < 8:
            return False
        if self.enharmonic_row() in (8, 9) and self.tone != 'C':
            return False
        if self.enharmonic_row() in (10, 11) and self.tone != 'B':
            return False
        return True

ENHARMONIC_MATRIX = (
    ## 1-octave enharmonic relationships
    (  Note('D', '' , 1), Note('C', '##', 1), Note('E', 'bb', 1)  ), # NHH
    (  Note('D', '#', 1), Note('E', 'b' , 1), Note('F', 'bb', 1)  ), # AAH
    (  Note('E', '' , 1), Note('F', 'b' , 1), Note('D', '##', 1)  ), # NAH
    (  Note('F', '' , 1), Note('E', '#' , 1), Note('G', 'bb', 1)  ), # NAH
    (  Note('F', '#', 1), Note('G', 'b' , 1), Note('E', '##', 1)  ), # AAH
    (  Note('G', '' , 1), Note('F', '##', 1), Note('A', 'bb', 1)  ), # NHH
    (  Note('G', '#', 1), Note('A', 'b' , 1)                      ), # AA
    (  Note('A', '' , 1), Note('G', '##', 1), Note('B', 'bb', 1)  ), # NHH
    ## 2-octave enharmonic relationships
    (  Note('A', '#', 1), Note('B', 'b' , 1), Note('C', 'bb', 2)  ), # AAH
    (  Note('B', '' , 1), Note('C', 'b' , 2), Note('A', '##', 1)  ), # NAH
    (  Note('C', '' , 2), Note('B', '#' , 1), Note('D', 'bb', 2)  ), # NAH
    (  Note('C', '#', 2), Note('D', 'b' , 2), Note('B', '##', 1)  ), # AAH
)

# notes need to be unique so that calc_degrees finds 1 exact match!