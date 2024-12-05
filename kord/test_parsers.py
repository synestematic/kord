import unittest

from .parsers import MusicNoteParser, MusicChordParser

from kord.keys.chords import (
    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    DiminishedSeventhChord, HalfDiminishedSeventhChord,
    MajorNinthChord, MinorNinthChord, DominantNinthChord
)
from .notes import MusicNote

from .errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

__all__ = [
    'MusicNoteParserTest',
    'MusicChordParserTest',
]


class MusicChordParserTest(unittest.TestCase):

    def testMajorSeventhChordClasses(self):
        assert isinstance(MusicChordParser('Amaj7').parse(), MajorSeventhChord)
        assert isinstance(MusicChordParser('BM7').parse(), MajorSeventhChord)
        assert isinstance(MusicChordParser('CΔ7').parse(), MajorSeventhChord)
        assert isinstance(MusicChordParser('Dmajor7').parse(), MajorSeventhChord)

    def testMajorSeventhChordRoots(self):
        C = MusicNote('C')
        assert MusicChordParser('Cmaj7').parse().root ** C, C
        assert MusicChordParser('CM7').parse().root ** C, C
        assert MusicChordParser('CΔ7').parse().root ** C, C
        assert MusicChordParser('Cmajor7').parse().root ** C, C

    def testMinorSeventhChordClasses(self):
        assert isinstance(MusicChordParser('Emin7').parse(), MinorSeventhChord)
        assert isinstance(MusicChordParser('Fm7').parse(), MinorSeventhChord)
        assert isinstance(MusicChordParser('G-7').parse(), MinorSeventhChord)
        assert isinstance(MusicChordParser('Bbminor7').parse(), MinorSeventhChord)

    def testMinorSeventhChordRoots(self):
        A = MusicNote('A')
        assert MusicChordParser('Amin7').parse().root ** A, A
        assert MusicChordParser('Am7').parse().root ** A, A
        assert MusicChordParser('A-7').parse().root ** A, A
        assert MusicChordParser('Aminor7').parse().root ** A, A

    def testFails(self):
        self.assertRaises(InvalidChord, MusicChordParser('H').parse)
        self.assertRaises(InvalidChord, MusicChordParser('A♯♭𝄫𝄪add13').parse)
        self.assertRaises(InvalidChord, MusicChordParser('C♯♭𝄫𝄪add13').parse)


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
