from bestia.output import echo

from notes import *
from scales import *
from guitars import *

def unit_test(scale):
    for _row in ENHARMONIC_MATRIX:
        # echo(_row, 'green')
        for _enharmonic_note in _row:
            if len(_enharmonic_note.alt) >1: # ignore double alteration notes
                continue
            echo('{} {}'.format(scale.__name__, _enharmonic_note), 'blue')
            echo(scale(_enharmonic_note), 'cyan')
        # echo(_row, 'red')
    echo()

if __name__ == '__main__':
    try:
        unit_test(ChromaticScale)
        unit_test(MajorScale)
        unit_test(NaturalMinorScale)
        unit_test(MelodicMinorScale)
        unit_test(HarmonicMinorScale)

        c = Note('f')
        a3 = Note('A', 3)
        c_major = MajorScale(c)
        # for n in c_major.scale(10):
        #     echo(n, 'cyan')

        std_tuning = Guitar(
            string1=Note('E', 'bb', 4),
            string2=Note('B', 3),
            string3=Note('G', 3),
            string4=Note('D', 3),
            string5=Note('A', 2),
            string6=Note('E', 2),
            # string7=Note('B', 2),
        )
        std_tuning.fretboard()
        std_tuning.fretboard(scale=c_major)

    except KeyboardInterrupt:
        echo()

# if start_note is not in scale it yields no notes


