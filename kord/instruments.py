from bestia.output import Row, FString, echo, tty_cols

from .keys import *

_NOTE_WIDTH = 5
_FRET_WIDTH = 1

def max_frets_on_screen(limit=24):
    frets = int(
        tty_cols() / ( _NOTE_WIDTH + _FRET_WIDTH )
    ) - 1
    return frets if frets <= limit else limit

class PluckedString(object):

    def __init__(self, tone, alt='', oct=0, frets=0, display=None, verbose=1):

        self.__key = None

        self.tuning = Note(tone, alt, oct)
        self.display_method = display
        self.frets = 12 if not frets else frets
        self.verbose = verbose
 

    @property
    def key(self):
        ''' inits an object of parent Key class from self.display_method '''
        if not self.__key:
            __key  = self.display_method.__self__
            Key = __key.__class__
            self.__key = Key(
                __key.root.chr,
                __key.root.alt,
            )
        return self.__key

    # USERS DO NOT SET STRING.KEY... USE STRING.DISPLAY_METHOD
    # @key.setter
    # def key(self, k):
    #     self.__key = k

    @property
    def display_method(self):
        if not self.__display:
            self.__display = ChromaticKey(*self.tuning).scale
        return self.__display

    @display_method.setter
    def display_method(self, dm):
        self.__display = dm


    @property
    def frets(self):
        return self.__frets

    @frets.setter
    def frets(self, f):
        self.__frets = int(f) +1


    def __repr__(self):
        ''' prints string notes matching given key '''
        string_line = Row()

        for fret_n, note in enumerate(
            self.display_method(
                note_count=self.frets,
                start_note=self.tuning,
                yield_all=True,
            )
        ):

            fret_value = ''
            if note:
                note_fg = 'green' if note ** self.key.root else 'magenta'
                fret_value = '{}{}{}'.format(
                    FString(note.chr, size=1, fg=note_fg, fx=['']),
                    FString(note.repr_alt, size=0, fg=note_fg, fx=['']),
                    FString(
                        note.repr_oct if self.verbose > 0 else '',
                        size=1,
                        fg=note_fg,
                        fx=['faint' if self.verbose < 2 else ''],
                    ),
                )

            # APPEND NOTE_INFO
            string_line.append(
                FString(
                    fret_value,
                    size=_NOTE_WIDTH -1 if fret_n == 0 else _NOTE_WIDTH,
                    align='cr',
                )
            )

            # APPEND FRET
            string_line.append(
                FString(                   
                    '║' if fret_n % 12 == 0 or fret_n == self.frets -1 else '|', #¦
                    size=_FRET_WIDTH,
                    # fg='blue',
                    # fx=['faint'],
                )
            )

            if fret_n == self.frets -1:
                break

        return str(string_line)


class PluckedStringInstrument(object):

    def __init__(self, *notes, name=''):
        self.name = name
        self.strings = [ PluckedString(*n) for n in notes ]


    def string(self, s):
        return self.strings[s -1]


    def fretboard(self, display=None, frets=12, verbose=1, limit=24):

        if frets > limit:
            frets = limit

        # INIT A NEW SCALE, OTHERWISE YOU USE THE SAME OUTER OBJECT!!!
        if verbose:
            echo(self.fret_inlays(verbose=verbose, frets=frets))

        echo(self.binding('upper', frets=frets))

        for string in self.strings:

            # string numbers
            string_n = FString(
                self.strings.index(string) +1,
                fg='cyan', 
                fx=['faint' if verbose < 1 else ''],
            )

            string.display_method = display
            string.frets = frets
            string.verbose = verbose

            echo(str(string_n) + str(string))
        
        echo(self.binding('lower', frets=frets))


    @classmethod
    def fret_inlays(cls, verbose=1, frets=12):

        if not verbose:
            return ''

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
            size=6 +83 # why this??
        )

        i = 1
        while frets:
            inlay_row.append(
                FString(
                    inlays[i],
                    size=_NOTE_WIDTH + _FRET_WIDTH,
                    align='cl',
                    fg='cyan',
                    fx=['faint' if i in (1, 2, 4, 6, 8, 10, 11, 13, 14, 16, 18, 20, 22, 23) else ''],
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

