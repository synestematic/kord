'''
using relative imports in my modules means that I can NOT run them directly
cuz I need to import the parent beforehand => use this script to run tests.py

https://docs.python.org/3/library/operator.html
https://stackoverflow.com/questions/39754808/overriding-not-operator-in-python

TDD:
    * write test
    * fail test RED
    * write code
    * pass test GREEN
    * remove duplication REFACTOR
    * pass test

'''

from kord.tests import *

if __name__ == '__main__':
    try:
        unittest.main()
    except KeyboardInterrupt:
        print()
