import unittest

from instruments import *
from keys import *
from notes import *
from errors import *

from uuid import uuid4

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


class DiatonicKeysTestCase(unittest.TestCase):

    def setUp(self):
        self.intervals = 7
        self.c_major = MajorKey('C')
        self.b_major = MajorKey('B')


    def testCMajorScaleGenerator(self):

        octaves_to_test = 18
        notes_to_test = octaves_to_test * self.intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.c_major.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            # print(note, end=' ')
            i += 1
            if i == 1:
                assert note.is_a('C', '', 0)
            elif i == 2:
                assert note.is_a('D', '', 0)
            elif i == 3:
                assert note.is_a('E', '', 0)
            elif i == 4:
                assert note.is_a('F', '', 0)
            elif i == 5:
                assert note.is_a('G', '', 0)
            elif i == 6:
                assert note.is_a('A', '', 0)
            elif i == 7:
                assert note.is_a('B', '', 0)
            # ..............................
            elif i == 8:
                assert note.is_a('C', '', 1)
            elif i == 9:
                assert note.is_a('D', '', 1)
            elif i == 10:
                assert note.is_a('E', '', 1)
            elif i == 11:
                assert note.is_a('F', '', 1)
            elif i == 12:
                assert note.is_a('G', '', 1)
            elif i == 13:
                assert note.is_a('A', '', 1)
            elif i == 14:
                assert note.is_a('B', '', 1)
            # ..............................
            elif i == 15:
                assert note.is_a('C', '', 2)
            # ..............................
            # ..............................
            elif i == 64:
                assert note.is_a('C', '', 9)
            elif i == 65:
                assert note.is_a('D', '', 9)
            elif i == 66:
                assert note.is_a('E', '', 9)
            elif i == 67:
                assert note.is_a('F', '', 9)
            elif i == 68:
                assert note.is_a('G', '', 9)
            elif i == 69:
                assert note.is_a('A', '', 9)
            elif i == 70:
                assert note.is_a('B', '', 9)
            # ..............................
            elif i == 71:
                assert note.is_a('C', '', 10)
            # ..............................
            # ..............................
            elif i == 120:
                assert note.is_a('C', '', 17)
            elif i == 121:
                assert note.is_a('D', '', 17)
            elif i == 122:
                assert note.is_a('E', '', 17)
            elif i == 123:
                assert note.is_a('F', '', 17)
            elif i == 124:
                assert note.is_a('G', '', 17)
            elif i == 125:
                assert note.is_a('A', '', 17)
            elif i == 126:
                assert note.is_a('B', '', 17)
            # ..............................
            elif i == 127:
                assert note.is_a('C', '', 18)


    def testDegreeMethod(self):
        assert self.c_major.degree(1) == self.c_major[1], 'degree() != __get_item__()'
        assert self.c_major.degree(1).is_a('C'), 'diocane'


# TDD
# write test
# fail test RED
# write code
# pass test GREEN
# remove duplication REFACTOR
# pass test

if __name__ == '__main__':
    unittest.main()
