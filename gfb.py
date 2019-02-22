from bestia.output import Row, FString, echo

from notes import *
from scales import *
from guitars import *

def unit_test(s):
    for _row in ENHARMONIC_MATRIX:
        for _enharmonic_note in _row:
            if len(_enharmonic_note.alt) >1 or '?' in _enharmonic_note.alt:
                continue
            echo(_enharmonic_note, 'blue')
            echo(s(_enharmonic_note.tone, _enharmonic_note.alt), 'cyan')

if __name__ == '__main__':
    try:
        # a_minor = MelodicMinorScale('A')
        # print(a_minor)

        std_tuning = Guitar(
            string1=Note('E', '', 4),
            string2=Note('B', '', 3),
            string3=Note('G', '', 3),
            string4=Note('D', '', 3),
            string5=Note('A', '', 2),
            string6=Note('E', '', 2),
            string7=Note('B', '', 2),
        )

        c_major = MajorScale('E')
        std_tuning.fretboard(scale=c_major)
        # echo(std_tuning.string(4))

        # unit_test(ChromaticScale)
        # unit_test(MajorScale)
        # unit_test(NaturalMinorScale)
        # unit_test(MelodicMinorScale)
        # unit_test(HarmonicMinorScale)

        # a_major = MinorScale('A')
        # for n in a_major.ninth():
        #     print(n)

        # a = Note('A', octave=1)
        # b = Note('A', octave=2)
        # if a == b:
        #     echo('same')

    except KeyboardInterrupt:
        echo()

# IMPLEMENT OCTAVES !!!
