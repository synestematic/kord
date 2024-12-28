import unittest

from .chord_parser import ChordParser

from ..keys.chords import (
    PowerChord, Suspended4Chord, Suspended2Chord,
    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
    MajorSixthChord, MinorSixthChord,
    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    HalfDiminishedSeventhChord, DiminishedSeventhChord,
    MajorAdd9Chord, MinorAdd9Chord, AugmentedAdd9Chord, DiminishedAdd9Chord,
    DominantNinthChord, DominantMinorNinthChord,
    MajorNinthChord, MinorNinthChord,
)

from ..notes.constants import (
    C_3, F_3, E_3, A_3, D_3,
    B_FLAT_3, E_FLAT_3, D_FLAT_3, C_FLAT_3, B_FLAT_3,
    A_SHARP_3, C_SHARP_3, E_SHARP_3,
    G_DOUBLE_FLAT_3,
    G_DOUBLE_SHARP_3,
)

from ..errors import InvalidChord

__all__ = [
    'ChordParserTest',
    'NonThirdChordsTest',
    'TriadChordsTest',
    'SixthChordsTest',
    'SeventhChordsTest',
    'Add9ChordsTest',
    'NinthChordsTest',
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
        self.assertRaises(InvalidChord, ChordParser('h').parse)

        self.assertRaises(InvalidChord, ChordParser('Dsharp').parse)
        self.assertRaises(InvalidChord, ChordParser('Eflat').parse)
        self.assertRaises(InvalidChord, ChordParser('pmin7').parse)

        # self.assertRaises(InvalidChord, ChordParser('CB').parse)  # should fail...
        # self.assertRaises(InvalidChord, ChordParser('Cqwe').parse)  # should fail...


class NonThirdChordsTest(unittest.TestCase):

    def testPowerChordClasses(self):
        assert isinstance(ChordParser('g5').parse(), PowerChord)

    def testPowerChordRoots(self):
        assert ChordParser('F5').parse().root ** F_3


    def testSuspended4ChordClasses(self):
        assert isinstance(ChordParser('D♭♭sus4').parse(), Suspended4Chord)
        assert isinstance(ChordParser('Fsus').parse(), Suspended4Chord)

    def testSuspended4ChordRoots(self):
        assert ChordParser('G𝄫sus4').parse().root ** G_DOUBLE_FLAT_3
        assert ChordParser('gbbsus').parse().root ** G_DOUBLE_FLAT_3


    def testSuspended2ChordClasses(self):
        assert isinstance(ChordParser('A♯sus2').parse(), Suspended2Chord)
        assert isinstance(ChordParser('Esus9').parse(), Suspended2Chord)

    def testSuspended4ChordRoots(self):
        assert ChordParser('G##sus2').parse().root ** G_DOUBLE_SHARP_3
        assert ChordParser('g𝄪sus9').parse().root ** G_DOUBLE_SHARP_3




class TriadChordsTest(unittest.TestCase):

    def testMajorTriadClasses(self):
        assert isinstance(ChordParser('A').parse(), MajorTriad)
        assert isinstance(ChordParser('Dmaj').parse(), MajorTriad)
        assert isinstance(ChordParser('Emajor').parse(), MajorTriad)

    def testMajorTriadRoots(self):
        assert ChordParser('C').parse().root ** C_3
        assert ChordParser('Cmaj').parse().root ** C_3
        assert ChordParser('Cmajor').parse().root ** C_3

    # def testMajorTriadBass(self):
    #     assert ChordParser('C').parse().bass ** C_3
    #     assert ChordParser('Cmaj').parse().bass ** C_3
    #     assert ChordParser('Cmajor').parse().bass ** C_3


    def testMinorTriadClasses(self):
        assert isinstance(ChordParser('Bmin').parse(), MinorTriad)
        assert isinstance(ChordParser('F-').parse(), MinorTriad)
        assert isinstance(ChordParser('Cminor').parse(), MinorTriad)

    def testMinorTriadRoots(self):
        assert ChordParser('Emin').parse().root ** E_3
        assert ChordParser('e-').parse().root ** E_3
        assert ChordParser('Eminor').parse().root ** E_3


    def testAugTriadClasses(self):
        assert isinstance(ChordParser('C##aug').parse(), AugmentedTriad)
        assert isinstance(ChordParser('Bbaugmented').parse(), AugmentedTriad)

    def testAugTriadRoots(self):
        assert ChordParser('Aaug').parse().root ** A_3
        assert ChordParser('Aaugmented').parse().root ** A_3


    def testDimTriadClasses(self):
        assert isinstance(ChordParser('D#dim').parse(), DiminishedTriad)
        assert isinstance(ChordParser('Bbdiminished').parse(), DiminishedTriad)

    def testDimTriadRoots(self):
        assert ChordParser('Ddim').parse().root ** D_3
        assert ChordParser('Ddiminished').parse().root ** D_3
        assert ChordParser('D dim').parse().root ** D_3


class SixthChordsTest(unittest.TestCase):

    def testMajorSixthChordClasses(self):
        assert isinstance(ChordParser('D#6').parse(), MajorSixthChord)
        assert isinstance(ChordParser('Fadd6').parse(), MajorSixthChord)

    def testMajorSixthChordRoots(self):
        assert ChordParser('Bb6').parse().root ** B_FLAT_3
        assert ChordParser('B♭add6').parse().root ** B_FLAT_3


    def testMinorSixthChordClasses(self):
        assert isinstance(ChordParser('Ebm6').parse(), MinorSixthChord)
        assert isinstance(ChordParser('Fmin6').parse(), MinorSixthChord)

    def testMinorSixthChordRoots(self):
        assert ChordParser('A♯m6').parse().root ** A_SHARP_3
        assert ChordParser('A#min6').parse().root ** A_SHARP_3


class SeventhChordsTest(unittest.TestCase):

    def testMajorSeventhChordClasses(self):
        assert isinstance(ChordParser('Amaj7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('BM7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('CΔ7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('Dmajor7').parse(), MajorSeventhChord)

    def testMajorSeventhChordRoots(self):
        assert ChordParser('Cmaj7').parse().root ** C_3
        assert ChordParser('CM7').parse().root ** C_3
        assert ChordParser('CΔ7').parse().root ** C_3
        assert ChordParser('Cmajor7').parse().root ** C_3


    def testMinorSeventhChordClasses(self):
        assert isinstance(ChordParser('Emin7').parse(), MinorSeventhChord)
        assert isinstance(ChordParser('Fm7').parse(), MinorSeventhChord)
        assert isinstance(ChordParser('G-7').parse(), MinorSeventhChord)
        assert isinstance(ChordParser('Bbminor7').parse(), MinorSeventhChord)

    def testMinorSeventhChordRoots(self):
        assert ChordParser('Amin7').parse().root ** A_3
        assert ChordParser('Am7').parse().root ** A_3
        assert ChordParser('A-7').parse().root ** A_3
        assert ChordParser('Aminor7').parse().root ** A_3
        assert ChordParser('A minor7').parse().root ** A_3


    def testDomSeventhChordClasses(self):
        assert isinstance(ChordParser('F7').parse(), DominantSeventhChord)
        assert isinstance(ChordParser('Bbdom7').parse(), DominantSeventhChord)
        assert isinstance(ChordParser('Dbbdominant7').parse(), DominantSeventhChord)

    def testDomSeventhChordRoots(self):
        assert ChordParser('C#7').parse().root ** C_SHARP_3
        assert ChordParser('C♯dom7').parse().root ** C_SHARP_3
        assert ChordParser('c#dominant7').parse().root ** C_SHARP_3


    def testHalfDiminishedSeventhChordClasses(self):
        assert isinstance(ChordParser('Em7b5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('F#m7-5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('Gmin7dim5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('Gbm7(b5)').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('fø7').parse(), HalfDiminishedSeventhChord)

    def testHalfDiminishedSeventhChordRoots(self):
        assert ChordParser('ebm7b5').parse().root ** E_FLAT_3
        assert ChordParser('E♭m7-5').parse().root ** E_FLAT_3
        assert ChordParser('Ebmin7dim5').parse().root ** E_FLAT_3
        assert ChordParser('Ebm7(b5)').parse().root ** E_FLAT_3
        assert ChordParser('Ebø7').parse().root ** E_FLAT_3


    def testDiminishedSeventhChordClasses(self):
        assert isinstance(ChordParser('fdim7').parse(), DiminishedSeventhChord)
        assert isinstance(ChordParser('ao7').parse(), DiminishedSeventhChord)
        assert isinstance(ChordParser('Cdiminished7').parse(), DiminishedSeventhChord)

    def testDiminishedSeventhChordRoots(self):
        assert ChordParser('Dbdim7').parse().root ** D_FLAT_3
        assert ChordParser('Dbo7').parse().root ** D_FLAT_3
        assert ChordParser('Dbdiminished7').parse().root ** D_FLAT_3


class Add9ChordsTest(unittest.TestCase):

    def testMajorAdd9ChordClasses(self):
        assert isinstance(ChordParser('bAdd9').parse(), MajorAdd9Chord)
        assert isinstance(ChordParser('Aadd9').parse(), MajorAdd9Chord)

    def testMajorAdd9ChordRoots(self):
        assert ChordParser('Dbadd9').parse().root ** D_FLAT_3
        assert ChordParser('d♭Add9').parse().root ** D_FLAT_3


    def testMinorAdd9ChordClasses(self):
        assert isinstance(ChordParser('Emadd9').parse(), MinorAdd9Chord)
        assert isinstance(ChordParser('GmAdd9').parse(), MinorAdd9Chord)

    def testMinorAdd9ChordRoots(self):
        assert ChordParser('Cbmadd9').parse().root ** C_FLAT_3
        assert ChordParser('C♭mAdd9').parse().root ** C_FLAT_3


    def testAugmentedAdd9ChordClasses(self):
        assert isinstance(ChordParser('f#augadd9').parse(), AugmentedAdd9Chord)
        assert isinstance(ChordParser('D#augAdd9').parse(), AugmentedAdd9Chord)

    def testAugmentedAdd9ChordRoots(self):
        assert ChordParser('E♯augadd9').parse().root ** E_SHARP_3
        assert ChordParser('E#augAdd9').parse().root ** E_SHARP_3


    def testDiminishedAdd9ChordClasses(self):
        assert isinstance(ChordParser('Cdimadd9').parse(), DiminishedAdd9Chord)
        assert isinstance(ChordParser('F#dimAdd9').parse(), DiminishedAdd9Chord)

    def testDiminishedAdd9ChordRoots(self):
        assert ChordParser('E♯dimadd9').parse().root ** E_SHARP_3
        assert ChordParser('E#dimAdd9').parse().root ** E_SHARP_3


class NinthChordsTest(unittest.TestCase):

    def testMajorNinthChordClasses(self):
        assert isinstance(ChordParser('D#maj9').parse(), MajorNinthChord)
        assert isinstance(ChordParser('FM9').parse(), MajorNinthChord)
        assert isinstance(ChordParser('Emajor9').parse(), MajorNinthChord)

    def testMajorNinthChordRoots(self):
        assert ChordParser('Bbmaj7').parse().root ** B_FLAT_3
        assert ChordParser('B♭M7').parse().root ** B_FLAT_3
        assert ChordParser('b♭major7').parse().root ** B_FLAT_3


    def testMinorNinthChordClasses(self):
        assert isinstance(ChordParser('Ebmin9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('Fm9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('G#-9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('Bminor9').parse(), MinorNinthChord)

    def testMinorNinthChordRoots(self):
        assert ChordParser('A♯min9').parse().root ** A_SHARP_3
        assert ChordParser('A#m9').parse().root ** A_SHARP_3
        assert ChordParser('A#-9').parse().root ** A_SHARP_3
        assert ChordParser('A♯minor9').parse().root ** A_SHARP_3
        assert ChordParser('A# min9').parse().root ** A_SHARP_3


    def testDomNinthChordClasses(self):
        assert isinstance(ChordParser('F9').parse(), DominantNinthChord)
        assert isinstance(ChordParser('Bbdom9').parse(), DominantNinthChord)

    def testDomNinthChordRoots(self):
        assert ChordParser('C#9').parse().root ** C_SHARP_3
        assert ChordParser('C♯dom9').parse().root ** C_SHARP_3


    def testDomMinNinthChordClasses(self):
        assert isinstance(ChordParser('E7b9').parse(), DominantMinorNinthChord)

    def testDomMinNinthChordRoots(self):
        assert ChordParser('eb7b9').parse().root ** E_FLAT_3


