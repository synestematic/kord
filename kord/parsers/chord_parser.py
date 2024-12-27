
from .pitch_parser import NotePitchParser

from ..notes import NotePitch
from ..keys.chords import *

from ..errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

from bestia.output import echo

__all__ = [
    'ChordParser',
]


class ChordParser:
    ''' chord symbols still left to add:

        Fadd4

        Am11

        G13
        B7b9
    '''

    RECOGNIZED_CHORDS = (
        PowerChord, Suspended4Chord, Suspended2Chord,
        MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
        MajorSixthChord, MinorSixthChord,
        MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
        HalfDiminishedSeventhChord, DiminishedSeventhChord,
        MajorAdd9Chord, MinorAdd9Chord, AugmentedAdd9Chord, DiminishedAdd9Chord,
        DominantNinthChord, DominantMinorNinthChord,
        MajorNinthChord, MinorNinthChord,
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
        ''' - sure   chord is correct?  return TonalKey()
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

