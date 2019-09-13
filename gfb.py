from bestia.output import echo

from tests import *

DISPLAY_FRETS = 12
VERBOSE = 1

if __name__ == '__main__':

    try:
                
        n = Note('D', '')
        sn = Note('F', '', 2)
        # sn = None

        # sc = MajorScale(n)
        sc = ChromaticScale(n)
        echo(sc)

        for d in sc.scale(notes=10, all=1, start=sn):
            echo(d, 'cyan', mode='raw')
            echo('  ', mode='raw')
        print()

        guitar_std = Tuning(
            string1=Note('E', 4),
            string2=Note('B', 3),
            string3=Note('G', 3),
            string4=Note('D', 3),
            string5=Note('A', 2),
            string6=Note('E', 2),
            # string7=Note('B', 2),
        )

        guitar_std.fretboard(
            scale= MajorScale(
                Note('G', '')
            ),
            frets=DISPLAY_FRETS,
        )

        # ukulele = Tuning(
        #     string1=Note('E', 3),
        #     string2=Note('A', 3),
        #     string3=Note('C', 3),
        #     string4=Note('G', 3),
        # )
        # ukulele.fretboard(
        #     scale= MajorScale(
        #         Note('C')
        #     ),
        #     frets=DISPLAY_FRETS,
        #     verbose=2,
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
