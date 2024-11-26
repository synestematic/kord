
from .notes import *
from .notes import _CHARS

class MusicNoteParser:

    def __init__(self, symbol):
        self.symbol = symbol
        self.reset()

    def reset(self):
        self.to_parse = self.symbol.strip()

    def _parse_char(self):
        if len(self.to_parse) == 0 or self.to_parse[0] not in _CHARS:
            raise InvalidNote(self.symbol)
        char = self.to_parse[0]
        self.to_parse = self.to_parse[1:]
        return char

    def _parse_oct(self):
        # raise InvalidOctave
        # handle F12
        try:
            octave = int(self.to_parse[-1])
            self.to_parse = self.to_parse[:-1]
        except ValueError:
            octave = 3
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

