from bestia.output import Row, FString, echo

from notes import *
from scales import *

class String(object):

    # fret = [] # WHY IS THIS SHARED BETWEEN MY STRING OBJECTS???

    def __init__(self, tone, alt='', octave=0):

        open_note = Note(tone, alt, octave)
        scale_generator = ChromaticScale(
            open_note.tone,
            open_note.alt
        ).spell()

        self.fret = []
        for degree in scale_generator:
            self.fret.append(degree)

    def __repr__(self):
        string_line = Row()

        for fret, note in enumerate(self.fret):

            sz = 4 if fret == 0 else 6
            note = FString(
                '{}{}{}'.format(note.tone, note.alt, note.octave),
                size=sz, align='cr', colors=['blue']
            )

            string_line.append(note)

            sep = FString(
                '|' if fret == 0 else '¦'
            )
            string_line.append(sep)
        
        return str(string_line)


class Tuning(object):

    tuners = '     '
    # tuners = 'O  O  O  '

    longness = 83

    @classmethod
    def binding(cls, side='lower'):
        _binding = '_' if side == 'upper' else '‾'
        echo(cls.tuners + _binding * cls.longness)

    @classmethod
    def fret_markers(cls):
        r = Row(
            FString('', size=5),
            FString('I', size=7, align='cl', colors=['magenta'], pad=None),
            FString('II', size=7, align='cl', colors=['magenta']),
            FString('III', size=7, align='cl', colors=['magenta']),
            FString('IV', size=7, align='cl', colors=['magenta']),
            FString('V', size=7, align='cl', colors=['magenta']),
            FString('VI', size=7, align='cl', colors=['magenta']),
            FString('VII', size=7, align='cl', colors=['magenta']),
            FString('VIII', size=7, align='cl', colors=['magenta']),
            FString('IX', size=7, align='cl', colors=['magenta']),
            FString('X', size=7, align='cl', colors=['magenta']),
            FString('XI', size=7, align='cl', colors=['magenta']),
            FString('XII', size=7, align='cl', colors=['magenta']),
            width=len(cls.tuners) +cls.longness
        ).echo()

    def __init__(self, *arg, **kwargs):
        for k, v in kwargs.items():
            if k.startswith('string'):
                setattr(self, k, String(v))


def unit_test(s):
    for _row in NOTE_MATRIX:
        for _enharmonic_note in _row:
            if len(_enharmonic_note.alt) >1 or '?' in _enharmonic_note.alt:
                continue
            echo(_enharmonic_note, 'blue')
            echo(s(_enharmonic_note.tone, _enharmonic_note.alt), 'cyan')

if __name__ == '__main__':

    try:
        # b_minor = NaturalMinorScale('B')
        # print(b_minor)

        # a_minor = MelodicMinorScale('A')
        # print(a_minor)

        # d_minor = HarmonicMinorScale('D')
        # print(d_minor)

        # std_tuning = Tuning(
        #     string1='E4',
        #     string2='B3',
        #     string3='G3',
        #     string4='D3',
        #     string5='A2',
        #     string6='E2'
        # )
        # echo(std_tuning.string5)

        Tuning.fret_markers()
        Tuning.binding('upper')

        s = String('E', '', 4)
        echo(s, 'green')
        d = String('B', '', 3)
        echo(d, 'green')
        s = String('G', '', 3)
        echo(s, 'green')
        s = String('D', '', 3)
        echo(s, 'green')
        s = String('A', '', 2)
        echo(s, 'green')
        s = String('E', '', 2)
        echo(s, 'green')

        Tuning.binding('lower')

        # empty_fret = Fret(fret=6)
        # string1 = Row(
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     empty_fret, 
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     # FString(empty_fret, size=6, align='r'),
        #     width=72
        # ).echo()

        # Bb3 = Note('B', 'b', 3)
        # new_fret = Fret(Bb3, fret=12)
        # print(new_fret)

        # unit_test(ChromaticScale)
        # unit_test(MajorScale)
        # unit_test(NaturalMinorScale)
        # unit_test(MelodicMinorScale)
        # unit_test(HarmonicMinorScale)

    except KeyboardInterrupt:
        echo()


# JUST FINISHED BASIC CHROMATIC SCALE DEFINITION TO OUTPUT ALL FRETS OF STRING
