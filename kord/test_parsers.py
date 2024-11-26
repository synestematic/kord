import unittest

from .parsers import MusicNoteParser

from .notes import MusicNote

class MusicNoteParserTest(unittest.TestCase):

    TESTS = (
        ['B', MusicNote('B')],
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

        ['A6', MusicNote('A', 6)],
        ['A6', MusicNote('A', '', 6)],
        ['Ab6', MusicNote('A', 'b', 6)],
        ['A#6', MusicNote('A', '#', 6)],
    )

    def setUp(self):
        print()

    def testParsedNotes(self):
        for symbol, expected in self.TESTS:
            parser = MusicNoteParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)
