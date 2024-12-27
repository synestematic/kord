import unittest

from .chords import (
    PowerChord,
    Suspended4Chord, Suspended2Chord,
    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
    MajorSixthChord, MinorSixthChord,
    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    DiminishedSeventhChord, HalfDiminishedSeventhChord,
    MajorAdd9Chord, MinorAdd9Chord, AugmentedAdd9Chord, DiminishedAdd9Chord,
    MajorNinthChord, MinorNinthChord,
    DominantNinthChord, DominantMinorNinthChord,
)
from ..notes import NotePitch

from ..errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

__all__ = [
    'ChordTest',
]

A = NotePitch('A')
B = NotePitch('B')
C = NotePitch('C')
D = NotePitch('D')
E = NotePitch('E')
F = NotePitch('F')
G = NotePitch('G')

class ChordTest(unittest.TestCase):

    def testPowerChord(self):
        chord = PowerChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert not chord[3] , chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert not chord[10] , chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testSuspended4Chord(self):
        chord = Suspended4Chord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert not chord[3] , chord[3]
        assert chord[4] >> NotePitch('F', '', 0), chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert not chord[10] , chord[10]
        assert chord[11] >> NotePitch('F', '', 1), chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testSuspended2Chord(self):
        chord = Suspended2Chord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', '', 0), chord[2]
        assert not chord[3] , chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', '', 1), chord[9]
        assert not chord[10] , chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMajorTriad(self):
        chord = MajorTriad(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMinorTriad(self):
        chord = MinorTriad(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testAugmentedTriad(self):
        chord = AugmentedTriad(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '#', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '#', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testDiminishedTriad(self):
        chord = DiminishedTriad(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', 'b', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', 'b', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMajorSixthChordChord(self):
        chord = MajorSixthChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert chord[6] >> NotePitch('A', '', 0), chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert chord[13] >> NotePitch('A', '', 1), chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMinorSixthChord(self):
        chord = MinorSixthChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert chord[6] >> NotePitch('A', '', 0), chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert chord[13] >> NotePitch('A', '', 1), chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMajorSeventhChord(self):
        chord = MajorSeventhChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', '', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', '', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMinorSeventhChord(self):
        chord = MinorSeventhChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', 'b', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', 'b', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testDominantSeventhChord(self):
        chord = DominantSeventhChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', 'b', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', 'b', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testHalfDiminishedSeventhChord(self):
        chord = HalfDiminishedSeventhChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', 'b', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', 'b', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', 'b', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', 'b', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testDiminishedSeventhChord(self):
        chord = DiminishedSeventhChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', 'b', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', 'bb', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', 'b', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', 'bb', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMajorAdd9Chord(self):
        chord = MajorAdd9Chord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', '', 0), chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', '', 1), chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMinorAdd9Chord(self):
        chord = MinorAdd9Chord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', '', 0), chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', '', 1), chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testAugmentedAdd9Chord(self):
        chord = AugmentedAdd9Chord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', '', 0), chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '#', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', '', 1), chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '#', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testDiminishedAdd9Chord(self):
        chord = DiminishedAdd9Chord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', '', 0), chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', 'b', 0), chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', '', 1), chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', 'b', 1), chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMajorNinthChord(self):
        chord = MajorNinthChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', '', 0), chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', '', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', '', 1), chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', '', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testMinorNinthChord(self):
        chord = MinorNinthChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', '', 0), chord[2]
        assert chord[3] >> NotePitch('E', 'b', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', 'b', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', '', 1), chord[9]
        assert chord[10] >> NotePitch('E', 'b', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', 'b', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testDominantNinthChord(self):
        chord = DominantNinthChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', '', 0), chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', 'b', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', '', 1), chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', 'b', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]


    def testDominantMinorNinthChord(self):
        chord = DominantMinorNinthChord(*C)
        assert not chord[0] , chord[0]
        assert chord[1] >> NotePitch('C', '', 0), chord[1]
        assert chord[2] >> NotePitch('D', 'b', 0), chord[2]
        assert chord[3] >> NotePitch('E', '', 0), chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> NotePitch('G', '', 0), chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> NotePitch('B', 'b', 0), chord[7]
        assert chord[8] >> NotePitch('C', '', 1), chord[8]
        assert chord[9] >> NotePitch('D', 'b', 1), chord[9]
        assert chord[10] >> NotePitch('E', '', 1), chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> NotePitch('G', '', 1), chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> NotePitch('B', 'b', 1), chord[14]
        assert chord[15] >> NotePitch('C', '', 2), chord[15]
