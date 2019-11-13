# THESE MODULE APPROPRIATELY TESTS LOWER-LEVEL MODULES BEFORE HITTING RUN-TIME
from bestia.output import echo

from cFlat.instruments import *


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


### KEY TESTS
key_is_valid(ChromaticKey)
key_is_valid(MajorKey)
key_is_valid(NaturalMinorKey)
key_is_valid(MelodicMinorKey)
key_is_valid(HarmonicMinorKey)
