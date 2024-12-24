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


    def testMajorChordDegrees(self):
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


    def testMinorChordDegrees(self):
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
