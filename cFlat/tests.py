import unittest

from instruments import *
from keys import *
from notes import *
from errors import *

from uuid import uuid4

# class ChromaticKeyTestCase(unittest.TestCase):

#     def setUp(self):
#         self.key = ChromaticKey('C')

#     # def testDegree1(self):
#     #     assert self.key.degree(1) == self.key[1], 'degree() != __get_item__()'
#     #     assert self.key.degree(1).is_a('C'), 'diocane'


#     def testGen(self):
#         for i, note in enumerate(self.key.scale()):
#             print(note, end=' ')
#         print()
#         print(self.key)


class DiatonicKeysTestCase(unittest.TestCase):

    def setUp(self):
        self.c_major = MajorKey('C')


    def testGen(self):

        for i, note in enumerate(self.c_major.scale()):
            print(note, end=' ')
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

        print()
        # print(self.c_major)


#     def testDegree1(self):
#         assert self.key.degree(1) == self.key[1], 'degree() != __get_item__()'
#         assert self.key.degree(1).is_a('C'), 'diocane'



# TDD
# write test
# fail test RED
# write code
# pass test GREEN
# remove duplication REFACTOR
# pass test

if __name__ == '__main__':
    unittest.main()
