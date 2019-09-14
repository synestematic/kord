from bestia.output import echo

from tests import *

DISPLAY_FRETS = 14
VERBOSE = 1

if __name__ == '__main__':

    try:
        guitar_std = Tuning(
            Note('E', 4),
            Note('B', 3),
            Note('G', 3),
            Note('D', 3),
            Note('A', 2),
            Note('E', 2),
            # Note('B', 1),
        )

        guitar_std.fretboard(
            # open strings for 3, 4, 5 are wrong
            scale= MajorScale(
                Note('A', '')
            ),
            frets=DISPLAY_FRETS,
            verbose=VERBOSE,
        )

        # ukulele = Tuning(
        #     Note('A', 3),
        #     Note('E', 3),
        #     Note('C', 3),
        #     Note('G', 3),
        # )
        # ukulele.fretboard(
        #     scale= MajorScale(
        #         Note('C')
        #     ),
        #     frets=DISPLAY_FRETS,
        #     verbose=VERBOSE,
        # )

        ### Strings......
        # c = Note('C', 5)
        # s1 = String(c)
        # s1.set_scale(
        #     MajorScale(c)
        # )
        # echo(s1)

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
