from bestia.output import Row, FString, echo, tty_cols

from .keys import *

_NOTE_WIDTH = 5
_FRET_WIDTH = 1
MAX_FRETS = 36

INLAYS = (
    'I',
    'II',
    'III',
    'IV',
    'V',
    'VI',
    'VII',
    'VIII',
    'IX',
    'X',
    'XI',

    'XII',
    'XIII',
    'XIV',
    'XV',
    'XVI',
    'XVII',
    'XVIII',
    'XIX',
    'XX',
    'XXI',
    'XXII',
    'XXIII',

    'XXIV',
    'XXV',
    'XXVI',
    'XXVII',
    'XXVIII',
    'XXIX',
    'XXX',
    'XXXI',
    'XXXII',
    'XXXIII',
    'XXXIV',
    'XXXV',
    'XXXVI',
)


def max_frets_on_screen(limit=24):
    frets = int(
        tty_cols() / ( _NOTE_WIDTH + _FRET_WIDTH )
    ) - 1
    return frets if frets <= limit else limit

class PluckedString(object):

    def __init__(self, c, alt='', oct=3, frets=0, display=None, verbose=1):
        self.tuning = Note(c, alt, oct)
        self.display_mode = display
        self.frets = 12 if not frets else frets
        self.verbose = verbose
 
    @property
    def frets(self):
        return self.__frets

    @frets.setter
    def frets(self, f):
        self.__frets = int(f) +1


    def __repr__(self):
        ''' prints string notes matching given key '''
        string_line = Row()

        mode = self.display_mode if self.display_mode else ChromaticScale(*self.tuning)

        for fret_n, note in enumerate(
            mode.spell(
                note_count=self.frets,
                start_note=self.tuning,
                yield_all=True,
            )
        ):

            fret_value = ''
            if note:
                note_fg = 'green' if note ** mode.root else 'magenta'
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
                    '║' if fret_n % 12 == 0 else '│',
                    size=_FRET_WIDTH,
                    # fg='blue',
                    # fx=['faint'],
                )
            )

            if fret_n == self.frets -1:
                break

        return str(string_line)


class PluckedStringInstrument(object):

    @classmethod
    def render_inlays(cls, frets=12, verbose=1):

        if not verbose:
            return

        dots = (3, 5, 7, 9, 12, 15, 17, 19, 21, 24, 27, 29, 31, 33, 36)

        inlay_row = Row(
            FString(
                '',
                size=_NOTE_WIDTH + _FRET_WIDTH,
                align='l'
            ),
        )

        i = 1
        while frets:
            inlay_row.append(
                FString(
                    '' if verbose == 1 and i not in dots else INLAYS[i-1],
                    size=_NOTE_WIDTH + _FRET_WIDTH,
                    align='r' if verbose == 2 else 'c', # high verbose needs more space
                    fg='cyan',
                    fx=['faint' if i not in dots else ''],
                )
            )
            frets -= 1
            i += 1

        echo(inlay_row)


    @staticmethod
    def render_binding(side, frets=12):
        ''' https://en.wikipedia.org/wiki/Box-drawing_character
        '''
        normal = { 'upper': '═', 'lower': '═' }
        twelve = { 'upper': '╦', 'lower': '╩' }
        joints = { 'upper': '╤', 'lower': '╧' }
        capo   = { 'upper': '╔', 'lower': '╚' }
        final  = { 'upper': '╕', 'lower': '╛' }
        fine   = { 'upper': '╗', 'lower': '╝' }
        total_fret_width = _NOTE_WIDTH + _FRET_WIDTH
        fret_bind = ' ' * _NOTE_WIDTH + capo[side]
        for f in range(1, frets * total_fret_width + 1):
            # final fret
            if f == frets * total_fret_width:
                if f % (total_fret_width * 12) == 0:
                    fret_bind += fine[side]
                else:
                    fret_bind += final[side]
            # 12th, 24th
            elif f % (total_fret_width * 12) == 0:
                fret_bind += twelve[side]
            # fret bar joints
            elif f % total_fret_width == 0:
                fret_bind += joints[side]
            # normal bind
            else:
                fret_bind += normal[side]
        
        echo(fret_bind)


    def __init__(self, *notes, name=''):
        self.strings = [ PluckedString(*n) for n in notes ]
        self.name = name

    def render_string(self, s, display, frets=12, verbose=1):
        if not s:
            return

        string_n = FString(
            s,
            fg='cyan', 
            fx=['faint' if verbose < 1 else ''],
        )

        string = self.strings[s-1]
        # INIT A NEW SCALE, OTHERWISE YOU USE THE SAME OUTER OBJECT!!!
        string.display_mode = display
        string.frets = frets
        string.verbose = verbose

        echo(string_n + string)

    def render_fretboard(self, display=None, frets=12, verbose=1, limit=MAX_FRETS):
        if frets > limit: frets = limit
        self.render_inlays(frets, verbose)
        self.render_binding('upper', frets)
        for s, _ in enumerate(self.strings):
            self.render_string(s+1, display, frets, verbose)
        self.render_binding('lower', frets)
