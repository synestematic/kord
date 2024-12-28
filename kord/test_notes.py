import unittest

from .notes import NotePitch

from .notes.constants import D_FLAT_3, C_SHARP_5, C_SHARP_3

from .errors import InvalidNote

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

        (NotePitch('C', 'b', 3), NotePitch('B', '#', 3)),

        (NotePitch('C', 'b', 3), NotePitch('B', '#', 3)),

        (NotePitch('E', 'b', 5), NotePitch('D', '#', 4)),

        (NotePitch('B', '', 5), NotePitch('C', 'b', 4)),

        (NotePitch('E', '#', 3), NotePitch('F', '', 4)),


        (NotePitch('B', 'b'), NotePitch('C', 'bb')),
        (NotePitch('A', '#'), NotePitch('C', 'bb')),

        (NotePitch('B'     ), NotePitch('C', 'b')),
        (NotePitch('A', '##'), NotePitch('C', 'b')),

        (NotePitch('B', '#'), NotePitch('C', '')),
        (NotePitch('B', '#'), NotePitch('D', 'bb')),

        (NotePitch('B', '##'), NotePitch('C', '#')),
        (NotePitch('B', '##'), NotePitch('D', 'b')),


        # these should eval False OK
        (NotePitch('A', '#'), NotePitch('B', 'b', 4)),
        (NotePitch('A', '##'), NotePitch('B', '', 4)),
        (NotePitch('C', ''), NotePitch('D', 'bb', 4)),
        (NotePitch('C', '#'), NotePitch('D', 'b', 4)),
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
