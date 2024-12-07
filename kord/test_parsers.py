import unittest

from .parsers import MusicNoteParser, MusicChordParser

from .notes import MusicNote

from .errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

__all__ = [
    'MusicNoteParserTest',
    'MusicChordParserTest',
]


class MusicChordParserTest(unittest.TestCase):

    CASES = (
        'A',
        'Emaj',

        'F7',
        # 'Am7',


        'fdim',
        'Bbdim',

        'Fmaj9',
        'Gm9',

        'Bbmaj7/C',

        # 'C13b9'


        'A#sus9',
    )

    FAILS = (
        'H',
        # 'A♯♭𝄫𝄪add13',
        # 'C♯♭𝄫𝄪add13',
    )

    def testWins(self):
        for symbol in self.CASES:
            parser = MusicChordParser(symbol)
            parsed_note = parser.parse()
            # self.assertEqual(parsed_note, expected)


    def testFails(self):
        for symbol in self.FAILS:
            parser = MusicChordParser(symbol)
            self.assertRaises(InvalidChord, parser.parse), symbol


class MusicNoteParserTest(unittest.TestCase):

    CHAR_WINS = [
        ['C', MusicNote('C')],
        ['D', MusicNote('D')],
        ['E', MusicNote('E')],
        ['F', MusicNote('F')],
        ['G', MusicNote('G')],
        ['A', MusicNote('A')],
        ['B', MusicNote('B')],

        ['c', MusicNote('C')],
        ['d', MusicNote('D')],
        ['e', MusicNote('E')],
        ['f', MusicNote('F')],
        ['g', MusicNote('G')],
        ['a', MusicNote('A')],
        ['b', MusicNote('B')],
    ]

    CHAR_FAILS = [
        'H', 'T', 'Y', 'h',
    ]

    OCTAVE_WINS = [
        [ f'C{octave}', MusicNote('C', octave) ] for octave
        in range(0, MusicNote.MAXIMUM_OCTAVE)
    ]

    OCTAVE_FAILS = [
        f'A{octave}' for octave
        in range(MusicNote.MAXIMUM_OCTAVE+1, MusicNote.MAXIMUM_OCTAVE+500)
    ]

    ALTS_WINS = [
        ['D#', MusicNote('D', '#')],
        ['D♯', MusicNote('D', '#')],

        ['C##', MusicNote('C', '##')],
        ['C♯♯', MusicNote('C', '##')],
        ['C#♯', MusicNote('C', '##')],
        ['C♯#', MusicNote('C', '##')],
        ['C𝄪', MusicNote('C', '##')],

        ['Eb', MusicNote('E', 'b')],
        ['E♭', MusicNote('E', 'b')],

        ['Gbb', MusicNote('G', 'bb')],
        ['G♭♭', MusicNote('G', 'bb')],
        ['Gb♭', MusicNote('G', 'bb')],
        ['G♭b', MusicNote('G', 'bb')],
        ['G𝄫', MusicNote('G', 'bb')],
    ]

    ALTS_FAILS = [
        'Abbb',
        'A###',
        'Bbr6',
        'Ce#',

        'D𝄫b',
        'D𝄫♭',

        'G𝄪#',
        'G𝄪♯',
    ]

    def setUp(self):
        print()

    def testChars(self):
        for symbol, expected in self.CHAR_WINS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testCharFails(self):
        for symbol in self.CHAR_FAILS:
            parser = MusicNoteParser(symbol)
            self.assertRaises(InvalidNote, parser.parse)

    def testOctaves(self):
        for symbol, expected in self.OCTAVE_WINS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testOctaveFails(self):
        for symbol in self.OCTAVE_FAILS:
            parser = MusicNoteParser(symbol)
            self.assertRaises(InvalidOctave, parser.parse)

    def testAlterations(self):
        for symbol, expected in self.ALTS_WINS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testAlterationFails(self):
        for symbol in self.ALTS_FAILS:
            parser = MusicNoteParser(symbol)
            self.assertRaises(InvalidAlteration, parser.parse)
