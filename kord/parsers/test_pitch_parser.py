import unittest

from .pitch_parser import NotePitchParser

from ..notes import NotePitch

from ..notes.constants import (
    C_3, F_3, E_3, A_3, D_3, G_3, B_3,
    D_SHARP_3, E_FLAT_3, C_DOUBLE_SHARP_3, G_DOUBLE_FLAT_3,
)

from ..errors import InvalidNote, InvalidAlteration, InvalidOctave

__all__ = [
    'NotePitchParserTest',
]

class NotePitchParserTest(unittest.TestCase):

    CHAR_WINS = [
        ['C', C_3],
        ['D', D_3],
        ['E', E_3],
        ['F', F_3],
        ['G', G_3],
        ['A', A_3],
        ['B', B_3],

        ['c', C_3],
        ['d', D_3],
        ['e', E_3],
        ['f', F_3],
        ['g', G_3],
        ['a', A_3],
        ['b', B_3],
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
        ['D#', D_SHARP_3],
        ['D♯', D_SHARP_3],

        ['C##', C_DOUBLE_SHARP_3],
        ['C♯♯', C_DOUBLE_SHARP_3],
        ['C#♯', C_DOUBLE_SHARP_3],
        ['C♯#', C_DOUBLE_SHARP_3],
        ['C𝄪',  C_DOUBLE_SHARP_3],

        ['Eb', E_FLAT_3],
        ['E♭', E_FLAT_3],

        ['Gbb', G_DOUBLE_FLAT_3],
        ['G♭♭', G_DOUBLE_FLAT_3],
        ['Gb♭', G_DOUBLE_FLAT_3],
        ['G♭b', G_DOUBLE_FLAT_3],
        ['G𝄫',  G_DOUBLE_FLAT_3],
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
