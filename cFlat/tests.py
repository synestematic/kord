import unittest

from instruments import *
from keys import *
from notes import *
from errors import *

from uuid import uuid4

class ChromaticKeyTestCase(unittest.TestCase):

    def setUp(self):
        self.key = ChromaticKey('C')

    # def testDegree1(self):
    #     assert self.key.degree(1) == self.key[1], 'degree() != __get_item__()'
    #     assert self.key.degree(1).is_a('C'), 'diocane'


    def testGen(self):
        for i, note in enumerate(self.key.scale()):
            print(note)
        # print(self.key)


# class DiatonicKeyTestCase(unittest.TestCase):

#     def setUp(self):
#         self.key = DiatonicKey('C')

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
