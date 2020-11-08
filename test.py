""" TDD:
    * write test
    * fail test RED
    * write code
    * pass test GREEN
    * remove duplication REFACTOR
    * pass test
"""

from kord.tests import *

if __name__ == '__main__':
    try:
        unittest.main()
    except KeyboardInterrupt:
        print()
