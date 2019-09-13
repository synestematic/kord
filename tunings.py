from bestia.output import Row, FString, echo

from notes import *
from scales import *

class String(object):

    # fret = [] # WHY IS THIS SHARED BETWEEN MY STRING OBJECTS???

    def __init__(self, open_note):
        self.fret = [
            # ALWAYS INIT NEW Note()
            Note(open_note.tone, open_note.alt, open_note.oct)
        ]
        self.__scale = ChromaticScale(self.fret[0])
        self.__display_frets = 1 +12
 
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
        # input(self.fret[0])

        for fret_n, fret_note in enumerate(self.scale.scale(notes=self.frets, start=self.fret[0], all=True)):

            # if not frets_displayed:
            #     break

            note = ''
            note_color = []
            if fret_note:
                note = '{}{}{}'.format(
                    fret_note.tone,
                    fret_note.repr_alt(),
                    fret_note.repr_oct()
                )
                note_color = 'magenta' if fret_note.tone == self.scale.degree(1).tone and fret_note.alt == self.scale.degree(1).alt else 'cyan'

            string_line.append(
                FString(
                    note,
                    # fret_note,
                    size=4 if fret_n == 0 else 6,
                    align='cr',
                    fg=note_color,
                )
            )

            string_line.append(
                FString(                    
                    '║' if fret_n % 12 == 0 or fret_n == self.frets -1 else '|',
                    # '|' if fret_n % 12 == 0 else '¦',
                    size=1,
                    # fg='blue',
                    fx=['faint'],
                )
            )

            frets_displayed -= 1

        # input(frets_displayed)
        return str(string_line)


class Tuning(object):

    fret_size = 7

    _binding = {
        'upper': '═', 'lower': '═',
        # 'upper': '_', 'lower': '‾',
        # 'upper': '=', 'lower': '=',
    }

    _capo = {
        'upper': '     ╔', 'lower': '     ╚',
    }

    _fine = {
        'upper': '╗', 'lower': '╝',
    }

    @classmethod
    def binding(cls, side='lower', frets=12):
        fret_binding = cls._binding[side] * frets * cls.fret_size
        echo(
            cls._capo[side] + fret_binding[:-1] + cls._fine[side],
            # 'blue',
            'faint',
        )

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
            FString(inlays[0], size=6, align='l'),
            width=6 +83 # why this??
        )

        i = 1
        while frets:
            inlay_row.append(
                FString(
                    inlays[i],
                    size=cls.fret_size,
                    align='cl',
                    fg='magenta',
                    fx=['faint'],
                )
            )
            frets -= 1
            i += 1

        inlay_row.echo()

    def __init__(self, *arg, **kwargs):
        self.strings = []
        string_args = dict(
            [ (k.replace('string', ''), note) for k, note in kwargs.items() if k.startswith('string') ]
        )

        self._init_strings(len(string_args))
        self._assign_strings(string_args)

    ### INIT FUNCTIONS
    def _init_strings(self, string_count):
        for n in range(string_count):
            self.strings.append(None)

    def _assign_strings(self, string_args):
        for k, note in string_args.items():
            self.strings[int(k) -1] = String(note)

    ### REPR FUNCTIONS
    def fretboard(self, scale=None, frets=12, verbose=1):

        # INIT A NEW SCALE, OTHERWISE YOU USE THE SAME OBJECT!!!

        self.fret_inlays(verbose=verbose, frets=frets)
        self.binding('upper', frets=frets)

        for string in self.strings:

            string_n = FString(
                self.strings.index(string) + 1,
                fg='magenta', 
                fx=['faint'],
            )

            string.scale = scale
            string.frets = frets

            echo(str(string_n) + str(string))
        
        self.binding('lower', frets=frets)

    def string(self, s):
        return self.strings[s -1]
