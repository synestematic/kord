import unittest

from .parsers import MusicNoteParser, MusicChordParser

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
    'MusicNoteParserTest',
    'MusicChordParserTest',
]


class MusicChordParserTest(unittest.TestCase):

    def testInvalidChords(self):
        self.assertRaises(InvalidChord, MusicChordParser('').parse)
        self.assertRaises(InvalidChord, MusicChordParser('#').parse)
        self.assertRaises(InvalidChord, MusicChordParser('♯').parse)
        self.assertRaises(InvalidChord, MusicChordParser('♭').parse)
        self.assertRaises(InvalidChord, MusicChordParser('#F').parse)
        self.assertRaises(InvalidChord, MusicChordParser('♭B').parse)
        self.assertRaises(InvalidChord, MusicChordParser('H').parse)

        self.assertRaises(InvalidChord, MusicChordParser('Dsharp').parse)
        self.assertRaises(InvalidChord, MusicChordParser('Eflat').parse)
        self.assertRaises(InvalidChord, MusicChordParser('pmin7').parse)

        # self.assertRaises(InvalidChord, MusicChordParser('CB').parse)  # should fail...
        # self.assertRaises(InvalidChord, MusicChordParser('Cqwe').parse)  # should fail...

    ####################
    ### POWER CHORDS ###
    ####################

    def testPowerChordClasses(self):
        assert isinstance(MusicChordParser('g5').parse(), PowerChord)

    def testPowerChordRoots(self):
        F = MusicNote('F')
        assert MusicChordParser('F5').parse().root ** F


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
        assert MusicChordParser('D dim').parse().root ** D


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
        assert MusicChordParser('A minor7').parse().root ** A

    def testDomSeventhChordClasses(self):
        assert isinstance(MusicChordParser('F7').parse(), DominantSeventhChord)
        assert isinstance(MusicChordParser('Bbdom7').parse(), DominantSeventhChord)
        assert isinstance(MusicChordParser('Dbbdominant7').parse(), DominantSeventhChord)

    def testDomSeventhChordRoots(self):
        Csharp = MusicNote('C', '#')
        assert MusicChordParser('C#7').parse().root ** Csharp
        assert MusicChordParser('C♯dom7').parse().root ** Csharp
        assert MusicChordParser('c#dominant7').parse().root ** Csharp

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
        assert isinstance(MusicChordParser('F#m7-5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(MusicChordParser('Gmin7dim5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(MusicChordParser('Gbm7(b5)').parse(), HalfDiminishedSeventhChord)
        assert isinstance(MusicChordParser('fø7').parse(), HalfDiminishedSeventhChord)

    def testHalfDiminishedSeventhChordRoots(self):
        Eflat = MusicNote('E', 'b')
        assert MusicChordParser('ebm7b5').parse().root ** Eflat
        assert MusicChordParser('E♭m7-5').parse().root ** Eflat
        assert MusicChordParser('Ebmin7dim5').parse().root ** Eflat
        assert MusicChordParser('Ebm7(b5)').parse().root ** Eflat
        assert MusicChordParser('Ebø7').parse().root ** Eflat


    ####################
    ### NINTH CHORDS ###
    ####################

    def testMajorNinthChordClasses(self):
        assert isinstance(MusicChordParser('D#maj9').parse(), MajorNinthChord)
        assert isinstance(MusicChordParser('FM9').parse(), MajorNinthChord)
        assert isinstance(MusicChordParser('Emajor9').parse(), MajorNinthChord)

    def testMajorNinthChordRoots(self):
        Bflat = MusicNote('B', 'b')
        assert MusicChordParser('Bbmaj7').parse().root ** Bflat
        assert MusicChordParser('B♭M7').parse().root ** Bflat
        assert MusicChordParser('b♭major7').parse().root ** Bflat

    def testMinorNinthChordClasses(self):
        assert isinstance(MusicChordParser('Ebmin9').parse(), MinorNinthChord)
        assert isinstance(MusicChordParser('Fm9').parse(), MinorNinthChord)
        assert isinstance(MusicChordParser('G#-9').parse(), MinorNinthChord)
        assert isinstance(MusicChordParser('Bminor9').parse(), MinorNinthChord)

    def testMinorNinthChordRoots(self):
        Asharp = MusicNote('A', '#')
        assert MusicChordParser('A♯min9').parse().root ** Asharp
        assert MusicChordParser('A#m9').parse().root ** Asharp
        assert MusicChordParser('A#-9').parse().root ** Asharp
        assert MusicChordParser('A♯minor9').parse().root ** Asharp
        assert MusicChordParser('A# min9').parse().root ** Asharp

    def testDomNinthChordClasses(self):
        assert isinstance(MusicChordParser('F9').parse(), DominantNinthChord)
        assert isinstance(MusicChordParser('Bbdom9').parse(), DominantNinthChord)

    def testDomNinthChordRoots(self):
        Csharp = MusicNote('C', '#')
        assert MusicChordParser('C#9').parse().root ** Csharp
        assert MusicChordParser('C♯dom9').parse().root ** Csharp

    def testDomMinNinthChordClasses(self):
        assert isinstance(MusicChordParser('E7b9').parse(), DominantMinorNinthChord)

    def testDomMinNinthChordRoots(self):
        Eflat = MusicNote('E', 'b')
        assert MusicChordParser('eb7b9').parse().root ** Eflat



    ####################
    ### SIXTH CHORDS ###
    ####################

    def testMajorSixthChordClasses(self):
        assert isinstance(MusicChordParser('D#6').parse(), MajorSixthChord)
        assert isinstance(MusicChordParser('Fadd6').parse(), MajorSixthChord)

    def testMajorSixthChordRoots(self):
        Bflat = MusicNote('B', 'b')
        assert MusicChordParser('Bb6').parse().root ** Bflat
        assert MusicChordParser('B♭add6').parse().root ** Bflat

    def testMinorSixthChordClasses(self):
        assert isinstance(MusicChordParser('Ebm6').parse(), MinorSixthChord)
        assert isinstance(MusicChordParser('Fmin6').parse(), MinorSixthChord)

    def testMinorSixthChordRoots(self):
        Asharp = MusicNote('A', '#')
        assert MusicChordParser('A♯m6').parse().root ** Asharp
        assert MusicChordParser('A#min6').parse().root ** Asharp


    ########################
    ### SUSPENDED CHORDS ###
    ########################

    def testSuspendedFourChordClasses(self):
        assert isinstance(MusicChordParser('D♭♭sus4').parse(), SuspendedFourChord)
        assert isinstance(MusicChordParser('Fsus').parse(), SuspendedFourChord)

    def testSuspendedFourChordRoots(self):
        Gflatflat = MusicNote('G', 'bb')
        assert MusicChordParser('G𝄫sus4').parse().root ** Gflatflat
        assert MusicChordParser('gbbsus').parse().root ** Gflatflat

    def testSuspendedTwoChordClasses(self):
        assert isinstance(MusicChordParser('A♯sus2').parse(), SuspendedTwoChord)
        assert isinstance(MusicChordParser('Esus9').parse(), SuspendedTwoChord)

    def testSuspendedFourChordRoots(self):
        Gsharpsharp = MusicNote('G', '##')
        assert MusicChordParser('G##sus2').parse().root ** Gsharpsharp
        assert MusicChordParser('g𝄪sus9').parse().root ** Gsharpsharp



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
