from bestia.iterate import LoopedList
from bestia.output import echo

from kord.errors import *

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


_NOTE_CHARS = LoopedList(
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
    # '₀',
    # '₁',
    # '₂',
    # '₃',
    # '₄',
    # '₅',
    # '₆',
    # '₇',
    # '₈',
    # '₉',
    '⁰',
    '¹',
    '²',
    '³',
    '⁴',
    '⁵',
    '⁶',
    '⁷',
    '⁸',
    '⁹',
)

_ALTS = {
    'bb': '𝄫',
    'b': '♭',
    # 'b': 'ᵇ',
    '': '',
    # '#': '⌗',
    # '#': '⋕',
    '#': '♯',
    '##': '𝄪',
}

def input_alterations():
    return list(_ALTS.keys())

def output_alterations():
    return list(_ALTS.values())

class Note(object):

    def __init__(self, *args):
        self.chr = args[0].upper()
        if self.chr not in _NOTE_CHARS:
            raise InvalidNote(args[0])

        self.alt = ''
        for a in args[1:]:
            if a in input_alterations():
                self.alt = a
        if self.alt not in input_alterations():
            raise InvalidAlteration(self.alt)

        self.oct = 3
        for a in args[1:]:
            if type(a) == int:
                self.oct = a
            raise InvalidOctave(self.oct)


    def __iter__(self):
        ''' allows unpacking Note objects as args for other functions '''
        for i in (self.chr, self.alt, self.oct):
            yield i


    def __repr__(self):
        return '{}{}{}'.format(
            self.chr,
            self.repr_alt,
            self.repr_oct,
        )

    @property
    def repr_oct(self):
        output = ''
        for c in str(self.oct):
            output += _OCTS[int(c)]
        return output

    @property
    def repr_alt(self):
        return _ALTS[self.alt]

    def __add__(self, other):
        ''' this is kinda useless but keeping it just for compliance '''
        return other.__interval_from(self)

    def __sub__(self, other):
        return self.__interval_from(other)

    def __eq__(self, other):
        return self.__interval_from(other) == 0

    def __gt__(self, other):
        return self.__interval_from(other) > 0

    def __ge__(self, other):
        return self.__interval_from(other) >= 0

    def is_note(self, other, ignore_oct=False):
        if self.__class__ == type(other):
            if self.chr == other.chr:
                if self.alt == other.alt:
                    if ignore_oct:
                        return True
                    return self.oct == other.oct

    def is_a(self, chr, alt='', oct=None):
        if self.chr == chr:
            if self.alt == alt:
                return True if oct is None else self.oct == oct


    ### CHR METHODS
    def relative_chr(self, n):
        my_index = _NOTE_CHARS.index(self.chr)
        return _NOTE_CHARS[my_index +n]

    def adjacent_chr(self, n=1):
        ''' returns next adjacent chr of self
            negative fails...
        '''
        c = ''
        count = 0
        i = 1

        while count != n:
            c = self.relative_chr(i)
            if c:
                count += 1
            i += 1

        return c

    ### OCT METHODS
    def oversteps_oct(self, other):
        ''' does NOT take oct attr into account '''
        if self.chr != other.chr:
            return _NOTE_CHARS.index(self.chr) > _NOTE_CHARS.index(other.chr)
        return input_alterations().index(self.alt) > input_alterations().index(other.alt)


    def __interval_from(self, other):
        ''' used ONLY to implement comparison operators, do NOT call directly... '''
        oct_interval = (self.oct - other.oct) * OCTAVE
        chr_interval = _NOTE_CHARS.index(self.chr) - _NOTE_CHARS.index(other.chr)
        alt_interval = input_alterations().index(self.alt) - input_alterations().index(other.alt)
        return oct_interval + chr_interval + alt_interval


    # ENHARMONIC ATTRIBUTES
    @property
    def enharmonic_row(self):
        return self.matrix_coordinates[0]

    @property
    def matrix_coordinates(self):
        for _row_index, _row in enumerate(EnharmonicMatrix):
            for _note_index, _enharmonic_note in enumerate(_row):
                if self.chr == _enharmonic_note.chr and self.alt == _enharmonic_note.alt:
                    return (_row_index, _note_index)




### This is the heart of the whole project
### indeces are used to determine:
###   * when to change octs
###   * intervals between Note instances
### notes MUST be unique so that Note.degree() finds 1 exact match!
EnharmonicMatrix = LoopedList(

    ## 2-octave enharmonic relationships
    (  Note('C', '' , 2), Note('B', '#' , 1), Note('D', 'bb', 2)  ), # NAH
    (  Note('C', '#', 2), Note('D', 'b' , 2), Note('B', '##', 1)  ), # AAH

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

)

def notes_by_alts(alts=[]):
    ''' yields all 35 possible notes in following order:
        * 7 notes with alt ''
        * 7 notes with alt 'b'
        * 7 notes with alt '#'
        * 7 notes with alt 'bb'
        * 7 notes with alt '##'
    '''
    notes = []
    for ehns in EnharmonicMatrix:
        for ehn in ehns:
            notes.append(ehn)

    for n in notes:
        if not n.alt:
            yield n

    for n in notes:
        if n.alt == 'b':
            yield n

    for n in notes:
        if n.alt == '#':
            yield n

    for n in notes:
        if n.alt == 'bb':
            yield n

    for n in notes:
        if n.alt == '##':
            yield n
