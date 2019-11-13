import unittest

from instruments import *
from keys import *
from notes import *
from errors import *

from uuid import uuid4

class NoteEqualityTestCase(unittest.TestCase):

    DANGEROUS_NON_EQUALS = (
        # ''' Used mainly to test B#, Cd, etc... '''

        (Note('C', 'b', 3), Note('B', '#', 3)),

        (Note('C', 'b', 3), Note('B', '#', 3)),

        (Note('E', 'b', 5), Note('D', '#', 4)),

        (Note('B', '', 5), Note('C', 'b', 4)),

        (Note('E', '#', 3), Note('F', '', 4)),


        (Note('B', 'b'), Note('C', 'bb')),
        (Note('A', '#'), Note('C', 'bb')),

        (Note('B'     ), Note('C', 'b')),
        (Note('A', '##'), Note('C', 'b')),

        (Note('B', '#'), Note('C', '')),
        (Note('B', '#'), Note('D', 'bb')),

        (Note('B', '##'), Note('C', '#')),
        (Note('B', '##'), Note('D', 'b')),


        # these should eval False OK
        (Note('A', '#'), Note('B', 'b', 4)),
        (Note('A', '##'), Note('B', '', 4)),
        (Note('C', ''), Note('D', 'bb', 4)),
        (Note('C', '#'), Note('D', 'b', 4)),
    )

    def testNotEnharmonic(self):
        for note_pair in self.DANGEROUS_NON_EQUALS:
            assert note_pair[0] != note_pair[1]


    def testAreEnharmonic(self):
        ''' checks note_pairs in enharmonic rows
            for different types of equality '''
        for note_pair in EnharmonicMatrix:
            assert note_pair[0] == note_pair[1]
            assert note_pair[0] -  note_pair[1] == 0


# class ChromaticKeyTestCase(unittest.TestCase):

#     def setUp(self):
#         self.c_chromatic = ChromaticKey('C')

#     # def testDegree1(self):
#     #     assert self.c_chromatic.degree(1) == self.c_chromatic[1], 'degree() != __get_item__()'
#     #     assert self.c_chromatic.degree(1).is_a('C'), 'diocane'

    # def testScaleGenerator(self):
#         for i, note in enumerate(self.c_chromatic.scale()):
#             print(note, end=' ')
#         print()
#         print(self.c_chromatic)


class MajorKeysTestCase(unittest.TestCase):

    def setUp(self):
        self.intervals = 7
        self.c_major = MajorKey('C')
        self.b_major = MajorKey('B')            # 5 sharps
        self.d_flat_major = MajorKey('D', 'b')  # 5 flats


    def testCMajorScaleGenerator(self):

        octaves_to_test = 18
        notes_to_test = octaves_to_test * self.intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.c_major.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('C', '', 0), note
            elif i == 2:
                assert note.is_a('D', '', 0), note
            elif i == 3:
                assert note.is_a('E', '', 0), note
            elif i == 4:
                assert note.is_a('F', '', 0), note
            elif i == 5:
                assert note.is_a('G', '', 0), note
            elif i == 6:
                assert note.is_a('A', '', 0), note
            elif i == 7:
                assert note.is_a('B', '', 0), note
            elif i == 8:
                assert note.is_a('C', '', 1), note
            elif i == 9:
                assert note.is_a('D', '', 1), note
            elif i == 10:
                assert note.is_a('E', '', 1), note
            elif i == 11:
                assert note.is_a('F', '', 1), note
            elif i == 12:
                assert note.is_a('G', '', 1), note
            elif i == 13:
                assert note.is_a('A', '', 1), note
            elif i == 14:
                assert note.is_a('B', '', 1), note
            elif i == 15:
                assert note.is_a('C', '', 2), note
            # ..............................
            elif i == 64:
                assert note.is_a('C', '', 9), note
            elif i == 65:
                assert note.is_a('D', '', 9), note
            elif i == 66:
                assert note.is_a('E', '', 9), note
            elif i == 67:
                assert note.is_a('F', '', 9), note
            elif i == 68:
                assert note.is_a('G', '', 9), note
            elif i == 69:
                assert note.is_a('A', '', 9), note
            elif i == 70:
                assert note.is_a('B', '', 9), note
            elif i == 71:
                assert note.is_a('C', '', 10), note
            # ..............................
            elif i == 120:
                assert note.is_a('C', '', 17), note
            elif i == 121:
                assert note.is_a('D', '', 17), note
            elif i == 122:
                assert note.is_a('E', '', 17), note
            elif i == 123:
                assert note.is_a('F', '', 17), note
            elif i == 124:
                assert note.is_a('G', '', 17), note
            elif i == 125:
                assert note.is_a('A', '', 17), note
            elif i == 126:
                assert note.is_a('B', '', 17), note
            elif i == 127:
                assert note.is_a('C', '', 18), note


    def testBMajorScaleGenerator(self):

        octaves_to_test = 18
        notes_to_test = octaves_to_test * self.intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.b_major.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('B', '', 0), note
            elif i == 2:
                assert note.is_a('C', '#', 1), note
            elif i == 3:
                assert note.is_a('D', '#', 1), note
            elif i == 4:
                assert note.is_a('E', '', 1), note
            elif i == 5:
                assert note.is_a('F', '#', 1), note
            elif i == 6:
                assert note.is_a('G', '#', 1), note
            elif i == 7:
                assert note.is_a('A', '#', 1), note
            elif i == 8:
                assert note.is_a('B', '', 1), note
            elif i == 9:
                assert note.is_a('C', '#', 2), note
            elif i == 10:
                assert note.is_a('D', '#', 2), note
            elif i == 11:
                assert note.is_a('E', '', 2), note
            elif i == 12:
                assert note.is_a('F', '#', 2), note
            elif i == 13:
                assert note.is_a('G', '#', 2), note
            elif i == 14:
                assert note.is_a('A', '#', 2), note
            elif i == 15:
                assert note.is_a('B', '', 2), note
            elif i == 16:
                assert note.is_a('C', '#', 3), note
            # ..............................
            elif i == 64:
                assert note.is_a('B', '', 9), note
            elif i == 65:
                assert note.is_a('C', '#', 10), note
            elif i == 66:
                assert note.is_a('D', '#', 10), note
            elif i == 67:
                assert note.is_a('E', '', 10), note
            elif i == 68:
                assert note.is_a('F', '#', 10), note
            elif i == 69:
                assert note.is_a('G', '#', 10), note
            elif i == 70:
                assert note.is_a('A', '#', 10), note
            elif i == 71:
                assert note.is_a('B', '', 10), note
            # ..............................
            elif i == 120:
                assert note.is_a('B', '', 17), note
            elif i == 121:
                assert note.is_a('C', '#', 18), note
            elif i == 122:
                assert note.is_a('D', '#', 18), note
            elif i == 123:
                assert note.is_a('E', '', 18), note
            elif i == 124:
                assert note.is_a('F', '#', 18), note
            elif i == 125:
                assert note.is_a('G', '#', 18), note
            elif i == 126:
                assert note.is_a('A', '#', 18), note
            elif i == 127:
                assert note.is_a('B', '', 18), note



    def testDFlatMajorScaleGenerator(self):

        octaves_to_test = 18
        notes_to_test = octaves_to_test * self.intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.d_flat_major.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('D', 'b', 0), note
            elif i == 2:
                assert note.is_a('E', 'b', 0), note
            elif i == 3:
                assert note.is_a('F', '', 0), note
            elif i == 4:
                assert note.is_a('G', 'b', 0), note
            elif i == 5:
                assert note.is_a('A', 'b', 0), note
            elif i == 6:
                assert note.is_a('B', 'b', 0), note
            elif i == 7:
                assert note.is_a('C', '', 1), note
            elif i == 8:
                assert note.is_a('D', 'b', 1), note
            elif i == 9:
                assert note.is_a('E', 'b', 1), note
            elif i == 10:
                assert note.is_a('F', '', 1), note
            elif i == 11:
                assert note.is_a('G', 'b', 1), note
            elif i == 12:
                assert note.is_a('A', 'b', 1), note
            elif i == 13:
                assert note.is_a('B', 'b', 1), note
            elif i == 14:
                assert note.is_a('C', '', 2), note
            elif i == 15:
                assert note.is_a('D', 'b', 2), note
            elif i == 16:
                assert note.is_a('E', 'b', 2), note
            # ..............................
            elif i == 64:
                assert note.is_a('D', 'b', 9), note
            elif i == 65:
                assert note.is_a('E', 'b', 9), note
            elif i == 66:
                assert note.is_a('F', '', 9), note
            elif i == 67:
                assert note.is_a('G', 'b', 9), note
            elif i == 68:
                assert note.is_a('A', 'b', 9), note
            elif i == 69:
                assert note.is_a('B', 'b', 9), note
            elif i == 70:
                assert note.is_a('C', '', 10), note
            elif i == 71:
                assert note.is_a('D', 'b', 10), note
            elif i == 72:
                assert note.is_a('E', 'b', 10), note
            # ..............................
            elif i == 120:
                assert note.is_a('D', 'b', 17), note
            elif i == 121:
                assert note.is_a('E', 'b', 17), note
            elif i == 122:
                assert note.is_a('F', '', 17), note
            elif i == 123:
                assert note.is_a('G', 'b', 17), note
            elif i == 124:
                assert note.is_a('A', 'b', 17), note
            elif i == 125:
                assert note.is_a('B', 'b', 17), note
            elif i == 126:
                assert note.is_a('C', '', 18), note
            elif i == 127:
                assert note.is_a('D', 'b', 18), note


    def testDegreeMethod(self):
        assert self.c_major.degree(1) == self.c_major[1], 'degree() != __get_item__()'
        assert self.c_major.degree(1).is_a('C'), 'diocane'


if __name__ == '__main__':
    # TDD
    # write test
    # fail test RED
    # write code
    # pass test GREEN
    # remove duplication REFACTOR
    # pass test
    unittest.main()
