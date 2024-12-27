import unittest

from .parsers import NotePitchParser

from kord.keys.chords import (
    PowerChord,
    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    DiminishedSeventhChord, HalfDiminishedSeventhChord,
    DominantNinthChord, DominantMinorNinthChord,
    MajorNinthChord, MinorNinthChord,
    MajorSixthChord, MinorSixthChord,
    Suspended4Chord, Suspended2Chord,
)
from .notes import NotePitch

from .errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

__all__ = [
    'NotePitchParserTest',
]

class NotePitchParserTest(unittest.TestCase):

    CHAR_WINS = [
        ['C', NotePitch('C')],
        ['D', NotePitch('D')],
        ['E', NotePitch('E')],
        ['F', NotePitch('F')],
        ['G', NotePitch('G')],
        ['A', NotePitch('A')],
        ['B', NotePitch('B')],

        ['c', NotePitch('C')],
        ['d', NotePitch('D')],
        ['e', NotePitch('E')],
        ['f', NotePitch('F')],
        ['g', NotePitch('G')],
        ['a', NotePitch('A')],
        ['b', NotePitch('B')],
    ]

    CHAR_FAILS = [
        '',
        'H',
        'T',
        'Y',
        'h',
    ]

    OCTAVE_WINS = [
        [ f'C{octave}', NotePitch('C', octave) ] for octave
        in range(0, NotePitch.MAXIMUM_OCTAVE)
    ]

    OCTAVE_FAILS = [
        f'A{octave}' for octave
        in range(NotePitch.MAXIMUM_OCTAVE+1, NotePitch.MAXIMUM_OCTAVE+500)
    ]

    ALTS_WINS = [
        ['D#', NotePitch('D', '#')],
        ['D♯', NotePitch('D', '#')],

        ['C##', NotePitch('C', '##')],
        ['C♯♯', NotePitch('C', '##')],
        ['C#♯', NotePitch('C', '##')],
        ['C♯#', NotePitch('C', '##')],
        ['C𝄪', NotePitch('C', '##')],

        ['Eb', NotePitch('E', 'b')],
        ['E♭', NotePitch('E', 'b')],

        ['Gbb', NotePitch('G', 'bb')],
        ['G♭♭', NotePitch('G', 'bb')],
        ['Gb♭', NotePitch('G', 'bb')],
        ['G♭b', NotePitch('G', 'bb')],
        ['G𝄫', NotePitch('G', 'bb')],
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

        'Dsharp',
        'eSharp',
        'Eflat',
        'bFlat',

        'CB',
        'Cqwe',
    ]

    def setUp(self):
        print()

    def testChars(self):
        for symbol, expected in self.CHAR_WINS:
            parser = NotePitchParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testCharFails(self):
        for symbol in self.CHAR_FAILS:
            parser = NotePitchParser(symbol)
            self.assertRaises(InvalidNote, parser.parse)

    def testOctaves(self):
        for symbol, expected in self.OCTAVE_WINS:
            parser = NotePitchParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testOctaveFails(self):
        for symbol in self.OCTAVE_FAILS:
            parser = NotePitchParser(symbol)
            self.assertRaises(InvalidOctave, parser.parse)

    def testAlterations(self):
        for symbol, expected in self.ALTS_WINS:
            parser = NotePitchParser(symbol)
            parsed_note = parser.parse()
            self.assertEqual(parsed_note, expected)

    def testAlterationFails(self):
        for symbol in self.ALTS_FAILS:
            parser = NotePitchParser(symbol)
            self.assertRaises(InvalidAlteration, parser.parse)
