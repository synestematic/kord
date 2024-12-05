
from .notes import MusicNote
from .keys.chords import *

from .errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

from bestia.output import echo

__all__ = [
    'MusicNoteParser',
    'MusicChordParser',
]


class MusicChordParser:

    RECOGNIZED_CHORDS = (
        MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
        MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
        HalfDiminishedSeventhChord, DiminishedSeventhChord,
        MajorNinthChord, MinorNinthChord, DominantNinthChord,
    )

    BASS_NOTE_SEP = '/'

    def __init__(self, symbol):
        self.symbol = symbol.strip()
        self.reset()


    def reset(self):
        self.root = None
        self.flavor = None
        self.to_parse = self.symbol.strip()


    @property
    def is_inverted(self) -> bool:
        return self.BASS_NOTE_SEP in self.symbol

    @property
    def bass_note(self):
        if self.is_inverted:
            bass_note = MusicNoteParser(
                self.symbol.split(self.BASS_NOTE_SEP)[-1]
            ).parse()
            return bass_note
        return self.root


    def _parse_root(self):
        ''' decides how many of the symbol's first 3 chars make up the root
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
        for chord_class in self.RECOGNIZED_CHORDS:
            if self.to_parse in chord_class.notations:
                return chord_class
        return None


    def parse(self):
        try:
            # parse root out of first 3 chars
            root = self._parse_root()
            self.root = MusicNoteParser(root).parse()

            # ignore Chord/Bass notes on inverted chords
            if self.is_inverted:
                self.to_parse = self.to_parse.split(self.BASS_NOTE_SEP)[0]

            # parse flavor out of remaining to parse
            self.to_parse = self.to_parse[len(root):]
            self.flavor = self._parse_flavor()

        except Exception:
            raise InvalidChord(self.symbol)

        finally:
            echo(
                f'{self.symbol} = {self.root} {self.flavor} {self.bass_note}',
                'cyan',
            )
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

