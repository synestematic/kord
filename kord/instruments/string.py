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

from bestia.output import Row, FString, echo

from ..keys.scales import ChromaticScale
from ..notes import NotePitch

__all__ = [
    'InstrumentString',
]


class InstrumentString:

    NOTE_WIDTH = 5
    FRET_WIDTH = 1

    _FRETS = (
        '│',
        '║',
    )

    _DEGREE_ICONS = (
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
                                    self._DEGREE_ICONS[d] if self.verbose != 0
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
                    size=self.NOTE_WIDTH,
                    align='cr',
                )
            )

            # APPEND FRET SYMBOL
            string_line.append(
                FString(
                    self._FRETS[ f % 12 == 0 ],
                    size=self.FRET_WIDTH,
                    # fg='blue',
                    # fx=['faint'],
                )
            )

            if f == self.frets:
                break

        return str(string_line)

