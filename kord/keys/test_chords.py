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

from ..notes.constants import (
    A_0, A_1, A_2, B_0, B_1, C_0, C_1, C_2, C_3, D_0, D_1, E_0, E_1, F_0, F_1, G_0, G_1,
    E_FLAT_0, E_FLAT_1, B_FLAT_0, B_FLAT_1, G_FLAT_0, G_FLAT_1, D_FLAT_0, D_FLAT_1,
    G_SHARP_0, G_SHARP_1,
    B_DOUBLE_FLAT_0, B_DOUBLE_FLAT_1,
)

from ..errors import InvalidNote, InvalidAlteration, InvalidOctave, InvalidChord

__all__ = [
    'ChordTest',
]


class ChordTest(unittest.TestCase):

    def testPowerChord(self):
        chord = PowerChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert not chord[3] , chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert not chord[10] , chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testSuspended4Chord(self):
        chord = Suspended4Chord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert not chord[3] , chord[3]
        assert chord[4] >> F_0, chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert not chord[10] , chord[10]
        assert chord[11] >> F_1, chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testSuspended2Chord(self):
        chord = Suspended2Chord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_0, chord[2]
        assert not chord[3] , chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_1, chord[9]
        assert not chord[10] , chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMajorTriad(self):
        chord = MajorTriad(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMinorTriad(self):
        chord = MinorTriad(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testAugmentedTriad(self):
        chord = AugmentedTriad(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_SHARP_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_SHARP_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testDiminishedTriad(self):
        chord = DiminishedTriad(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_FLAT_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_FLAT_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMajorSixthChordChord(self):
        chord = MajorSixthChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert chord[6] >> A_0, chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert chord[13] >> A_1, chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMinorSixthChord(self):
        chord = MinorSixthChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert chord[6] >> A_0, chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert chord[13] >> A_1, chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMajorSeventhChord(self):
        chord = MajorSeventhChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_1, chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMinorSeventhChord(self):
        chord = MinorSeventhChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_FLAT_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_FLAT_1, chord[14]
        assert chord[15] >> C_2, chord[15]


    def testDominantSeventhChord(self):
        chord = DominantSeventhChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_FLAT_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_FLAT_1, chord[14]
        assert chord[15] >> C_2, chord[15]


    def testHalfDiminishedSeventhChord(self):
        chord = HalfDiminishedSeventhChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_FLAT_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_FLAT_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_FLAT_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_FLAT_1, chord[14]
        assert chord[15] >> C_2, chord[15]


    def testDiminishedSeventhChord(self):
        chord = DiminishedSeventhChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert not chord[2] , chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_FLAT_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_DOUBLE_FLAT_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert not chord[9] , chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_FLAT_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_DOUBLE_FLAT_1, chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMajorAdd9Chord(self):
        chord = MajorAdd9Chord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_0, chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_1, chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMinorAdd9Chord(self):
        chord = MinorAdd9Chord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_0, chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_1, chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testAugmentedAdd9Chord(self):
        chord = AugmentedAdd9Chord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_0, chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_SHARP_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_1, chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_SHARP_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testDiminishedAdd9Chord(self):
        chord = DiminishedAdd9Chord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_0, chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_FLAT_0, chord[5]
        assert not chord[6] , chord[6]
        assert not chord[7] , chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_1, chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_FLAT_1, chord[12]
        assert not chord[13] , chord[13]
        assert not chord[14] , chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMajorNinthChord(self):
        chord = MajorNinthChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_0, chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_1, chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_1, chord[14]
        assert chord[15] >> C_2, chord[15]


    def testMinorNinthChord(self):
        chord = MinorNinthChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_0, chord[2]
        assert chord[3] >> E_FLAT_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_FLAT_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_1, chord[9]
        assert chord[10] >> E_FLAT_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_FLAT_1, chord[14]
        assert chord[15] >> C_2, chord[15]


    def testDominantNinthChord(self):
        chord = DominantNinthChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_0, chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_FLAT_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_1, chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_FLAT_1, chord[14]
        assert chord[15] >> C_2, chord[15]


    def testDominantMinorNinthChord(self):
        chord = DominantMinorNinthChord(*C_3)
        assert not chord[0] , chord[0]
        assert chord[1] >> C_0, chord[1]
        assert chord[2] >> D_FLAT_0, chord[2]
        assert chord[3] >> E_0, chord[3]
        assert not chord[4] , chord[4]
        assert chord[5] >> G_0, chord[5]
        assert not chord[6] , chord[6]
        assert chord[7] >> B_FLAT_0, chord[7]
        assert chord[8] >> C_1, chord[8]
        assert chord[9] >> D_FLAT_1, chord[9]
        assert chord[10] >> E_1, chord[10]
        assert not chord[11] , chord[11]
        assert chord[12] >> G_1, chord[12]
        assert not chord[13] , chord[13]
        assert chord[14] >> B_FLAT_1, chord[14]
        assert chord[15] >> C_2, chord[15]
