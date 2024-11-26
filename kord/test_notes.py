import unittest

from .notes import *


class NoteEqualityTest(unittest.TestCase):

    DANGEROUS_NON_EQUALS = (
        # ''' Used mainly to test B#, Cb, etc... '''

        (MusicNote('C', 'b', 3), MusicNote('B', '#', 3)),

        (MusicNote('C', 'b', 3), MusicNote('B', '#', 3)),

        (MusicNote('E', 'b', 5), MusicNote('D', '#', 4)),

        (MusicNote('B', '', 5), MusicNote('C', 'b', 4)),

        (MusicNote('E', '#', 3), MusicNote('F', '', 4)),


        (MusicNote('B', 'b'), MusicNote('C', 'bb')),
        (MusicNote('A', '#'), MusicNote('C', 'bb')),

        (MusicNote('B'     ), MusicNote('C', 'b')),
        (MusicNote('A', '##'), MusicNote('C', 'b')),

        (MusicNote('B', '#'), MusicNote('C', '')),
        (MusicNote('B', '#'), MusicNote('D', 'bb')),

        (MusicNote('B', '##'), MusicNote('C', '#')),
        (MusicNote('B', '##'), MusicNote('D', 'b')),


        # these should eval False OK
        (MusicNote('A', '#'), MusicNote('B', 'b', 4)),
        (MusicNote('A', '##'), MusicNote('B', '', 4)),
        (MusicNote('C', ''), MusicNote('D', 'bb', 4)),
        (MusicNote('C', '#'), MusicNote('D', 'b', 4)),
    )

    def setUp(self):
        print()

    def testNotEnharmonic(self):
        for note_pair in self.DANGEROUS_NON_EQUALS:
            assert not note_pair[0] >> note_pair[1], (note_pair[0], note_pair[1])
            assert note_pair[0] - note_pair[1] != 0, (note_pair[0], note_pair[1])


    def testAreEnharmonic(self):
        ''' checks note_pairs in enharmonic rows for different types of enharmonic equality '''
        for note_pair in EnharmonicMatrix:

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
        Cs5 = MusicNote('C', '#', 5)
        Db3 = MusicNote('D', 'b', 3)
        Cs3 = MusicNote('C', '#', 3)
        assert Cs3 ** Cs5      # loosest equality
        assert Db3 == Cs3      # enhamonic notes
        assert not Db3 >> Cs3  # enh note
        assert not Cs3 >> Db3  # enh note

        # ** same note, ignr oct
        # == enhr note, same oct
        # >> same note, same oct

        # // enhr note, ignr oct   do I need to implement this operator ?

