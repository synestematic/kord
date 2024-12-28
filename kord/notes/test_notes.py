import unittest

from . import NotePitch

from .constants import (
    F_4, B_4, B_5,
    C_FLAT_3, C_FLAT_4, D_FLAT_4, B_FLAT_4, E_FLAT_5, D_FLAT_3, 
    E_SHARP_3, B_SHARP_3, D_SHARP_4, C_SHARP_5, C_SHARP_3,
    D_DOUBLE_FLAT_4,
)

from ..errors import InvalidNote

__all__ = [
    'TestInvalidNotes',
    'NoteEqualityTest',
]


class TestInvalidNotes(unittest.TestCase):

    def testInvalidChars(self):
        self.assertRaises(
            InvalidNote, lambda : NotePitch('Y')
        )


class NoteEqualityTest(unittest.TestCase):

    DANGEROUS_NON_EQUALS = (
        # ''' Used mainly to test B#, Cb, etc... '''

        (C_FLAT_3, B_SHARP_3),
        (E_FLAT_5, D_SHARP_4),

        (B_5, C_FLAT_4),

        (E_SHARP_3, F_4),


        (NotePitch('B', 'b'), NotePitch('C', 'bb')),
        (NotePitch('A', '#'), NotePitch('C', 'bb')),

        (NotePitch('B'     ), NotePitch('C', 'b')),
        (NotePitch('A', '##'), NotePitch('C', 'b')),

        (NotePitch('B', '#'), NotePitch('C', '')),
        (NotePitch('B', '#'), NotePitch('D', 'bb')),

        (NotePitch('B', '##'), NotePitch('C', '#')),
        (NotePitch('B', '##'), NotePitch('D', 'b')),


        # these should eval False OK
        (NotePitch('A', '#'), B_FLAT_4),
        (NotePitch('A', '##'), B_4),
        (NotePitch('C', ''), D_DOUBLE_FLAT_4),
        (NotePitch('C', '#'), D_FLAT_4),
    )

    def setUp(self):
        print()

    def testNotEnharmonic(self):
        for note_pair in self.DANGEROUS_NON_EQUALS:
            assert not note_pair[0] >> note_pair[1], (note_pair[0], note_pair[1])
            assert note_pair[0] - note_pair[1] != 0, (note_pair[0], note_pair[1])


    def testAreEnharmonic(self):
        ''' checks note_pairs in enharmonic rows for different types of enharmonic equality '''
        for note_pair in NotePitch.EnharmonicMatrix():

            # PASS ENHARMONIC EQUALITY
            assert note_pair[0] == note_pair[1], (note_pair[0], note_pair[1])

            # DO NOT PASS NOTE EQUALITY
            assert not note_pair[0] >> note_pair[1], (note_pair[0], note_pair[1])
            assert not note_pair[0] ** note_pair[1], (note_pair[0], note_pair[1])

            # CHECK DELTA_ST == 0
            assert not note_pair[0] < note_pair[1], (note_pair[0], note_pair[1])
            assert not note_pair[0] > note_pair[1], (note_pair[0], note_pair[1])
            assert note_pair[0] <= note_pair[1], (note_pair[0], note_pair[1])
            assert note_pair[0] >= note_pair[1], (note_pair[0], note_pair[1])
            assert note_pair[0] - note_pair[1] == 0, (note_pair[0], note_pair[1])


    def testEnharmonicOperators(self):
        ''' '''
        print('Testing enharmonic operators')
        assert C_SHARP_3 ** C_SHARP_5     # loosest equality
        assert C_SHARP_3 == D_FLAT_3      # enhamonic notes
        assert not D_FLAT_3 >> C_SHARP_3  # enh note
        assert not C_SHARP_3 >> D_FLAT_3  # enh note

        # ** same note, ignr oct
        # == enhr note, same oct
        # >> same note, same oct

        # // enhr note, ignr oct   do I need to implement this operator ?
