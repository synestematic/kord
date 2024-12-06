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

    ####################
    ### TRIAD CHORDS ###
    ####################

    def testMajorTriadClasses(self):
        assert isinstance(MusicChordParser('A').parse(), MajorTriad)
        assert isinstance(MusicChordParser('Dmaj').parse(), MajorTriad)
        assert isinstance(MusicChordParser('Emajor').parse(), MajorTriad)

    def testMajorTriadRoots(self):
        C = MusicNote('C')
        assert MusicChordParser('C').parse().root ** C
        assert MusicChordParser('Cmaj').parse().root ** C
        assert MusicChordParser('Cmajor').parse().root ** C

    # def testMajorTriadBass(self):
    #     C = MusicNote('C')
    #     assert MusicChordParser('C').parse().bass ** C
    #     assert MusicChordParser('Cmaj').parse().bass ** C
    #     assert MusicChordParser('Cmajor').parse().bass ** C

    def testMinorTriadClasses(self):
        assert isinstance(MusicChordParser('Bmin').parse(), MinorTriad)
        assert isinstance(MusicChordParser('F-').parse(), MinorTriad)
        assert isinstance(MusicChordParser('Cminor').parse(), MinorTriad)

    def testMinorTriadRoots(self):
        E = MusicNote('E')
        assert MusicChordParser('Emin').parse().root ** E
        assert MusicChordParser('e-').parse().root ** E
        assert MusicChordParser('Eminor').parse().root ** E

    def testAugTriadClasses(self):
        assert isinstance(MusicChordParser('C##aug').parse(), AugmentedTriad)
        assert isinstance(MusicChordParser('Bbaugmented').parse(), AugmentedTriad)

    def testAugTriadRoots(self):
        A = MusicNote('A')
        assert MusicChordParser('Aaug').parse().root ** A
        assert MusicChordParser('Aaugmented').parse().root ** A

    def testDimTriadClasses(self):
        assert isinstance(MusicChordParser('D#dim').parse(), DiminishedTriad)
        assert isinstance(MusicChordParser('Bbdiminished').parse(), DiminishedTriad)

    def testDimTriadRoots(self):
        D = MusicNote('D')
        assert MusicChordParser('Ddim').parse().root ** D
        assert MusicChordParser('Ddiminished').parse().root ** D


    ######################
    ### SEVENTH CHORDS ###
    ######################

    def testMajorSeventhChordClasses(self):
        assert isinstance(MusicChordParser('Amaj7').parse(), MajorSeventhChord)
        assert isinstance(MusicChordParser('BM7').parse(), MajorSeventhChord)
        assert isinstance(MusicChordParser('CΔ7').parse(), MajorSeventhChord)
        assert isinstance(MusicChordParser('Dmajor7').parse(), MajorSeventhChord)

    def testMajorSeventhChordRoots(self):
        C = MusicNote('C')
        assert MusicChordParser('Cmaj7').parse().root ** C
        assert MusicChordParser('CM7').parse().root ** C
        assert MusicChordParser('CΔ7').parse().root ** C
        assert MusicChordParser('Cmajor7').parse().root ** C

    def testMinorSeventhChordClasses(self):
        assert isinstance(MusicChordParser('Emin7').parse(), MinorSeventhChord)
        assert isinstance(MusicChordParser('Fm7').parse(), MinorSeventhChord)
        assert isinstance(MusicChordParser('G-7').parse(), MinorSeventhChord)
        assert isinstance(MusicChordParser('Bbminor7').parse(), MinorSeventhChord)

    def testMinorSeventhChordRoots(self):
        A = MusicNote('A')
        assert MusicChordParser('Amin7').parse().root ** A
        assert MusicChordParser('Am7').parse().root ** A
        assert MusicChordParser('A-7').parse().root ** A
        assert MusicChordParser('Aminor7').parse().root ** A

    def testDomSeventhChordClasses(self):
        assert isinstance(MusicChordParser('F7').parse(), DominantSeventhChord)
        assert isinstance(MusicChordParser('Bbdom7').parse(), DominantSeventhChord)
        assert isinstance(MusicChordParser('Dbbdominant7').parse(), DominantSeventhChord)

    def testDomSeventhChordRoots(self):
        Csharp = MusicNote('C', '#')
        assert MusicChordParser('C#7').parse().root ** Csharp
        assert MusicChordParser('C#dom7').parse().root ** Csharp
        assert MusicChordParser('C#dominant7').parse().root ** Csharp

    def testDiminishedSeventhChordClasses(self):
        assert isinstance(MusicChordParser('fdim7').parse(), DiminishedSeventhChord)
        assert isinstance(MusicChordParser('ao7').parse(), DiminishedSeventhChord)
        assert isinstance(MusicChordParser('Cdiminished7').parse(), DiminishedSeventhChord)

    def testDiminishedSeventhChordRoots(self):
        Dflat = MusicNote('D', 'b')
        assert MusicChordParser('Dbdim7').parse().root ** Dflat
        assert MusicChordParser('Dbo7').parse().root ** Dflat
        assert MusicChordParser('Dbdiminished7').parse().root ** Dflat


    def testHalfDiminishedSeventhChordClasses(self):
        assert isinstance(MusicChordParser('Em7b5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(MusicChordParser('Gmin7dim5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(MusicChordParser('Gbm7(b5)').parse(), HalfDiminishedSeventhChord)
        assert isinstance(MusicChordParser('fø7').parse(), HalfDiminishedSeventhChord)

    def testHalfDiminishedSeventhChordRoots(self):
        Eflat = MusicNote('E', 'b')
        assert MusicChordParser('ebm7b5').parse().root ** Eflat
        assert MusicChordParser('Ebmin7dim5').parse().root ** Eflat
        assert MusicChordParser('Ebm7(b5)').parse().root ** Eflat
        assert MusicChordParser('Ebø7').parse().root ** Eflat


    ####################
    ### NINTH CHORDS ###
    ####################


    def testFails(self):
        self.assertRaises(InvalidChord, MusicChordParser('H').parse)
        self.assertRaises(InvalidChord, MusicChordParser('B m7').parse)
        # self.assertRaises(InvalidChord, MusicChordParser('Db#').parse)


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
