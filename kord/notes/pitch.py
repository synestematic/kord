from bestia.iterate import LoopedList

from .intervals import Intervals

from ..errors import InvalidNote, InvalidAlteration, InvalidOctave

__all__ = [
    'NotePitch',
]


class NotePitch:

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
        # '♮': '',
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
    def EnharmonicMatrix(cls):
        ''' This is the heart of the whole project
            indeces are used to determine:
            * when to change octs
            * intervals between NotePitch instances
            notes MUST be unique so that TonalKey[d] finds 1 exact match!
        '''
        return LoopedList(
            ## 2-octave enharmonic relationships
            (  cls('C', '' , 2), cls('B', '#' , 1), cls('D', 'bb', 2)  ), # NAH
            (  cls('C', '#', 2), cls('D', 'b' , 2), cls('B', '##', 1)  ), # AAH

            ## 1-octave enharmonic relationships
            (  cls('D', '' , 1), cls('C', '##', 1), cls('E', 'bb', 1)  ), # NHH
            (  cls('D', '#', 1), cls('E', 'b' , 1), cls('F', 'bb', 1)  ), # AAH
            (  cls('E', '' , 1), cls('F', 'b' , 1), cls('D', '##', 1)  ), # NAH
            (  cls('F', '' , 1), cls('E', '#' , 1), cls('G', 'bb', 1)  ), # NAH
            (  cls('F', '#', 1), cls('G', 'b' , 1), cls('E', '##', 1)  ), # AAH
            (  cls('G', '' , 1), cls('F', '##', 1), cls('A', 'bb', 1)  ), # NHH
            (  cls('G', '#', 1), cls('A', 'b' , 1)                     ), # AA
            (  cls('A', '' , 1), cls('G', '##', 1), cls('B', 'bb', 1)  ), # NHH

            ## 2-octave enharmonic relationships
            (  cls('A', '#', 1), cls('B', 'b' , 1), cls('C', 'bb', 2)  ), # AAH
            (  cls('B', '' , 1), cls('C', 'b' , 2), cls('A', '##', 1)  ), # NAH
        )

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
    def input_alterations(cls) -> tuple:
        return tuple( cls._ALTS.keys() )

    @classmethod
    def output_alterations(cls) -> tuple:
        return tuple( cls._ALTS.values() )

    @classmethod
    def notes_by_alts(cls):
        ''' yields all 35 possible notes in following order:
            * 7 notes with alt ''
            * 7 notes with alt 'b'
            * 7 notes with alt '#'
            * 7 notes with alt 'bb'
            * 7 notes with alt '##'
        '''
        # sort alts
        alts = list( cls.input_alterations() )
        alts.sort(key=len) # '', b, #, bb, ##

        # get all notes
        notes = []
        for ehns in cls.EnharmonicMatrix():
            for ehn in ehns:
                notes.append(ehn)

        # yield notes
        for alt in alts:
            for note in notes:
                if note.alt == alt:
                    # note.oct = 3
                    yield note


    def __init__(self, char, *args):
        ''' init WITHOUT specifying argument names
            should be able to handle:
            NotePitch('C')
            NotePitch('C', 9)
            NotePitch('C', '#')
            NotePitch('C', '#', 9)
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
            oct_interval = (self.oct - other.oct) * Intervals.PERFECT_OCTAVE
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
            return other - self == Intervals.UNISON

    def __ne__(self, other):
        if other.__class__ == self.__class__:
            return other - self != Intervals.UNISON
        return True

    def __gt__(self, other):
        if self.__class__ == other.__class__:
            return self - other > Intervals.UNISON
        raise TypeError(' > not supported with {}'.format(other.__class__))

    def __ge__(self, other):
        if self.__class__ == other.__class__:
            return self - other >= Intervals.UNISON
        raise TypeError(' >= not supported with {}'.format(other.__class__))

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self - other < Intervals.UNISON
        raise TypeError(' < not supported with {}'.format(other.__class__))

    def __le__(self, other):
        if self.__class__ == other.__class__:
            return self - other <= Intervals.UNISON
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
        for row_index, row in enumerate( self.EnharmonicMatrix() ):
            for note_index, enharmonic_note in enumerate(row):
                if self ** enharmonic_note:  # ignore oct
                    return (row_index, note_index)

