from bestia.output import echo

from notes import *
from scales import *
from tunings import *

from tests import *

DISPLAY_FRETS = recommended_frets()
# DISPLAY_FRETS = 3
VERBOSE = 1

if __name__ == '__main__':

    try:
        guitar_std = Tuning(
            Note('E', 3),
            Note('B', 3),
            Note('G', 3),
            Note('D', 3),
            Note('A', 2),
            Note('E', 2),
            # Note('B', 1),
        )

        guitar_std.fretboard(
            scale= MajorScale('C'),
            frets=DISPLAY_FRETS,  # frets is NOT Notes
            verbose=VERBOSE,
        )

        # ukulele = Tuning(
        #     Note('A', 3),
        #     Note('E', 3),
        #     Note('C', 3),
        #     Note('G', 3),
        # )
        # ukulele.fretboard(
        #     scale= MajorScale('C'),
        #     frets=DISPLAY_FRETS,
        #     verbose=VERBOSE,
        # )

        ## Strings......
        # c = Note('F', 5)
        # s1 = String(*c)
        # s1.scale = MajorScale(*c)
        # echo(s1)

    except KeyboardInterrupt:
        echo()


# BUGS TO FIX:
    # fret notes are not yielded notes...




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
