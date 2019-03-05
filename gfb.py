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

def equality_test(ls):
    for l in ls:
        echo('{} == {}\t{}\t{} == {}\t{}'.format(
            l[0], l[1], l[0] == l[1],
            l[1], l[0], l[1] == l[0]),            
            'cyan'
        )
        assert l[0] == l[1]
        assert l[1] == l[0]

def inequality_test(ls):
    for l in ls:
        echo('{} != {}\t{}\t{} != {}\t{}'.format(
            l[0], l[1], l[0] != l[1],
            l[1], l[0], l[1] != l[0]),            
            'magenta'
        )
        assert l[0] != l[1]
        assert l[1] != l[0]

if __name__ == '__main__':
    try:
        # unit_test(ChromaticScale)
        # unit_test(MajorScale)
        # unit_test(NaturalMinorScale)
        # unit_test(MelodicMinorScale)
        # unit_test(HarmonicMinorScale)

        eqs = [
            # equal
            # (Note('c'), Note('c')),

            # 1 octave
            (Note('D', 'b'), Note('C', '#')),
            (Note('E', 'b'), Note('D', '#')),
            (Note('F', 'b'), Note('E')),
            (Note('G', 'b'), Note('F', '#')),
            (Note('A', 'b'), Note('G', '#')),
            (Note('B', 'b'), Note('A', '#')),

            (Note('D', 'bb'), Note('C', '')),
            (Note('E', 'bb'), Note('D', '')),
            (Note('F', 'bb'), Note('E', 'b')),
            (Note('G', 'bb'), Note('F', '')),
            (Note('A', 'bb'), Note('G', '')),
            (Note('B', 'bb'), Note('A', '')),

            (Note('D', ''), Note('C', '##')),
            (Note('E', ''), Note('D', '##')),
            (Note('F', '#'), Note('E', '##')),
            (Note('G', ''), Note('F', '##')),
            (Note('A', ''), Note('G', '##')),
            (Note('B', ''), Note('A', '##')),

            (Note('E', '#'), Note('G', 'bb')),


            # 2 octave
            (Note('B', 'b'), Note('C', 'bb', 4)),
            (Note('A', '#'), Note('C', 'bb', 4)),

            (Note('B'     ), Note('C', 'b', 4)),
            (Note('A', '##'), Note('C', 'b', 4)),

            (Note('B', '#'), Note('C', '', 4)),
            (Note('B', '#'), Note('D', 'bb', 4)),

            (Note('B', '##'), Note('C', '#', 4)),
            (Note('B', '##'), Note('D', 'b', 4)),

            (Note('A', '#'), Note('B', 'b')),
            (Note('A', '##'), Note('B', '')),
            (Note('C', ''), Note('D', 'bb')),
            (Note('C', '#'), Note('D', 'b')),



        ]

        neqs = [

            # (Note('c'), Note('c')),

            (Note('C', 'b', 3), Note('B', '#', 3)),

            (Note('E', 'b', 5), Note('D', '#', 4)),

            (Note('B', '', 5), Note('C', 'b', 4)),

            (Note('E', '#', 3), Note('F', '', 4)),


            (Note('B', 'b'), Note('C', 'bb')),
            (Note('A', '#'), Note('C', 'bb')),

            (Note('B'     ), Note('C', 'b')),
            (Note('A', '##'), Note('C', 'b')),

            (Note('B', '#'), Note('C', '')),
            (Note('B', '#'), Note('D', 'bb')),

            (Note('B', '##'), Note('C', '#')),
            (Note('B', '##'), Note('D', 'b')),


            # these should eval False OK
            (Note('A', '#'), Note('B', 'b', 4)),
            (Note('A', '##'), Note('B', '', 4)),
            (Note('C', ''), Note('D', 'bb', 4)),
            (Note('C', '#'), Note('D', 'b', 4)),






        ]

        equality_test(eqs)
        inequality_test(neqs)

        # c_major = MajorScale(c)
        # ebb = Note('E', 'bb', 3)
        # ebb = Note('C', '#', 3)
        # ebb_chrom = ChromaticScale(ebb)
        # for n in c_major.scale(10):
        #     echo(n, 'cyan')

        # std_tuning = Guitar(
        #     string1=ebb,
        #     string2=Note('B', 3),
        #     string3=Note('G', 3),
        #     string4=Note('D', 3),
        #     string5=Note('A', 2),
        #     string6=Note('E', 2),
        #     string7=Note('B', 2),
        # )
        # std_tuning.fretboard()
        # std_tuning.fretboard(scale=c_major)

        # for n in ebb_chrom.scale():
        #     echo(n, 'cyan')

    except KeyboardInterrupt:
        echo()

# if start_note is not in scale it yields no notes
# string with ebb0 not repr, ebb_chrom works though...
