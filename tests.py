from bestia.output import echo
from gfb import *

def scale_test(scale):
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

        equal_notes = [
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

        not_equal_notes = [

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


        equality_test(equal_notes)
        inequality_test(not_equal_notes)
        enh_test()

        # TEST SCALES
        scale_test(ChromaticScale)
        scale_test(MajorScale)
        scale_test(NaturalMinorScale)
        scale_test(MelodicMinorScale)
        scale_test(HarmonicMinorScale)


    except KeyboardInterrupt:
        pass

    finally:
        echo('Done')
