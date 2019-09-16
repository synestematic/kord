from argparse import ArgumentParser
from bestia.output import echo

from notes import *
from keys import *
from tunings import *

from tests import *

def parse_arguments():
    parser = ArgumentParser(
        description = 'guitar fretboard',
    )
    parser.add_argument(
        '-f', '--frets',
        help = 'number of frets to display',
        type = int,
        default=recommended_frets()
    )
    parser.add_argument(
        '-v', '--verbosity',
        help = 'amount of verbosity',
        type = int,
        default=1
    )
    return parser.parse_args()


if __name__ == '__main__':

    argv = parse_arguments()
    DISPLAY_FRETS = argv.frets
    VERBOSE = argv.verbosity
    try:

        k = MinorKey('A')
        for n in k.thirteenth():
            echo(n)
        # exit()
        # broken, not increasing last octave....

        print()
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
            key= MajorKey('C'),
            frets=DISPLAY_FRETS,
            verbose=VERBOSE,
        )

        print()
        ukulele = Tuning(
            Note('A', 3),
            Note('E', 3),
            Note('C', 3),
            Note('G', 3),
        )
        ukulele.fretboard(
            key= MajorKey('F'),
            frets=DISPLAY_FRETS,
            verbose=VERBOSE,
        )

        ## Strings......
        # c = Note('F', 5)
        # s1 = String(*c)
        # s1.key = MajorKey(*c)
        # echo(s1)

    except KeyboardInterrupt:
        echo()

    finally:
        exit(0)


# BUGS TO FIX:



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
