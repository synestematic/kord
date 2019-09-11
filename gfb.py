from bestia.output import echo

from notes import *
from scales import *
from tunings import *

DISPLAY_FRETS = 3
VERBOSE = 1

if __name__ == '__main__':

    try:
        c = Note('c')
        ebb = Note('E', 'bb')

        c_major = MajorScale(c)
        ebb_chrom = ChromaticScale(ebb)
        # for n in c_major.scale(20, start_note=ebb):
        #     echo(n, 'cyan')

        guitar_std = Tuning(
            string1=Note('E', 4),
            string2=Note('B', 3),
            string3=Note('G', 3),
            string4=Note('D', 3),
            string5=Note('A', 2),
            string6=Note('E', 2),
            # string7=Note('B', 2),
        )
        guitar_std.fretboard(frets=DISPLAY_FRETS)
        # guitar_std.fretboard(scale=c_major, frets=DISPLAY_FRETS)

        # ukulele_std = Tuning(
        #     string1=Note('E', 3),
        #     string2=Note('A', 3),
        #     string3=Note('C', 3),
        #     string4=Note('G', 3),
        # )
        # ukulele_std.fretboard(frets=DISPLAY_FRETS)


        mel = MelodicMinorScale(Note('A', ''))
        e = Note('E', 3)
        # # e = None
        for n in mel.scale(13, start_note=e):
        # for n in mel.scale(13):
            echo(n, 'cyan')

        # echo(mel)
        # echo()


        # c = Note('C', 3)
        # s1 = String(c)
        # s1.set_scale(MajorScale(c))
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
