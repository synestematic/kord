from bestia.output import echo

from notes import *
from scales import *
from tunings import *

from tests import *

DISPLAY_FRETS = recommended_frets()
VERBOSE = 1

if __name__ == '__main__':

    try:

        sc = MajorScale('B')
        echo(sc)

        for d in sc.scale(5, start=Note('E', 4)):
            print(d)

        # exit()

        guitar_std = Tuning(
            # Note('E', 3),
            Note('A', 'b', 10),     # why is this displaying diesei? create a test for this...
            Note('B', 3),
            Note('G', 3),
            Note('D', 3),
            Note('A', 2),
            Note('E', 2),
            # Note('B', 1),
        )

        guitar_std.fretboard(
            scale= MajorScale('B'),
            frets=DISPLAY_FRETS,  # frets is NOT Notes
            verbose=VERBOSE,
        )

        ukulele = Tuning(
            Note('A', 3),
            Note('E', 3),
            Note('C', 3),
            Note('G', 3),
        )
        ukulele.fretboard(
            scale= MajorScale('C'),
            frets=DISPLAY_FRETS,
            verbose=VERBOSE,
        )

        ## Strings......
        c = Note('C', 5)
        s1 = String(*c)
        s1.scale = MajorScale(*c)
        echo(s1)

    except KeyboardInterrupt:
        echo()


# gfb E --chord 7

# seventh chords
# 7
# M7
# m7
# D7
# d7

# gfb G --scale M

# scales
# major
# minor
