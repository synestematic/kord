
from .notes import MusicNote
from .keys.chords import (
    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    HalfDiminishedSeventhChord, DiminishedSeventhChord,
)

from .errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

from bestia.output import echo

__all__ = [
    'MusicNoteParser',
    'MusicChordParser',
]


CHORD_FLAVORS = {
    '': MajorTriad,
    'maj': MajorTriad,
    'major': MajorTriad,

    '-': MinorTriad,
    'min': MinorTriad,
    'minor': MinorTriad,

    'aug': AugmentedTriad,
    'augmented': AugmentedTriad,

    'dim': DiminishedTriad,
    'diminished': DiminishedTriad,

    # 'M7': MajorSeventhChord,
    'Δ7': MajorSeventhChord,
    'maj7': MajorSeventhChord,
    'major7': MajorSeventhChord,


    # 'm7': MinorSeventhChord,
    '-7': MinorSeventhChord,
    'min7': MinorSeventhChord,
    'minor7': MinorSeventhChord,

    '7': DominantSeventhChord,
    'dom7': DominantSeventhChord,
    'dominant7': DominantSeventhChord,

    'dim7': DiminishedSeventhChord,
    'diminished7': DiminishedSeventhChord,
    'o7': DiminishedSeventhChord,


    'min7dim5': HalfDiminishedSeventhChord,
    'm7b5': HalfDiminishedSeventhChord,
    'm7(b5)': HalfDiminishedSeventhChord,
    'ø7': HalfDiminishedSeventhChord,

}

class MusicChordParser:

    def __init__(self, symbol):
        self.symbol = symbol.strip()
        self.reset()


    def reset(self):
        self.root = None
        self.flavor = None
        self.to_parse = self.symbol.strip()


    def is_inverted(self) -> bool:
        return '/' in self.symbol


    def bass_note(self):
        if self.is_inverted():
            bass_note = MusicNoteParser(
                self.symbol.split('/')[-1]
            ).parse()
            return bass_note
        return self.root


    def _parse_root(self):
        ''' decides how many of the symbol's first 3 chars make up the chord root
        '''
        possible_root = self.to_parse[:3]
        if len(possible_root) == 0:
            raise InvalidNote(possible_root)

        MusicNote.validate_char(possible_root[0])
        if len(possible_root) == 1:
            return possible_root[:1]

        # if len(possible_root) == 3:
        if possible_root[1:] in ('bb', '##', '♯♯', '♭♭'):
            return possible_root[:3]

        # if len(possible_root) == 2:
        if possible_root[1] in ('b', '#', '♯', '♭', '𝄫', '𝄪'):
            return possible_root[:2]

        return possible_root[:1]


    def _parse_flavor(self):
        possible_flavor = CHORD_FLAVORS.get(self.to_parse)
        return possible_flavor

    def parse(self):
        try:
            root = self._parse_root()
            self.root = MusicNoteParser(root).parse()
            self.to_parse = self.to_parse[len(root):]
            self.flavor = self._parse_flavor()

        except Exception:
            raise InvalidChord(self.symbol)

        finally:
            echo(f'{self.symbol} = {self.root} {self.flavor}', 'cyan')
            if self.flavor and self.root:
                # init instance of Chord class using Chord root
                return self.flavor(*self.root)

class MusicNoteParser:

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

