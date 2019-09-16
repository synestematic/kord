from bestia.output import Row, FString, echo, tty_columns

from notes import *
from scales import *

_NOTE_WIDTH = 5
_FRET_WIDTH = 1

def recommended_frets():
    frets = int(
        tty_columns() / ( _NOTE_WIDTH + _FRET_WIDTH )
    ) - 1
    return frets if frets <= 24 else 24

class String(object):

    # fret = [] # WHY IS THIS SHARED BETWEEN MY STRING OBJECTS???

    def __init__(self, tone, alt='', oct=0, frets=0):

        self.fret = [
            # ALWAYS INIT NEW Note()
            Note(tone, alt, oct)
        ]

        self.__scale = ChromaticScale(*self.fret[0])

        self.frets = 12 if not frets else frets
 
    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, s):
        self.__scale = s

    @property
    def frets(self):
        return self.__display_frets

    @frets.setter
    def frets(self, f):
        self.__display_frets = int(f) +1


    def __repr__(self):
        ''' prints string notes matching given scale '''
        string_line = Row()

        frets_displayed = self.frets

        for fret_n, fret_note in enumerate(self.scale.scale(notes=self.frets, start=self.fret[0], all=True)):

            # if not frets_displayed:
            #     break

            note = ''
            note_color = ''
            note_fx = ''
            if fret_note:
                note = '{}{}{}'.format(
                    fret_note.tone,
                    fret_note.repr_alt,
                    fret_note.repr_oct,
                )
                note_fx = 'underline' if fret_note.is_note(self.scale.degree(1), ignore_oct=1) else ''

            string_line.append(
                FString(
                    note,
                    # fret_note,
                    size=_NOTE_WIDTH -1 if fret_n == 0 else _NOTE_WIDTH,
                    align='cr',
                    fg='cyan',
                    # fg=note_color,
                    fx=[note_fx],
                )
            )

            string_line.append(
                FString(                    
                    '║' if fret_n % 12 == 0 or fret_n == self.frets -1 else '¦',
                    # '|' if fret_n % 12 == 0 else '¦',
                    size=_FRET_WIDTH,
                    # fg='blue',
                    # fx=['faint'],
                )
            )

            # if fret_note:
            #     frets_displayed -= 1

        # input(frets_displayed)
        return str(string_line)


class Tuning(object):


    def __init__(self, *notes):
        self.strings = []
        for n in notes:
            self.strings.append(
                String(*n)
            )


    def string(self, s):
        return self.strings[s -1]


    def fretboard(self, scale=None, frets=12, verbose=1):

        # INIT A NEW SCALE, OTHERWISE YOU USE THE SAME OUTER OBJECT!!!

        echo(self.fret_inlays(verbose=verbose, frets=frets))
        echo(self.binding('upper', frets=frets))

        for string in self.strings:

            string_n = FString(
                self.strings.index(string) +1,
                fg='magenta', 
                fx=['faint'],
            )

            string.scale = scale
            string.frets = frets

            echo(str(string_n) + str(string))
        
        echo(self.binding('lower', frets=frets))


    @classmethod
    def fret_inlays(cls, verbose=1, frets=12):

        if not verbose:
            return

        inlays = (
            '',
            'I' if verbose > 1 else '',
            'II' if verbose > 1 else '',
            'III',
            'IV' if verbose > 1 else '',
            'V',
            'VI' if verbose > 1 else '',
            'VII',
            'VIII' if verbose > 1 else '',
            'IX',
            'X' if verbose > 1 else '',
            'XI' if verbose > 1 else '',

            'XII',
            'XIII' if verbose > 1 else '',
            'XIV' if verbose > 1 else '',
            'XV',
            'XVI' if verbose > 1 else '',
            'XVII',
            'XVIII' if verbose > 1 else '',
            'XIX',
            'XX' if verbose > 1 else '',
            'XXI',
            'XXII' if verbose > 1 else '',
            'XXIII' if verbose > 1 else '',

            'XXIV'
        )

        inlay_row = Row(
            FString(
                inlays[0],
                size=_NOTE_WIDTH + _FRET_WIDTH,
                align='l'
            ),
            width=6 +83 # why this??
        )

        i = 1
        while frets:
            inlay_row.append(
                FString(
                    inlays[i],
                    size=_NOTE_WIDTH + _FRET_WIDTH,
                    align='cl',
                    fg='magenta',
                    fx=['faint'],
                )
            )
            frets -= 1
            i += 1

        return inlay_row


    @staticmethod
    def binding(side, frets=12):
        binding = {'upper': '═', 'lower': '═'}
        capo = {'upper': '     ╔', 'lower': '     ╚'}
        fine = {'upper': '╗', 'lower': '╝'}
        fret_binding = binding[side] * frets * (_NOTE_WIDTH + _FRET_WIDTH)
        return capo[side] + fret_binding[:-1] + fine[side]

