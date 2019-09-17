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
    parser.add_argument(
        '-s', '--scale',
        help = 'scale to display',
    )
    parser.add_argument(
        '-c', '--chord',
        help = 'chord to display',
    )



    return parser.parse_args()


if __name__ == '__main__':

    argv = parse_arguments()
    DISPLAY_FRETS = argv.frets
    VERBOSE = argv.verbosity
    # try:

    print()
    # echo(
    #     PhrygianMode('A')
    # )

    # c = MajorKey('C')
    # echo(
    #     c.degree(24)
    # )
    # echo(
    #     c
    # )
    # echo(
    #     c.degree(1)
    # )
    
    # exit()

    # k = MinorKey('A')
    # for n in k.thirteenth():
    #     echo(n)
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
        key= DorianMode('A'),
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









    # except KeyboardInterrupt:
    #     echo()

    # except Exception as x:
    #     # print("Unexpected error:", sys.exc_info()[0])
    #     # print(31341323231)
    #     raise x


    # finally:
    #     exit(0)


# BUGS TO FIX:



# gfb E --chord C7

# seventh chords
# 7
# M7
# m7
# D7
# d7

# 9


# gfb G --scale M

# scales
# major
# lydian
# mixo

# minor
# aeolian

