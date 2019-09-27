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



def allowed_keys(KeyClass=MajorKey):
    ''' yields only practical Key objects
    for Notes that dont produce InvalidNotes
        ie. C###, etc...
    '''
    for n in notes_by_alts():
        try:
            k = KeyClass(*n)
            for d in k.scale():
                pass
            yield k
        except InvalidNote:
            pass
            echo(
                '{} invalid {}'.format(n, KeyClass.__name__),
                'red', 'faint'
            )



def test_key(KeyClass):
    ''' for a given key, allows to verify:
            * invalid scales        
            * octave changes
    '''
    echo('Testing {}'.format(KeyClass.__name__), 'underline')
    for key in allowed_keys(KeyClass):
        line = Row()
        for d in key.scale(
            notes=len(key._root_intervals) +16, yield_all=False
        ):
            line.append(
                FString(
                    d,
                    size=5,
                    fg='blue' if not (d.oct % 2) else 'white', 
                )
            )
        line.echo()

### KEY TESTS
test_key(MajorKey)
test_key(NaturalMinorKey)
test_key(MelodicMinorKey)
test_key(HarmonicMinorKey)
test_key(ChromaticKey)


# equality_test()
# inequality_test()
# enharmonic_test()

