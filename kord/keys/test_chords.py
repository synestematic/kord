import unittest

from .chords import (
    Chord,
    PowerChord,
    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    DiminishedSeventhChord, HalfDiminishedSeventhChord,
    DominantNinthChord, DominantMinorNinthChord,
    MajorNinthChord, MinorNinthChord,
    MajorSixthChord, MinorSixthChord,
    SuspendedFourChord, SuspendedTwoChord,
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

    def testChordDegrees(self):
        chord = Chord(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testMajorTriadDegrees(self):
        chord = MajorTriad(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testMinorTriadDegrees(self):
        chord = MinorTriad(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testAugmentedTriadDegrees(self):
        chord = AugmentedTriad(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testDiminishedTriadDegrees(self):
        chord = DiminishedTriad(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testMajorSixthChordChordDegrees(self):
        chord = MajorSixthChord(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testMinorSixthChordDegrees(self):
        chord = MinorSixthChord(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testMajorNinthChordDegrees(self):
        chord = MajorNinthChord(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testMinorNinthChordDegrees(self):
        chord = MinorNinthChord(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testDominantNinthChordDegrees(self):
        chord = DominantNinthChord(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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


    def testDominantMinorNinthChordDegrees(self):
        chord = DominantMinorNinthChord(*C)
        # print(chord.all_degrees())
        # print(chord.intervals)
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

