from bestia.output import Row, FString, echo, tty_cols

from .keys import *

_NOTE_WIDTH = 5
_FRET_WIDTH = 1

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

MAX_FRETS = len(INLAYS)

def max_frets_on_screen():
    ''' calculates how may frets can be rendered without exceeding terminal size
        will NOT go over MAX_FRETS
    '''
    frets = int(
        tty_cols() / ( _NOTE_WIDTH + _FRET_WIDTH )
    ) - 2
    return frets if frets < MAX_FRETS else MAX_FRETS

class PluckedString(object):

    def __init__(self, c, alt='', oct=3, frets=12, mode=None, verbose=1):
        self.tuning = MusicNote(c, alt, oct)
        self.mode = mode
        self.frets = frets
        self.verbose = verbose

    def __repr__(self):
        ''' prints string notes matching given key '''
        string_line = Row()

        mode = self.mode if self.mode else ChromaticScale(*self.tuning)

        for f, note in enumerate(
            mode.spell(
                note_count=self.frets + 1,
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
                        fx=['faint'],
                    ),
                )

            # APPEND MUSICNOTE DATA
            string_line.append(
                FString(
                    fret_value,
                    size=_NOTE_WIDTH,
                    align='cr',
                )
            )

            # APPEND FRET SYMBOL
            string_line.append(
                FString(
                    '║' if f % 12 == 0 else '│',
                    size=_FRET_WIDTH,
                    # fg='blue',
                    # fx=['faint'],
                )
            )

            if f == self.frets:
                break

        return str(string_line)


class PluckedStringInstrument(object):

    def __init__(self, *notes, name=''):
        self.strings = [ PluckedString(*n) for n in notes ]
        self.name = name

    @property
    def string_n_size(self):
        ''' does not expect more then 99 strings... '''
        return 1 if len(self.strings) < 10 else 2

    def render_inlays(self, frets=12, verbose=1):

        if not verbose:
            return

        dots = (3, 5, 7, 9, 12, 15, 17, 19, 21, 24, 27, 29, 31, 33, 36)

        inlay_row = Row(
            FString(
                '',
                size=self.string_n_size + _NOTE_WIDTH + _FRET_WIDTH,
                align='l',
                # pad='*',
            ),
        )

        f = 1
        while frets:
            inlay_row.append(
                FString(
                    '' if verbose == 1 and f not in dots else INLAYS[f-1],
                    size=_NOTE_WIDTH + _FRET_WIDTH,
                    align='r' if verbose == 2 else 'c', # high verbose needs more space
                    fg='cyan',
                    fx=['faint' if f not in dots else ''],
                )
            )
            f += 1
            frets -= 1

        echo(inlay_row)


    def render_binding(self, side, frets=12):
        ''' https://en.wikipedia.org/wiki/Box-drawing_character
        '''
        normal = { 'upper': '═', 'lower': '═' }
        twelve = { 'upper': '╦', 'lower': '╩' }
        joints = { 'upper': '╤', 'lower': '╧' }
        capo   = { 'upper': '╔', 'lower': '╚' }
        final  = { 'upper': '╕', 'lower': '╛' }
        fine   = { 'upper': '╗', 'lower': '╝' }
        total_fret_width = _NOTE_WIDTH + _FRET_WIDTH
        render = ' ' * ( _NOTE_WIDTH + self.string_n_size )
        render += capo[side]
        for f in range(1, frets * total_fret_width + 1):
            # final fret
            if f == frets * total_fret_width:
                if f % (total_fret_width * 12) == 0:
                    render += fine[side]
                else:
                    render += final[side]
            # 12th, 24th
            elif f % (total_fret_width * 12) == 0:
                render += twelve[side]
            # fret bar joints
            elif f % total_fret_width == 0:
                render += joints[side]
            # normal bind
            else:
                render += normal[side]
        echo(render)

    def render_string(self, s, mode, frets=12, verbose=1):
        string_n = FString(
            s,
            fg='cyan',
            fx=['faint' if verbose < 1 else ''],
            size=self.string_n_size,
        )
        string = self.strings[s-1]
        string.mode = mode
        string.frets = frets
        string.verbose = verbose
        echo(string_n + string)

    def render_fretboard(self, mode=None, frets=12, verbose=1):
        # if frets > max_frets_on_screen():
        #     frets = max_frets_on_screen()
        self.render_inlays(frets, verbose)
        self.render_binding('upper', frets)
        for s, _ in enumerate(self.strings):
            self.render_string(s+1, mode, frets, verbose)
        self.render_binding('lower', frets)
