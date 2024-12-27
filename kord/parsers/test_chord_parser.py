import unittest

from .chord_parser import ChordParser

from ..keys.chords import (
    PowerChord,
    Suspended4Chord, Suspended2Chord,

    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,

    MajorSixthChord, MinorSixthChord,

    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    DiminishedSeventhChord, HalfDiminishedSeventhChord,

    DominantNinthChord, DominantMinorNinthChord,
    MajorNinthChord, MinorNinthChord,

)

from ..notes import NotePitch

from ..errors import InvalidChord

__all__ = [
    'ChordParserTest',
    'NonThirdChordsTest',
    'TriadChordsTest',
    'SixthChordsTest',
    'SeventhChordsTest',
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

        self.assertRaises(InvalidChord, ChordParser('Dsharp').parse)
        self.assertRaises(InvalidChord, ChordParser('Eflat').parse)
        self.assertRaises(InvalidChord, ChordParser('pmin7').parse)

        # self.assertRaises(InvalidChord, ChordParser('CB').parse)  # should fail...
        # self.assertRaises(InvalidChord, ChordParser('Cqwe').parse)  # should fail...


class NonThirdChordsTest(unittest.TestCase):

    def testPowerChordClasses(self):
        assert isinstance(ChordParser('g5').parse(), PowerChord)

    def testPowerChordRoots(self):
        F = NotePitch('F')
        assert ChordParser('F5').parse().root ** F


    def testSuspended4ChordClasses(self):
        assert isinstance(ChordParser('D♭♭sus4').parse(), Suspended4Chord)
        assert isinstance(ChordParser('Fsus').parse(), Suspended4Chord)

    def testSuspended4ChordRoots(self):
        Gflatflat = NotePitch('G', 'bb')
        assert ChordParser('G𝄫sus4').parse().root ** Gflatflat
        assert ChordParser('gbbsus').parse().root ** Gflatflat


    def testSuspended2ChordClasses(self):
        assert isinstance(ChordParser('A♯sus2').parse(), Suspended2Chord)
        assert isinstance(ChordParser('Esus9').parse(), Suspended2Chord)

    def testSuspended4ChordRoots(self):
        Gsharpsharp = NotePitch('G', '##')
        assert ChordParser('G##sus2').parse().root ** Gsharpsharp
        assert ChordParser('g𝄪sus9').parse().root ** Gsharpsharp




class TriadChordsTest(unittest.TestCase):

    def testMajorTriadClasses(self):
        assert isinstance(ChordParser('A').parse(), MajorTriad)
        assert isinstance(ChordParser('Dmaj').parse(), MajorTriad)
        assert isinstance(ChordParser('Emajor').parse(), MajorTriad)

    def testMajorTriadRoots(self):
        C = NotePitch('C')
        assert ChordParser('C').parse().root ** C
        assert ChordParser('Cmaj').parse().root ** C
        assert ChordParser('Cmajor').parse().root ** C

    # def testMajorTriadBass(self):
    #     C = NotePitch('C')
    #     assert ChordParser('C').parse().bass ** C
    #     assert ChordParser('Cmaj').parse().bass ** C
    #     assert ChordParser('Cmajor').parse().bass ** C


    def testMinorTriadClasses(self):
        assert isinstance(ChordParser('Bmin').parse(), MinorTriad)
        assert isinstance(ChordParser('F-').parse(), MinorTriad)
        assert isinstance(ChordParser('Cminor').parse(), MinorTriad)

    def testMinorTriadRoots(self):
        E = NotePitch('E')
        assert ChordParser('Emin').parse().root ** E
        assert ChordParser('e-').parse().root ** E
        assert ChordParser('Eminor').parse().root ** E


    def testAugTriadClasses(self):
        assert isinstance(ChordParser('C##aug').parse(), AugmentedTriad)
        assert isinstance(ChordParser('Bbaugmented').parse(), AugmentedTriad)

    def testAugTriadRoots(self):
        A = NotePitch('A')
        assert ChordParser('Aaug').parse().root ** A
        assert ChordParser('Aaugmented').parse().root ** A


    def testDimTriadClasses(self):
        assert isinstance(ChordParser('D#dim').parse(), DiminishedTriad)
        assert isinstance(ChordParser('Bbdiminished').parse(), DiminishedTriad)

    def testDimTriadRoots(self):
        D = NotePitch('D')
        assert ChordParser('Ddim').parse().root ** D
        assert ChordParser('Ddiminished').parse().root ** D
        assert ChordParser('D dim').parse().root ** D


class SixthChordsTest(unittest.TestCase):

    def testMajorSixthChordClasses(self):
        assert isinstance(ChordParser('D#6').parse(), MajorSixthChord)
        assert isinstance(ChordParser('Fadd6').parse(), MajorSixthChord)

    def testMajorSixthChordRoots(self):
        Bflat = NotePitch('B', 'b')
        assert ChordParser('Bb6').parse().root ** Bflat
        assert ChordParser('B♭add6').parse().root ** Bflat


    def testMinorSixthChordClasses(self):
        assert isinstance(ChordParser('Ebm6').parse(), MinorSixthChord)
        assert isinstance(ChordParser('Fmin6').parse(), MinorSixthChord)

    def testMinorSixthChordRoots(self):
        Asharp = NotePitch('A', '#')
        assert ChordParser('A♯m6').parse().root ** Asharp
        assert ChordParser('A#min6').parse().root ** Asharp



class SeventhChordsTest(unittest.TestCase):

    def testMajorSeventhChordClasses(self):
        assert isinstance(ChordParser('Amaj7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('BM7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('CΔ7').parse(), MajorSeventhChord)
        assert isinstance(ChordParser('Dmajor7').parse(), MajorSeventhChord)

    def testMajorSeventhChordRoots(self):
        C = NotePitch('C')
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
        A = NotePitch('A')
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
        Csharp = NotePitch('C', '#')
        assert ChordParser('C#7').parse().root ** Csharp
        assert ChordParser('C♯dom7').parse().root ** Csharp
        assert ChordParser('c#dominant7').parse().root ** Csharp


    def testHalfDiminishedSeventhChordClasses(self):
        assert isinstance(ChordParser('Em7b5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('F#m7-5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('Gmin7dim5').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('Gbm7(b5)').parse(), HalfDiminishedSeventhChord)
        assert isinstance(ChordParser('fø7').parse(), HalfDiminishedSeventhChord)

    def testHalfDiminishedSeventhChordRoots(self):
        Eflat = NotePitch('E', 'b')
        assert ChordParser('ebm7b5').parse().root ** Eflat
        assert ChordParser('E♭m7-5').parse().root ** Eflat
        assert ChordParser('Ebmin7dim5').parse().root ** Eflat
        assert ChordParser('Ebm7(b5)').parse().root ** Eflat
        assert ChordParser('Ebø7').parse().root ** Eflat


    def testDiminishedSeventhChordClasses(self):
        assert isinstance(ChordParser('fdim7').parse(), DiminishedSeventhChord)
        assert isinstance(ChordParser('ao7').parse(), DiminishedSeventhChord)
        assert isinstance(ChordParser('Cdiminished7').parse(), DiminishedSeventhChord)

    def testDiminishedSeventhChordRoots(self):
        Dflat = NotePitch('D', 'b')
        assert ChordParser('Dbdim7').parse().root ** Dflat
        assert ChordParser('Dbo7').parse().root ** Dflat
        assert ChordParser('Dbdiminished7').parse().root ** Dflat


class NinthChordsTest(unittest.TestCase):

    def testMajorNinthChordClasses(self):
        assert isinstance(ChordParser('D#maj9').parse(), MajorNinthChord)
        assert isinstance(ChordParser('FM9').parse(), MajorNinthChord)
        assert isinstance(ChordParser('Emajor9').parse(), MajorNinthChord)

    def testMajorNinthChordRoots(self):
        Bflat = NotePitch('B', 'b')
        assert ChordParser('Bbmaj7').parse().root ** Bflat
        assert ChordParser('B♭M7').parse().root ** Bflat
        assert ChordParser('b♭major7').parse().root ** Bflat


    def testMinorNinthChordClasses(self):
        assert isinstance(ChordParser('Ebmin9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('Fm9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('G#-9').parse(), MinorNinthChord)
        assert isinstance(ChordParser('Bminor9').parse(), MinorNinthChord)

    def testMinorNinthChordRoots(self):
        Asharp = NotePitch('A', '#')
        assert ChordParser('A♯min9').parse().root ** Asharp
        assert ChordParser('A#m9').parse().root ** Asharp
        assert ChordParser('A#-9').parse().root ** Asharp
        assert ChordParser('A♯minor9').parse().root ** Asharp
        assert ChordParser('A# min9').parse().root ** Asharp


    def testDomNinthChordClasses(self):
        assert isinstance(ChordParser('F9').parse(), DominantNinthChord)
        assert isinstance(ChordParser('Bbdom9').parse(), DominantNinthChord)

    def testDomNinthChordRoots(self):
        Csharp = NotePitch('C', '#')
        assert ChordParser('C#9').parse().root ** Csharp
        assert ChordParser('C♯dom9').parse().root ** Csharp


    def testDomMinNinthChordClasses(self):
        assert isinstance(ChordParser('E7b9').parse(), DominantMinorNinthChord)

    def testDomMinNinthChordRoots(self):
        Eflat = NotePitch('E', 'b')
        assert ChordParser('eb7b9').parse().root ** Eflat


