from bestia.iterate import LoopedList

from .errors import *

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


_CHARS = LoopedList(
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

MAX_OCT = 9


_ALTS = {
    'bb': '𝄫',
    'b': '♭',
    '': '',
    '#': '♯',
    '##': '𝄪',
}

def input_alterations():
    return list(_ALTS.keys())

def output_alterations():
    return list(_ALTS.values())


class Note(object):

    def __init__(self, char, *args):
        ''' init WITHOUT specifying argument names
            should be able to handle:
            Note('C')
            Note('C', 3)
            Note('C', '#')
            Note('C', '#', 3)
        '''
        self.chr = char.upper()
        if self.chr not in _CHARS:
            raise InvalidNote(char)

        self.alt = ''
        self.oct = 3

        if len(args) >  2:
            raise InvalidNote('Too many arguments')

        # with only 1 arg, decide if it's alt or oct
        if len(args) == 1:
            if args[0] in input_alterations():
                self.alt = args[0]
            else:
                try:
                    self.oct = int(args[0])
                except:
                    raise InvalidNote(
                        'Failed to parse argument: '.format(args[0])
                    )

        # with 2 args, order must be alt, oct
        if len(args) == 2:
            if args[0] not in input_alterations():
                raise InvalidAlteration(args[0])
            self.alt = args[0]

            try:
                self.oct = int(args[1])
            except:
                raise InvalidOctave(args[1])

        if self.oct > MAX_OCT:
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

    def __sub__(self, other):
        if self.__class__ == other.__class__:
            oct_interval = (self.oct - other.oct) * OCTAVE
            chr_interval = _CHARS.index(self.chr) - _CHARS.index(other.chr)
            alt_interval = input_alterations().index(self.alt) - input_alterations().index(other.alt)
            return oct_interval + chr_interval + alt_interval
        raise TypeError(f' - not supported with {other.__class__}')

    def __pow__(self, other):
        if self.__class__ == other.__class__:
            if self.chr == other.chr:
                if self.alt == other.alt:
                    return True
            return False
        raise TypeError(f' ** not supported with {other.__class__}')

    def __rshift__(self, other):
        if self.__class__ == other.__class__:
            if self.chr == other.chr:
                if self.alt == other.alt:
                    if self.oct == other.oct:
                        return True
            return False
        raise TypeError(f' >> not supported with {other.__class__}')


    def __eq__(self, other):  # ==
        if other.__class__ == self.__class__:
            return other - self == UNISON

    def __ne__(self, other):  # !=
        if other.__class__ == self.__class__:
            return other - self != UNISON
        return True

    def __gt__(self, other):  # >
        if self.__class__ == other.__class__:
            return self - other > UNISON
        raise TypeError(f' > not supported with {other.__class__}')

    def __ge__(self, other):  # >=
        if self.__class__ == other.__class__:
            return self - other >= UNISON
        raise TypeError(f' >= not supported with {other.__class__}')

    def __lt__(self, other):  # <
        if self.__class__ == other.__class__:
            return self - other < UNISON
        raise TypeError(f' < not supported with {other.__class__}')

    def __le__(self, other):  # <=
        if self.__class__ == other.__class__:
            return self - other <= UNISON
        raise TypeError(f' <= not supported with {other.__class__}')


    ### CHR METHODS
    def relative_chr(self, n):
        my_index = _CHARS.index(self.chr)
        return _CHARS[my_index +n]

    def adjacent_chr(self, n=1):
        ''' returns next adjacent chr of self
            negative fails...
        '''
        c = ''
        i = 1
        while n != 0:
            c = self.relative_chr(i)
            if c:
                n -= 1
            i += 1
        return c

    ### OCT METHODS
    def oversteps_oct(self, other):
        ''' evaluates whether I need to cross octave border in rder to go from self to other
            ignores octave
        '''
        if self.chr != other.chr:
            return _CHARS.index(self.chr) > _CHARS.index(other.chr)
        return input_alterations().index(self.alt) > input_alterations().index(other.alt)


    # ENHARMONIC ATTRIBUTES
    @property
    def enharmonic_row(self):
        return self.matrix_coordinates[0]

    @property
    def matrix_coordinates(self):
        for row_index, row in enumerate(EnharmonicMatrix):
            for note_index, enharmonic_note in enumerate(row):
                if self ** enharmonic_note:  # ignore oct
                    return (row_index, note_index)


### This is the heart of the whole project
### indeces are used to determine:
###   * when to change octs
###   * intervals between Note instances
### notes MUST be unique so that MusicKey[d] finds 1 exact match!
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

def notes_by_alts():
    ''' yields all 35 possible notes in following order:
        * 7 notes with alt ''
        * 7 notes with alt 'b'
        * 7 notes with alt '#'
        * 7 notes with alt 'bb'
        * 7 notes with alt '##'
    '''
    # sort alts
    alts = input_alterations()
    alts.sort(key=len) # '', b, #, bb, ##

    # get all notes
    notes = []
    for ehns in EnharmonicMatrix:
        for ehn in ehns:
            notes.append(ehn)

    # yield notes
    for alt in alts:
        for note in notes:
            if note.alt == alt:
                # note.oct = 3
                yield note
