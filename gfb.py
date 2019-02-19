from bestia.output import Row, FString, echo

from notes import *
from scales import *

class Fret(object):

    def __init__(self, note='', fret=12):
        self.fret = fret
        self.note = Note(' ', ' ', ' ') if not note else note

    def __repr__(self):
        f = '||' if self.fret == 0 else '|'
        fret = FString(
            '{}{}{} {}'.format(self.note.tone, self.note.alt, self.note.octave, f),
            size=6, align='r', colors=['red']
        )
        return str(fret)


class String(object):

    fret = []

    def __init__(self, open_note='Abb3'):

        self.init_frets()

        tone = open_note[0]
        alt = open_note[1:-1]
        octave = int(open_note[-1])

        open_note = Note(tone, alt, octave)
        self.fret[0] = Fret(open_note, fret=0)

    def init_frets(self):
        for n in range(12):
            self.fret.append(Fret())


    def __repr__(self):
        string_line = Row()
        for i in range(12):
            string_line.append(self.fret[i])
        return str(string_line)


class Tuning(object):

    def __init__(self, *arg, **kwargs):
        for k, v in kwargs.items():
            if k.startswith('string'):
                setattr(self, k, String(v))



def unit_test(s):
    for _row in NOTE_MATRIX:
        for _column in _row:
            if len(_column.alt) >1 or '?' in _column.alt:
                continue
            echo(_column, 'blue')
            echo(s(_column.tone, _column.alt), 'cyan')

if __name__ == '__main__':

    try:
        # b_minor = NaturalMinorScale('B')
        # print(b_minor)

        # a_minor = MelodicMinorScale('A')
        # print(a_minor)

        # d_minor = HarmonicMinorScale('D')
        # print(d_minor)

        std_tuning = Tuning(
            string1='E4',
            string2='B3',
            string3='G3',
            string4='D3',
            string5='A2',
            string6='E2'
        )
        # echo(std_tuning.string5)

        empty_fret = Fret(fret=6)
        string1 = Row(
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            width=72
        ).echo()

        Bb3 = Note('B', 'b', 3)
        # new_fret = Fret(Bb3, fret=12)
        # print(new_fret)

        unit_test(ChromaticScale)
        unit_test(MajorScale)
        unit_test(NaturalMinorScale)
        unit_test(MelodicMinorScale)
        unit_test(HarmonicMinorScale)

    except KeyboardInterrupt:
        echo()


# JUST FINISHED BASIC CHROMATIC SCALE DEFINITION TO OUTPUT ALL FRETS OF STRING
