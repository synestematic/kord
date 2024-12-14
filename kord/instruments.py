'''
㉑ ㉒ ㉓ ㉔ ㉕ ㉖ ㉗ ㉘ ㉙ ㉚
㉛ ㉜ ㉝ ㉞ ㉟ ㊱ ㊲ ㊳ ㊴ ㊵
㊶ ㊷ ㊸ ㊹ ㊺ ㊻ ㊼ ㊽ ㊾ ㊿

These are specifically sans-serif:

🄋 ➀ ➁ ➂ ➃ ➄ ➅ ➆ ➇ ➈ ➉

Black Circled Number
⓿
❶
❷
❸
❹
❺
❻
❼
❽
❾
❿


Ⓐ ⓐ
Ⓑ ⓑ
Ⓒ ⓒ
Ⓓ ⓓ
Ⓔ ⓔ
Ⓕ ⓕ
Ⓖ ⓖ


# NUMERALS = {
#     'I' : 'Ⅰ',
#     'V' : 'ⅤⅠⅤ',
#     'X' : 'Ⅹ',
#     'L' : 'Ⅼ',
#     'C' : 'Ⅽ',
#     'D' : 'Ⅾ',
#     'M' : 'Ⅿ',
# }

https://www.unicode.org/charts/nameslist/n_2460.html

'''

from bestia.output import Row, FString, echo, tty_cols

from .keys.scales import ChromaticScale
from .notes import NotePitch

__all__ = [
    'PluckedStringInstrument',
    'max_frets_on_screen',
]


class PluckedString:

    DEGREE_ICONS = (
        '⓪',  # null degree...
        # 'Ⓝ',
        # '①',
        'Ⓡ',
        '➁',
        '➂',
        '➃',
        '➄',
        '➅',
        '➆',
        '➇',
        '➈',
        '➉',
        '⑪',
        '⑫',
        '⑬',
        '⑭',
        '⑮',
        '⑯',
        '⑰',
        '⑱',
        '⑲',
        '⑳',
    )

    def __init__(
        self,
        char, alt='', oct=NotePitch.DEFAULT_OCTAVE,
        frets=12,
        mode=None,
        verbose=1,
        show_degrees=False
    ):
        self.tuning = NotePitch(char, alt, oct)
        self.mode = mode
        self.frets = frets
        self.verbose = verbose
        self.show_degrees = show_degrees

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

                if self.show_degrees:
                    for d in mode.allowed_degrees():
                        if note ** mode[d]:
                            fret_value = FString(
                                '{} '.format(
                                    self.DEGREE_ICONS[d] if self.verbose != 0
                                    else (
                                        d if d != 1 else 'R'
                                    )
                                ),
                                size=3,
                                fg=note_fg,
                                align='r',
                            )
                            break

                else:
                    fret_value = '{}{}{}'.format(
                        FString(
                            note.chr,
                            size=1,
                            fg=note_fg,
                            fx=[''],
                        ),
                        FString(
                            note.repr_alt,
                            size=0,
                            fg=note_fg,
                            fx=[''],
                        ),
                        FString(
                            note.repr_oct if self.verbose > 0 else '',
                            size=1,
                            fg=note_fg,
                            fx=['faint'],
                        ),
                    )


            # APPEND NOTE PITCH DATA
            string_line.append(
                FString(
                    fret_value,
                    size=PluckedStringInstrument.NOTE_WIDTH,
                    align='cr',
                )
            )

            # APPEND FRET SYMBOL
            string_line.append(
                FString(
                    '║' if f % 12 == 0 else '│',
                    size=PluckedStringInstrument.FRET_WIDTH,
                    # fg='blue',
                    # fx=['faint'],
                )
            )

            if f == self.frets:
                break

        return str(string_line)


class PluckedStringInstrument:

    NOTE_WIDTH = 5
    FRET_WIDTH = 1

    _INLAYS = (
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

    @classmethod
    def maximum_frets(cls):
        return len(cls._INLAYS)


    @classmethod
    def total_fret_width(cls):
        return cls.NOTE_WIDTH + cls.FRET_WIDTH


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
                size=self.string_n_size + self.total_fret_width(),
                align='l',
                # pad='*',
            ),
        )

        f = 1
        while frets:
            inlay_row.append(
                FString(
                    '' if verbose == 1 and f not in dots else self._INLAYS[f-1],
                    size=self.total_fret_width(),
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
        total_fret_width = self.total_fret_width()
        render = ' ' * ( self.NOTE_WIDTH + self.string_n_size )
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
            # normal binding
            else:
                render += normal[side]
        echo(render)


    def render_string(self, s, mode, frets=12, verbose=1, show_degrees=False):
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
        string.show_degrees = show_degrees
        echo(string_n + string)


    def render_fretboard(self, mode=None, frets=12, verbose=1, show_degrees=False):
        # if frets > max_frets_on_screen():
        #     frets = max_frets_on_screen()
        self.render_inlays(frets, verbose)
        self.render_binding('upper', frets)
        for s, _ in enumerate(self.strings):
            self.render_string(s+1, mode, frets, verbose, show_degrees)
        self.render_binding('lower', frets)


def max_frets_on_screen():
    frets_allowed_by_tty = int(
        tty_cols() / PluckedStringInstrument.total_fret_width()
    ) - 2
    if frets_allowed_by_tty < PluckedStringInstrument.maximum_frets():
        return frets_allowed_by_tty
    return PluckedStringInstrument.maximum_frets()

