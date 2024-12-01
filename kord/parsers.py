
from .notes import (
    MusicNote, DEFAULT_OCTAVE,
    input_alterations, output_alterations
)

from .errors import InvalidNote, InvalidAlteration, InvalidOctave

__all__ = [
    'MusicNoteParser',
    'MusicChordParser',
]


class MusicChordParser:

    def __init__(self, symbol):
        self.symbol = symbol
        self.reset()


    def reset(self):
        self.to_parse = self.symbol.strip()


    def _parse_root(self):
        possible_root = self.symbol[:3]
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


    def parse(self):
        root = self._parse_root()
        self.root = MusicNoteParser(root).parse()
        print(self.root)


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
            octave = DEFAULT_OCTAVE
        finally:
            return octave


    def _parse_alts(self):
        self.to_parse = self.to_parse.replace('𝄫', 'bb')
        self.to_parse = self.to_parse.replace('♭', 'b')
        self.to_parse = self.to_parse.replace('𝄪', '##')
        self.to_parse = self.to_parse.replace('♯', '#')

        if self.to_parse not in input_alterations():
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

