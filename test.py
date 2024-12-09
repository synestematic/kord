""" TDD:
    * write test
    * fail test RED
    * write code
    * pass test GREEN
    * remove duplication REFACTOR
    * pass test
"""

import unittest

# from kord.test_keys import *
# from kord.test_notes import *
from kord.test_parsers import *


if __name__ == '__main__':
    try:
        unittest.main()
    except KeyboardInterrupt:
        print()
