from bestia.output import echo

from notes import *
from scales import *
from tunings import *

def unit_test(scale):
    for _row in ENHARMONIC_MATRIX:
        for _enharmonic_note in _row:
            if len(_enharmonic_note.alt) >1: # ignore double alteration notes
                continue
            echo('{} {}'.format(scale.__name__, _enharmonic_note), 'blue')
            echo(scale(_enharmonic_note), 'cyan')
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

def enh_test():
    for row in ENHARMONIC_MATRIX:
        if len(row) == 3:
            l = [
                [ row[0], row[1] ],
                [ row[1], row[2] ],
                [ row[0], row[2] ],
            ]
        elif len(row) == 2:
            l = [
                [ row[0], row[1] ],
            ]
        equality_test(l)

if __name__ == '__main__':
    try:
        eqs = [
            (Note('c'), Note('c')),
            (Note('d'), Note('d')),
            (Note('e'), Note('e')),
            (Note('f'), Note('f')),
            (Note('g'), Note('g')),
            (Note('a'), Note('a')),
            (Note('b'), Note('b')),

            (Note('A', '#'), Note('B', 'b')),
            (Note('A', '##'), Note('B', '')),
            (Note('C', ''), Note('D', 'bb')),
            (Note('C', '#'), Note('D', 'b')),

        ]

        neqs = [

            (Note('C', 'b', 3), Note('B', '#', 3)),

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

        # equality_test(eqs)
        # inequality_test(neqs)
        # enh_test()

        # unit_test(ChromaticScale)
        # unit_test(MajorScale)
        # unit_test(NaturalMinorScale)
        # unit_test(MelodicMinorScale)
        # unit_test(HarmonicMinorScale)
        c = Note('e')
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
        # guitar_std.fretboard()
        guitar_std.fretboard(scale=c_major)

        ukulele_std = Tuning(
            string1=Note('E', '#', 3),
            string2=Note('b', 'b', 3),
            string3=Note('C', 3),
            string4=Note('G', 3),
        )
        ukulele_std.fretboard()

        mel = ChromaticScale(Note('E', '#'))
        for n in mel.scale(9, start_note=Note('E', '#', 3)):
            echo(n, 'cyan')


    except KeyboardInterrupt:
        echo()

