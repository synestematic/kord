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

from .string import InstrumentString

__all__ = [
    'PluckedStringInstrument',
    'max_frets_on_screen',
]


class PluckedStringInstrument:

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

    _INLAY_DOTS = (3, 5, 7, 9, 12, 15, 17, 19, 21, 24, 27, 29, 31, 33, 36, )

    _BINDING = {
        'default': '═',
        'capo'  : ('╔', '╚'),
        '1224'  : ('╦', '╩'),
        'fret'  : ('╤', '╧'),
        'end'   : ('╕', '╛'),
        'end12' : ('╗', '╝'),
    }

    @classmethod
    def maximum_frets(cls):
        return len(cls._INLAYS)


    @classmethod
    def fret_width(cls):
        return InstrumentString.NOTE_WIDTH + InstrumentString.FRET_WIDTH


    def __init__(self, *notes):
        self.strings = [ InstrumentString(*n) for n in notes ]


    @property
    def string_n_size(self):
        ''' does not expect more then 99 strings... '''
        return 1 if len(self.strings) < 10 else 2


    def render_inlays(self, frets=12, verbose=1):

        if not verbose:
            return

        inlay_row = Row(
            FString(
                '',
                size=self.string_n_size + self.fret_width(),
                align='l',
                # pad='*',
            ),
        )

        f = 1
        while frets:
            inlay_row.append(
                FString(
                    '' if verbose == 1 and f not in self._INLAY_DOTS else self._INLAYS[f-1],
                    size=self.fret_width(),
                    align='r' if verbose == 2 else 'c', # high verbose needs more space
                    fg='cyan',
                    fx=['faint' if f not in self._INLAY_DOTS else ''],
                )
            )
            f += 1
            frets -= 1

        echo(inlay_row)


    def render_binding(self, frets, is_lower):
        ''' https://en.wikipedia.org/wiki/Box-drawing_character
        '''
        fret_width = self.fret_width()
        render = ' ' * ( InstrumentString.NOTE_WIDTH + self.string_n_size )
        render += self._BINDING['capo'][is_lower]
        total_space = frets * fret_width
        for f in range(total_space):
            f += 1
            is_12th_fret = f % (fret_width * 12) == 0
            is_fret = f % fret_width == 0
            if f == total_space:
                # final fret
                render += (
                    self._BINDING['end12'][is_lower] if is_12th_fret
                    else self._BINDING['end'][is_lower]
                )
            elif is_12th_fret:
                # 12th, 24th
                render += self._BINDING['1224'][is_lower]
            elif is_fret:
                # fret bar joints
                render += self._BINDING['fret'][is_lower]
            else:
                # normal binding
                render += self._BINDING['default']
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
        self.render_inlays(frets, verbose)
        self.render_binding(frets, is_lower=False)
        for s, _ in enumerate(self.strings):
            self.render_string(s+1, mode, frets, verbose, show_degrees)
        self.render_binding(frets, is_lower=True)


def max_frets_on_screen():
    frets_allowed_by_tty = int(
        tty_cols() / PluckedStringInstrument.fret_width()
    ) - 2
    if frets_allowed_by_tty < PluckedStringInstrument.maximum_frets():
        return frets_allowed_by_tty
    return PluckedStringInstrument.maximum_frets()

