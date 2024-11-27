import unittest

from .parsers import MusicNoteParser

from .notes import MusicNote, MAXIMUM_OCTAVE

from .errors import InvalidAlteration, InvalidOctave

class MusicNoteParserTest(unittest.TestCase):

    CHAR_TESTS = (
        ['C', MusicNote('C')],
        ['D', MusicNote('D')],
        ['E', MusicNote('E')],
        ['F', MusicNote('F')],
        ['G', MusicNote('G')],
        ['A', MusicNote('A')],
        ['B', MusicNote('B')],
    )

    OCTAVE_TESTS = (
        ['A0', MusicNote('A', 0)],
        ['A1', MusicNote('A', 1)],
        ['A2', MusicNote('A', 2)],
        ['A3', MusicNote('A', 3)],
        ['A4', MusicNote('A', 4)],
        ['A5', MusicNote('A', 5)],
        ['A6', MusicNote('A', 6)],
        ['A7', MusicNote('A', 7)],
        ['A8', MusicNote('A', 8)],
        ['A9', MusicNote('A', MAXIMUM_OCTAVE)],
    )

    ALTS_TESTS = (
        ['D#', MusicNote('D', '#')],
        ['D♯', MusicNote('D', '#')],

        ['C##', MusicNote('C', '##')],
        ['C♯♯', MusicNote('C', '##')],
        ['C𝄪', MusicNote('C', '##')],

        ['Eb', MusicNote('E', 'b')],
        ['E♭', MusicNote('E', 'b')],

        ['Gbb', MusicNote('G', 'bb')],
        ['G♭♭', MusicNote('G', 'bb')],
        ['Gb♭', MusicNote('G', 'bb')],
        ['G𝄫', MusicNote('G', 'bb')],
    )

    ALTS_FAILS = (
        'Abbb',
        'A###',
        'C#e',
        'Bbr6',
    )

    def setUp(self):
        print()

    def testChars(self):
        for symbol, expected in self.CHAR_TESTS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testOctaves(self):
        for symbol, expected in self.OCTAVE_TESTS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testOctaveFails(self):
        for octave in range(MAXIMUM_OCTAVE+1, MAXIMUM_OCTAVE+50):
            note = f'A{octave}'
            parser = MusicNoteParser(note)
            self.assertRaises(InvalidOctave, parser.parse)

    def testAlterations(self):
        for symbol, expected in self.ALTS_TESTS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testAlterationFails(self):
        for note in self.ALTS_FAILS:
            parser = MusicNoteParser(note)
            self.assertRaises(InvalidAlteration, parser.parse)
