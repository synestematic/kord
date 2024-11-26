import unittest

from .parsers import MusicNoteParser

from .notes import MusicNote, MAXIMUM_OCTAVE

from .errors import InvalidOctave

class MusicNoteParserTest(unittest.TestCase):

    ALT_TESTS = (
        ['D#', MusicNote('D', '#')],
        ['D♯', MusicNote('D', '#')],

        ['C##', MusicNote('C', '##')],
        ['C♯♯', MusicNote('C', '##')],
        ['C𝄪', MusicNote('C', '##')],

        ['Eb', MusicNote('E', 'b')],
        ['E♭', MusicNote('E', 'b')],

        ['Gbb', MusicNote('G', 'bb')],
        ['G♭♭', MusicNote('G', 'bb')],
        ['G𝄫', MusicNote('G', 'bb')],
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

    def setUp(self):
        print()

    def testOctaves(self):
        for symbol, expected in self.OCTAVE_TESTS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testOctaveFails(self):
        for octave in range(MAXIMUM_OCTAVE+1, MAXIMUM_OCTAVE+50):
            parser = MusicNoteParser(f'A{octave}')
            self.assertRaises(InvalidOctave, parser.parse)

    def testAlterations(self):
        for symbol, expected in self.ALT_TESTS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)
