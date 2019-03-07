from bestia.output import echo

from notes import *
from scales import *
from tunings import *

def compare_delta(n1, n2):            
    # 0    = equal
    # 1..  = n1 > n2
    # ..-1 = n1 < n2

    oct_delta = n1.oct - n2.oct
    tone_delta = n1.tone_delta(n2)
    alt_delta  = n1.alt_delta(n2)
    tone_alt_delta = tone_delta + alt_delta
    # echo('oct  delta: {}'.format(oct_delta), 'green')
    # echo('tone delta: {}'.format(tone_delta), 'blue')
    # echo('alt  delta: {}'.format(alt_delta), 'yellow')
    # echo('TOT  delta: {}'.format(tone_alt_delta), 'red')
    # return tone_alt_delta + oct_delta * OCTAVE

    if not oct_delta:
        # same octave
        return tone_alt_delta

    elif abs(oct_delta) > 1:
        echo('notes safely {} octs apart'.format(oct_delta))
        bla = OCTAVE * oct_delta
        # echo('D = {}'.format(bla))
        return tone_alt_delta + bla

    elif abs(oct_delta) == 1:
        bla = OCTAVE * oct_delta
        # echo('D = {}'.format(bla))
        return tone_alt_delta + bla


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
        unit_test(ChromaticScale)
        unit_test(MajorScale)
        unit_test(NaturalMinorScale)
        unit_test(MelodicMinorScale)
        unit_test(HarmonicMinorScale)

        eqs = [
            # (Note('c'), Note('c')),
            # (Note('d'), Note('d')),
            # (Note('e'), Note('e')),
            # (Note('f'), Note('f')),
            # (Note('g'), Note('g')),
            # (Note('a'), Note('a')),
            # (Note('b'), Note('b')),

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

        equality_test(eqs)
        inequality_test(neqs)
        enh_test()

        c = Note('c', '', 1)
        c_major = MajorScale(c)
        ebb = Note('C', '', 1)
        ebb_chrom = ChromaticScale(ebb)
        # for n in c_major.scale(50):
        #     echo(n, 'cyan')

        guitar_std = Tuning(
            string1=ebb,
            string2=Note('B', 3),
            string3=Note('G', 3),
            string4=Note('D', 3),
            string5=Note('A', 2),
            string6=Note('E', 2),
            string7=Note('B', 2),
        )
        # guitar_std.fretboard()
        # guitar_std.fretboard(scale=c_major)

        ukulele_std = Tuning(
            string1=Note('A', 3),
            string2=Note('E', 3),
            string3=Note('C', 3),
            string4=Note('G', 3),
        )
        # ukulele_std.fretboard()

    except KeyboardInterrupt:
        echo()

# if start_note is not in scale it yields no notes
# string with ebb0 not repr, ebb_chrom works though...
