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

from ..keys.scales import ChromaticScale
from ..notes import NotePitch



class AsciiInstrument():

    _FRETS = (
        '|',
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

    def degrees():
        return [
            n for n in range(21)
        ]

    def render_binding(self, frets, fret_width, is_lower):
        total_space = frets * fret_width
        render = '-' * (total_space + 1)
        return render


