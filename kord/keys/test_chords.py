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

    def testChordNotes(self):
        c_chord = MajorTriad(*C)
        print(c_chord.all_degrees())
        print(c_chord.intervals)

        # THSE 2 KEEP ITERATING NONES...
        c_chord = Chord(*C)
        print(c_chord.all_degrees())
        print(c_chord.intervals)

        c_chord = DominantMinorNinthChord(*C)
        print(c_chord._parent_scale_root_offset())
        # print(c_chord[1])
        # print(c_chord[3])
        # print(c_chord[5])
        # print(c_chord[7])
        # print(c_chord[9])

        # for n in c_chord:
        #     print(n)
            # input('----')