import unittest

from .parsers import NotePitchParser, ChordParser

from kord.keys.chords import (
    PowerChord,
    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    DiminishedSeventhChord, HalfDiminishedSeventhChord,
    DominantNinthChord, DominantMinorNinthChord,
    MajorNinthChord, MinorNinthChord,
    MajorSixthChord, MinorSixthChord,
    SuspendedFourChord, SuspendedTwoChord,
)
from .notes import MusicNote

from .errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

__all__ = [
    'NotePitchParserTest',
    'ChordParserTest',
]


class ChordParserTest(unittest.TestCase):

    def testInvalidChords(self):
        self.assertRaises(InvalidChord, ChordParser('').parse)
        self.assertRaises(InvalidChord, ChordParser('#').parse)
        self.assertRaises(InvalidChord, ChordParser('♯').parse)
        self.assertRaises(InvalidChord, ChordParser('♭').parse)
        self.assertRaises(InvalidChord, ChordParser('#F').parse)
        self.assertRaises(InvalidChord, ChordParser('♭B').parse)
        self.assertRaises(InvalidChord, ChordParser('H').parse)

        self.assertRaises(InvalidChord, ChordParser('Dsharp').parse)
        self.assertRaises(InvalidChord, ChordParser('Eflat').parse)
        self.assertRaises(InvalidChord, ChordParser('pmin7').parse)

        # self.assertRaises(InvalidChord, ChordParser('CB').parse)  # should fail...
        # self.assertRaises(InvalidChord, ChordParser('Cqwe').parse)  # should fail...

    ####################
    ### POWER CHORDS ###
    ####################

    def testPowerChordClasses(self):
        assert isinstance(ChordParser('g5').parse(), PowerChord)

    def testPowerChordRoots(self):
        F = MusicNote('F')
        assert ChordParser('F5').parse().root ** F


    ####################
    ### TRIAD CHORDS ###
    ####################

    def testMajorTriadClasses(self):
        assert isinstance(ChordParser('A').parse(), MajorTriad)
        assert isinstance(ChordParser('Dmaj').parse(), MajorTriad)
        assert isinstance(ChordParser('Emajor').parse(), MajorTriad)

    def testMajorTriadRoots(self):
        C = MusicNote('C')
        assert ChordParser('C').parse().root ** C
        assert ChordParser('Cmaj').parse().root ** C
        assert ChordParser('Cmajor').parse().root ** C

    # def testMajorTriadBass(self):
    #     C = MusicNote('C')
    #     assert ChordParser('C').parse().bass ** C
    #     assert ChordParser('Cmaj').parse().bass ** C
    #     assert ChordParser('Cmajor').parse().bass ** C

    def testMinorTriadClasses(self):
        assert isinstance(ChordParser('Bmin').parse(), MinorTriad)
        assert isinstance(ChordParser('F-').parse(), MinorTriad)
        assert isinstance(ChordParser('Cminor').parse(), MinorTriad)

    def testMinorTriadRoots(self):
        E = MusicNote('E')
        assert ChordParser('Emin').parse().root ** E
        assert ChordParser('e-').parse().root ** E
        assert ChordParser('Eminor').parse().root ** E

    def testAugTriadClasses(self):
        assert isinstance(ChordParser('C##aug').parse(), AugmentedTriad)
        assert isinstance(ChordParser('Bbaugmented').parse(), AugmentedTriad)

    def testAugTriadRoots(self):
        A = MusicNote('A')
        assert ChordParser('Aaug').parse().root ** A
        assert ChordParser('Aaugmented').parse().root ** A

    def testDimTriadClasses(self):
        assert isinstance(ChordParser('D#dim').parse(), DiminishedTriad)
        assert isinstance(ChordParser('Bbdiminished').parse(), DiminishedTriad)

    def testDimTriadRoots(self):
        D = MusicNote('D')
        assert ChordParser('Ddim').parse().root ** D
        assert ChordParser('Ddiminished').parse().root ** D
        assert ChordParser('D dim').parse().root ** D


    ######################
    ### SEVENTH CHORDS ###
    ######################

    def testMajorSeventhChordClasses(self):
        assert isinstance(ChordParser('Amaj7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('BM7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('CΔ7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('Dmajor7').parse(), MajorSeventhChord)

    def testMajorSeventhChordRoots(self):
        C = MusicNote('C')
        assert ChordParser('Cmaj7').parse().root ** C
        assert ChordParser('CM7').parse().root ** C
        assert ChordParser('CΔ7').parse().root ** C
        assert ChordParser('Cmajor7').parse().root ** C

    def testMinorSeventhChordClasses(self):
        assert isinstance(ChordParser('Emin7').parse(), MinorSeventhChord)
        assert isinstance(ChordParser('Fm7').parse(), MinorSeventhChord)
        assert isinstance(ChordParser('G-7').parse(), MinorSeventhChord)
        assert isinstance(ChordParser('Bbminor7').parse(), MinorSeventhChord)

    def testMinorSeventhChordRoots(self):
        A = MusicNote('A')
        assert ChordParser('Amin7').parse().root ** A
        assert ChordParser('Am7').parse().root ** A
        assert ChordParser('A-7').parse().root ** A
        assert ChordParser('Aminor7').parse().root ** A
        assert ChordParser('A minor7').parse().root ** A

    def testDomSeventhChordClasses(self):
        assert isinstance(ChordParser('F7').parse(), DominantSeventhChord)
        assert isinstance(ChordParser('Bbdom7').parse(), DominantSeventhChord)
        assert isinstance(ChordParser('Dbbdominant7').parse(), DominantSeventhChord)

    def testDomSeventhChordRoots(self):
        Csharp = MusicNote('C', '#')
        assert ChordParser('C#7').parse().root ** Csharp
        assert ChordParser('C♯dom7').parse().root ** Csharp
        assert ChordParser('c#dominant7').parse().root ** Csharp

    def testDiminishedSeventhChordClasses(self):
        assert isinstance(ChordParser('fdim7').parse(), DiminishedSeventhChord)
        assert isinstance(ChordParser('ao7').parse(), DiminishedSeventhChord)
        assert isinstance(ChordParser('Cdiminished7').parse(), DiminishedSeventhChord)

    def testDiminishedSeventhChordRoots(self):
        Dflat = MusicNote('D', 'b')
        assert ChordParser('Dbdim7').parse().root ** Dflat
        assert ChordParser('Dbo7').parse().root ** Dflat
        assert ChordParser('Dbdiminished7').parse().root ** Dflat

    def testHalfDiminishedSeventhChordClasses(self):
        assert isinstance(ChordParser('Em7b5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('F#m7-5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('Gmin7dim5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('Gbm7(b5)').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('fø7').parse(), HalfDiminishedSeventhChord)

    def testHalfDiminishedSeventhChordRoots(self):
        Eflat = MusicNote('E', 'b')
        assert ChordParser('ebm7b5').parse().root ** Eflat
        assert ChordParser('E♭m7-5').parse().root ** Eflat
        assert ChordParser('Ebmin7dim5').parse().root ** Eflat
        assert ChordParser('Ebm7(b5)').parse().root ** Eflat
        assert ChordParser('Ebø7').parse().root ** Eflat


    ####################
    ### NINTH CHORDS ###
    ####################

    def testMajorNinthChordClasses(self):
        assert isinstance(ChordParser('D#maj9').parse(), MajorNinthChord)
        assert isinstance(ChordParser('FM9').parse(), MajorNinthChord)
        assert isinstance(ChordParser('Emajor9').parse(), MajorNinthChord)

    def testMajorNinthChordRoots(self):
        Bflat = MusicNote('B', 'b')
        assert ChordParser('Bbmaj7').parse().root ** Bflat
        assert ChordParser('B♭M7').parse().root ** Bflat
        assert ChordParser('b♭major7').parse().root ** Bflat

    def testMinorNinthChordClasses(self):
        assert isinstance(ChordParser('Ebmin9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('Fm9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('G#-9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('Bminor9').parse(), MinorNinthChord)

    def testMinorNinthChordRoots(self):
        Asharp = MusicNote('A', '#')
        assert ChordParser('A♯min9').parse().root ** Asharp
        assert ChordParser('A#m9').parse().root ** Asharp
        assert ChordParser('A#-9').parse().root ** Asharp
        assert ChordParser('A♯minor9').parse().root ** Asharp
        assert ChordParser('A# min9').parse().root ** Asharp

    def testDomNinthChordClasses(self):
        assert isinstance(ChordParser('F9').parse(), DominantNinthChord)
        assert isinstance(ChordParser('Bbdom9').parse(), DominantNinthChord)

    def testDomNinthChordRoots(self):
        Csharp = MusicNote('C', '#')
        assert ChordParser('C#9').parse().root ** Csharp
        assert ChordParser('C♯dom9').parse().root ** Csharp

    def testDomMinNinthChordClasses(self):
        assert isinstance(ChordParser('E7b9').parse(), DominantMinorNinthChord)

    def testDomMinNinthChordRoots(self):
        Eflat = MusicNote('E', 'b')
        assert ChordParser('eb7b9').parse().root ** Eflat



    ####################
    ### SIXTH CHORDS ###
    ####################

    def testMajorSixthChordClasses(self):
        assert isinstance(ChordParser('D#6').parse(), MajorSixthChord)
        assert isinstance(ChordParser('Fadd6').parse(), MajorSixthChord)

    def testMajorSixthChordRoots(self):
        Bflat = MusicNote('B', 'b')
        assert ChordParser('Bb6').parse().root ** Bflat
        assert ChordParser('B♭add6').parse().root ** Bflat

    def testMinorSixthChordClasses(self):
        assert isinstance(ChordParser('Ebm6').parse(), MinorSixthChord)
        assert isinstance(ChordParser('Fmin6').parse(), MinorSixthChord)

    def testMinorSixthChordRoots(self):
        Asharp = MusicNote('A', '#')
        assert ChordParser('A♯m6').parse().root ** Asharp
        assert ChordParser('A#min6').parse().root ** Asharp


    ########################
    ### SUSPENDED CHORDS ###
    ########################

    def testSuspendedFourChordClasses(self):
        assert isinstance(ChordParser('D♭♭sus4').parse(), SuspendedFourChord)
        assert isinstance(ChordParser('Fsus').parse(), SuspendedFourChord)

    def testSuspendedFourChordRoots(self):
        Gflatflat = MusicNote('G', 'bb')
        assert ChordParser('G𝄫sus4').parse().root ** Gflatflat
        assert ChordParser('gbbsus').parse().root ** Gflatflat

    def testSuspendedTwoChordClasses(self):
        assert isinstance(ChordParser('A♯sus2').parse(), SuspendedTwoChord)
        assert isinstance(ChordParser('Esus9').parse(), SuspendedTwoChord)

    def testSuspendedFourChordRoots(self):
        Gsharpsharp = MusicNote('G', '##')
        assert ChordParser('G##sus2').parse().root ** Gsharpsharp
        assert ChordParser('g𝄪sus9').parse().root ** Gsharpsharp



class NotePitchParserTest(unittest.TestCase):

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
        '',
        'H',
        'T',
        'Y',
        'h',
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
