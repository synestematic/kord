# THESE MODULE APPROPRIATELY TESTS LOWER-LEVEL MODULES BEFORE HITTING RUN-TIME
from bestia.output import echo

from kord.instruments import *

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


def equality_test(l=[]):
    if not l:
        l = EQUALS
    for l in EQUALS:
        # echo('{} == {}\t{}\t{} == {}\t{}'.format(
        #     l[0], l[1], l[0] == l[1],
        #     l[1], l[0], l[1] == l[0]),            
        #     'green'
        # )
        assert l[0] == l[1]
        assert l[1] == l[0]

def inequality_test(l=[]):
    if not l:
        l = NON_EQUALS
    for l in NON_EQUALS:
        # echo('{} != {}\t{}\t{} != {}\t{}'.format(
        #     l[0], l[1], l[0] != l[1],
        #     l[1], l[0], l[1] != l[0]),            
        #     'red'
        # )
        assert l[0] != l[1]
        assert l[1] != l[0]


def enharmonic_test():
    for row in EnharmonicMatrix:
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
    for _row in EnharmonicMatrix:
        for _enharmonic_note in _row:

            # ignore double alteration notes
            if len(_enharmonic_note.alt) >1:
                continue

            # check_degree_root_intervals(
            #     key_class(*_enharmonic_note)
            # )

            echo(
                '{} {}'.format(
                    key_class.__name__, _enharmonic_note
                ), 'blue'
            )
            echo(
                key_class(*_enharmonic_note),
                'cyan'
            )

### SCALES TESTS
# key_test(ChromaticKey)
# key_test(MajorKey)
# key_test(NaturalMinorKey)
# key_test(MelodicMinorKey)
# key_test(HarmonicMinorKey)


def note_subtraction():
    assert Note('C') - Note('C') == 0

note_subtraction()


def check_degree_root_intervals(s):
    for n in range(1, 128):
        a = s.degree_root_interval(n) == s[n] - s[1]
        if not a:
            echo(n, 'yellow')
            echo(
                '{} - {} == {}'.format(
                    s[n],
                    s[1],
                    s.degree_root_interval(n),
                    # s[n] - s[1]
                ), 'red'
            )
        assert a

check_degree_root_intervals(
    MajorKey('C', '')
)

def key_oct_change(Key=ChromaticKey):
    print('NO ALTS:')
    echo(Key('C', ''))
    echo(Key('D', ''))
    echo(Key('E', ''))
    echo(Key('F', ''))
    echo(Key('G', ''))
    echo(Key('A', ''))
    echo(Key('B', ''))
    print('#:')
    echo(Key('C', '#'))
    echo(Key('D', '#'))
    echo(Key('E', '#'))
    echo(Key('F', '#'))
    echo(Key('G', '#'))
    echo(Key('A', '#'))
    echo(Key('B', '#')) #####
    print('b:')
    echo(Key('C', 'b'))
    echo(Key('D', 'b'))
    echo(Key('E', 'b'))
    echo(Key('F', 'b'))
    echo(Key('G', 'b'))
    echo(Key('A', 'b'))
    echo(Key('B', 'b'))
    print('##:')
    echo(Key('C', '##'))
    # echo(Key('D', '##'))
    # echo(Key('E', '##'))
    echo(Key('F', '##'))
    # echo(Key('G', '##'))
    # echo(Key('A', '##'))
    # echo(Key('B', '##'))
    print('bb:')
    echo(Key('C', 'bb'))
    echo(Key('D', 'bb'))
    echo(Key('E', 'bb'))
    # echo(Key('F', 'bb'))
    echo(Key('G', 'bb')) ####
    echo(Key('A', 'bb'))
    echo(Key('B', 'bb'))

    return

    echo(Key('C', '#'))
    echo(Key('D', 'bb'))

key_oct_change(MajorKey)

# equality_test()
# inequality_test()
# enharmonic_test()

