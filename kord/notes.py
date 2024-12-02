from bestia.iterate import LoopedList

from .errors import InvalidNote, InvalidAlteration, InvalidOctave

__all__ = [
    'UNISON',
    'DIMINISHED_SECOND',
    'MINOR_SECOND',
    'AUGMENTED_UNISON',
    'MAJOR_SECOND',
    'DIMINISHED_THIRD',
    'MINOR_THIRD',
    'AUGMENTED_SECOND',
    'DIMINISHED_FOURTH',
    'MAJOR_THIRD',
    'PERFECT_FOURTH',
    'AUGMENTED_THIRD',
    'AUGMENTED_FOURTH',
    'DIMINISHED_FIFTH',
    'PERFECT_FIFTH',
    'DIMINISHED_SIXTH',
    'MINOR_SIXTH',
    'AUGMENTED_FIFTH',
    'MAJOR_SIXTH',
    'DIMINISHED_SEVENTH',
    'MINOR_SEVENTH',
    'AUGMENTED_SIXTH',
    'MAJOR_SEVENTH',
    'DIMINISHED_OCTAVE',
    'OCTAVE',
    'AUGMENTED_SEVENTH',

    'MusicNote',
    'notes_by_alts',
]

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


class MusicNote:

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

    _ALTS = {
        'bb': '𝄫',
        'b': '♭',
        '': '',
        '#': '♯',
        '##': '𝄪',
    }

    _OCTAVES = (
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

    DEFAULT_OCTAVE = 3
    MAXIMUM_OCTAVE = 9

    @classmethod
    def possible_chars(cls):
        return [ c for c in cls._CHARS if c ]

    @classmethod
    def validate_char(cls, char):
        char = char.upper()
        if char not in cls.possible_chars():
            raise InvalidNote(char)
        return char

    @classmethod
    def input_alterations(cls):
        return list( cls._ALTS.keys() )

    def __init__(self, char, *args):
        ''' init WITHOUT specifying argument names
            should be able to handle:
            MusicNote('C')
            MusicNote('C', 9)
            MusicNote('C', '#')
            MusicNote('C', '#', 9)
        '''
        self.chr = self.validate_char(char)
        self.alt = ''
        self.oct = self.DEFAULT_OCTAVE

        if len(args) > 2:
            raise InvalidNote('Too many arguments')

        # with only 1 arg, decide if it's alt or oct
        if len(args) == 1:
            if args[0] in self._ALTS:
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
            if args[0] not in self._ALTS:
                raise InvalidAlteration(args[0])
            self.alt = args[0]

            try:
                self.oct = int(args[1])
            except:
                raise InvalidOctave(args[1])

        if self.oct > self.MAXIMUM_OCTAVE:
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
            output += self._OCTAVES[int(c)]
        return output

    @property
    def repr_alt(self):
        return self._ALTS[self.alt]

    def __sub__(self, other):
        if self.__class__ == other.__class__:
            oct_interval = (self.oct - other.oct) * OCTAVE
            chr_interval = self._CHARS.index(self.chr) - self._CHARS.index(other.chr)
            alt_interval = (
                self.input_alterations().index(self.alt) - self.input_alterations().index(other.alt)
            )
            return oct_interval + chr_interval + alt_interval
        raise TypeError(' - not supported with {}'.format(other.__class__))

    def __pow__(self, other):
        if self.__class__ == other.__class__:
            if self.chr == other.chr:
                if self.alt == other.alt:
                    return True
            return False
        raise TypeError(' ** not supported with {}'.format(other.__class__))

    def __rshift__(self, other):
        if self.__class__ == other.__class__:
            if self.chr == other.chr:
                if self.alt == other.alt:
                    if self.oct == other.oct:
                        return True
            return False
        raise TypeError(' >> not supported with {}'.format(other.__class__))

    def __eq__(self, other):
        if other.__class__ == self.__class__:
            return other - self == UNISON

    def __ne__(self, other):
        if other.__class__ == self.__class__:
            return other - self != UNISON
        return True

    def __gt__(self, other):
        if self.__class__ == other.__class__:
            return self - other > UNISON
        raise TypeError(' > not supported with {}'.format(other.__class__))

    def __ge__(self, other):
        if self.__class__ == other.__class__:
            return self - other >= UNISON
        raise TypeError(' >= not supported with {}'.format(other.__class__))

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self - other < UNISON
        raise TypeError(' < not supported with {}'.format(other.__class__))

    def __le__(self, other):
        if self.__class__ == other.__class__:
            return self - other <= UNISON
        raise TypeError(' <= not supported with {}'.format(other.__class__))


    ### CHR METHODS
    def relative_chr(self, n):
        my_index = self._CHARS.index(self.chr)
        return self._CHARS[my_index +n]

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
        ''' evaluates whether I need to cross octave border in order to go from self to other
            ignores octave
        '''
        if self.chr != other.chr:
            return self._CHARS.index(self.chr) > self._CHARS.index(other.chr)
        return (
            self.input_alterations().index(self.alt) > self.input_alterations().index(other.alt)
        )


    # ENHARMONIC ATTRIBUTES
    @property
    def enharmonic_row(self):
        return self.matrix_coordinates[0]

    @property
    def matrix_coordinates(self):
        for row_index, row in enumerate(_EnharmonicMatrix):
            for note_index, enharmonic_note in enumerate(row):
                if self ** enharmonic_note:  # ignore oct
                    return (row_index, note_index)


### This is the heart of the whole project
### indeces are used to determine:
###   * when to change octs
###   * intervals between MusicNote instances
### notes MUST be unique so that MusicKey[d] finds 1 exact match!
_EnharmonicMatrix = LoopedList(

    ## 2-octave enharmonic relationships
    (  MusicNote('C', '' , 2), MusicNote('B', '#' , 1), MusicNote('D', 'bb', 2)  ), # NAH
    (  MusicNote('C', '#', 2), MusicNote('D', 'b' , 2), MusicNote('B', '##', 1)  ), # AAH

    ## 1-octave enharmonic relationships
    (  MusicNote('D', '' , 1), MusicNote('C', '##', 1), MusicNote('E', 'bb', 1)  ), # NHH
    (  MusicNote('D', '#', 1), MusicNote('E', 'b' , 1), MusicNote('F', 'bb', 1)  ), # AAH
    (  MusicNote('E', '' , 1), MusicNote('F', 'b' , 1), MusicNote('D', '##', 1)  ), # NAH
    (  MusicNote('F', '' , 1), MusicNote('E', '#' , 1), MusicNote('G', 'bb', 1)  ), # NAH
    (  MusicNote('F', '#', 1), MusicNote('G', 'b' , 1), MusicNote('E', '##', 1)  ), # AAH
    (  MusicNote('G', '' , 1), MusicNote('F', '##', 1), MusicNote('A', 'bb', 1)  ), # NHH
    (  MusicNote('G', '#', 1), MusicNote('A', 'b' , 1)                      ),      # AA
    (  MusicNote('A', '' , 1), MusicNote('G', '##', 1), MusicNote('B', 'bb', 1)  ), # NHH

    ## 2-octave enharmonic relationships
    (  MusicNote('A', '#', 1), MusicNote('B', 'b' , 1), MusicNote('C', 'bb', 2)  ), # AAH
    (  MusicNote('B', '' , 1), MusicNote('C', 'b' , 2), MusicNote('A', '##', 1)  ), # NAH

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
    alts = MusicNote.input_alterations()
    alts.sort(key=len) # '', b, #, bb, ##

    # get all notes
    notes = []
    for ehns in _EnharmonicMatrix:
        for ehn in ehns:
            notes.append(ehn)

    # yield notes
    for alt in alts:
        for note in notes:
            if note.alt == alt:
                # note.oct = 3
                yield note
