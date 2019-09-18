# THESE MODULE APPROPRIATELY TESTS LOWER-LEVEL MODULES BEFORE HITTING RUN-TIME
from bestia.output import echo

from kord.tunings import *

EQUALS = (

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

)


NON_EQUALS = (

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
)


def equality_test(ls):
    for l in ls:
        echo('{} == {}\t{}\t{} == {}\t{}'.format(
            l[0], l[1], l[0] == l[1],
            l[1], l[0], l[1] == l[0]),            
            'green'
        )
        assert l[0] == l[1]
        assert l[1] == l[0]

def inequality_test(ls):
    for l in ls:
        echo('{} != {}\t{}\t{} != {}\t{}'.format(
            l[0], l[1], l[0] != l[1],
            l[1], l[0], l[1] != l[0]),            
            'red'
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


def key_test(key_class):
    for _row in ENHARMONIC_MATRIX:
        for _enharmonic_note in _row:

            # ignore double alteration notes
            if len(_enharmonic_note.alt) >1:
                continue

            echo(
                '{} {}'.format(
                    key_class.__name__, _enharmonic_note
                ), 'blue'
            )
            echo(
                key_class(*_enharmonic_note),
                'cyan'
            )


equality_test(EQUALS)
inequality_test(NON_EQUALS)
enh_test()

### SCALES TESTS
key_test(ChromaticKey)
key_test(MajorKey)
key_test(NaturalMinorKey)
key_test(MelodicMinorKey)
key_test(HarmonicMinorKey)



# if __name__ == '__main__':

#     try:
#         ### NOTES TESTS
#         equality_test(EQUALS)
#         inequality_test(NON_EQUALS)
#         enh_test()

#         # ### SCALES TESTS
#         key_test(ChromaticKey)
#         key_test(MajorKey)
#         key_test(NaturalMinorKey)
#         key_test(MelodicMinorKey)
#         key_test(HarmonicMinorKey)

#     except KeyboardInterrupt:
#         pass

#     finally:
#         echo('Done', 'green')
