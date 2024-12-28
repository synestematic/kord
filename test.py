""" TDD:
    * write test
    * fail test RED
    * write code
    * pass test GREEN
    * remove duplication REFACTOR
    * pass test
"""

import unittest

from kord.keys.test_scales import *
from kord.keys.test_chords import *
from kord.notes.test_notes import *

from kord.parsers.test_chord_parser import *
from kord.parsers.test_pitch_parser import *


if __name__ == '__main__':
    try:
        unittest.main()
    except KeyboardInterrupt:
        print()
