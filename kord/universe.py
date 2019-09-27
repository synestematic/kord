# THESE MODULE APPROPRIATELY TESTS LOWER-LEVEL MODULES BEFORE HITTING RUN-TIME
from bestia.output import echo

from kord.instruments import *


DANGEROUS_NON_EQUALS = (
    # ''' Used mainly to test B#, Cd, etc... '''

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


def notes_are_enharmonic(n1, n2):
    assert n1 == n2
    assert n2 == n1

def notes_not_enharmonic(n1, n2):
    assert n1 != n2
    assert n2 != n1

def notes_subtraction(n1, n2):
    assert n1 - n2 == 0


def notes_arent_enharmonic(notes=[]):
    for n in notes:
        notes_not_enharmonic(*n)


def all_notes_are_enharmonic():
    ''' checks notes in same enharmonic row are equals '''
    for enh_notes in EnharmonicMatrix:
        for x in range(len(enh_notes)):
            l = [
                enh_notes[x], enh_notes[x-1]
            ]
            notes_are_enharmonic(*l)
            notes_subtraction(*l)


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
    for Notes that dont produce InvalidNotes (any note with a triple alt)
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



def key_is_valid(KeyClass):
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

notes_arent_enharmonic(DANGEROUS_NON_EQUALS)

all_notes_are_enharmonic()

### KEY TESTS
key_is_valid(MajorKey)
key_is_valid(NaturalMinorKey)
key_is_valid(MelodicMinorKey)
key_is_valid(HarmonicMinorKey)
key_is_valid(ChromaticKey)
