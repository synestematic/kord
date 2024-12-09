
from .notes import MusicNote
from .keys.chords import *

from .errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

from bestia.output import echo

__all__ = [
    'NotePitchParser',
    'ChordParser',
]


class ChordParser:
    ''' chord symbols still left to implement:

        Fadd4
        Cadd9

        Am11

        G13
        B7b9
    '''

    RECOGNIZED_CHORDS = (
        PowerChord,
        MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
        MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
        HalfDiminishedSeventhChord, DiminishedSeventhChord,
        DominantNinthChord, DominantMinorNinthChord,
        MajorNinthChord, MinorNinthChord,
        MajorSixthChord, MinorSixthChord,
        SuspendedFourChord, SuspendedTwoChord,
    )

    BASS_NOTE_SEP = '/'

    def __init__(self, symbol):
        self.symbol = symbol.strip()
        self.reset()


    def reset(self):
        self.root = None
        self.flavor = None
        self.to_parse = self.symbol.replace(' ', '')  # 'B aug7'


    @property
    def is_inverted(self) -> bool:
        return self.BASS_NOTE_SEP in self.symbol

    @property
    def bass(self):
        if not self.is_inverted:
            return self.root
        return NotePitchParser(
            self.symbol.split(self.BASS_NOTE_SEP)[-1]
        ).parse()


    def _parse_root(self):
        ''' this should NOT validate anything!
            only guess how many of the symbol's first 3 chars make up the root
            return value will be validated using NotePitchParser::parse()
        '''
        possible_root = self.to_parse[:3]
        if len(possible_root) in (0, 1,):
            # symbol='', possible_root=''
            # symbol='D', possible_root='D'
            return possible_root

        if possible_root[1:] in ('bb', '##', '♯♯', '♭♭'):
            # symbol='Dbbmin7', possible_root='Dbb'
            return possible_root[:3]

        if possible_root[1] in ('b', '#', '♯', '♭', '𝄫', '𝄪'):
            # symbol='Dbmin7', possible_root='Db'
            return possible_root[:2]

        # symbol='Dmin7', possible_root='D'
        return possible_root[:1]


    def _parse_flavor(self):
        # shouldnt  this go in a _parse_alt() function
        if 'sharp' in self.to_parse.lower() or 'flat' in self.to_parse.lower():
            raise InvalidAlteration(self.symbol)

        for chord_class in self.RECOGNIZED_CHORDS:
            if self.to_parse in chord_class.notations:
                return chord_class
        return None


    def parse(self):
        ''' - sure   chord is correct?  return MusicKey()
            - unsure chord is correct?  return None
            - sure   chord is wrong  ?  raise  InvalidChord()
        '''
        try:
            # parse root out of first 3 chars
            root = self._parse_root()
            self.root = NotePitchParser(root).parse()
            # print(self.root)

            # ignore Chord/Bass notes on inverted chords
            if self.is_inverted:
                self.to_parse = self.to_parse.split(self.BASS_NOTE_SEP)[0]

            # parse flavor out of remaining to parse
            self.to_parse = self.to_parse[len(root):]
            self.flavor = self._parse_flavor()

        except Exception:
            # echo(self.symbol, 'red')
            raise InvalidChord(self.symbol)

        # c = 'cyan'
        # if not self.symbol or not self.flavor:
        #     c = 'red'
        # echo(
        #     f'{self.symbol} = {self.root} {self.flavor} {self.bass}',
        #     c,
        # )
        if self.flavor and self.root:
            # init instance of Chord class using Chord root
            return self.flavor(*self.root)
        return None


class NotePitchParser:

    def __init__(self, symbol):
        self.symbol = symbol
        self.reset()


    def reset(self):
        self.to_parse = self.symbol.strip()


    def _parse_char(self):
        char = MusicNote.validate_char(self.to_parse[0])
        self.to_parse = self.to_parse[1:]
        return char


    def _parse_oct(self):
        if len(self.to_parse) > 1:
            try:
                # this being an int means octave > MAXIMUM_OCTAVE
                octave = int(self.to_parse[-2])
                octave_over_max = True
            except ValueError:
                # probably an alt
                octave_over_max = False
            finally:
                if octave_over_max:
                    raise InvalidOctave(self.symbol)

        try:
            # this being an int means this is an octave
            octave = int(self.to_parse[-1])
            self.to_parse = self.to_parse[:-1]
        except ValueError:
            # probably an alt
            octave = MusicNote.DEFAULT_OCTAVE
        finally:
            return octave


    def _parse_alts(self):
        self.to_parse = self.to_parse.replace('𝄫', 'bb')
        self.to_parse = self.to_parse.replace('♭', 'b')
        self.to_parse = self.to_parse.replace('𝄪', '##')
        self.to_parse = self.to_parse.replace('♯', '#')

        if self.to_parse not in MusicNote.input_alterations():
            raise InvalidAlteration(self.symbol)

        alts = self.to_parse
        self.to_parse = self.to_parse[len(self.to_parse):]
        return alts


    def parse(self):
        if len(self.to_parse) == 0:
            raise InvalidNote(self.symbol)

        char = self._parse_char()
        if len(self.to_parse) == 0:
            self.reset()
            return MusicNote(char)

        octave = self._parse_oct()
        if len(self.to_parse) == 0:
            self.reset()
            return MusicNote(char, octave)

        alts = self._parse_alts()
        if len(self.to_parse) == 0:
            self.reset()
            return MusicNote(char, alts, octave)

        raise InvalidNote(self.symbol)

