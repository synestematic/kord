from bestia.output import Row, FString, echo

from notes import *
from scales import *

class String(object):

    # fret = [] # WHY IS THIS SHARED BETWEEN MY STRING OBJECTS???
    _DISPLAY_FRETS = 1 +12

    def __init__(self, open_note):
        self.fret = [
            # ALWAYS INIT NEW NOTe
            Note(open_note.tone, open_note.alt, open_note.oct)
        ]
        self.scale = ChromaticScale(self.fret[0])
 
    def set_scale(self, scale):
        if scale:
            self.scale = scale

    def __repr__(self):
        ''' prints string notes matching given scale '''
        string_line = Row()

        for fret_n, fret_note in enumerate(self.scale.scale(self._DISPLAY_FRETS, start_note=self.fret[0])):

            note_display = FString(
                '{}{}{}'.format(fret_note.tone, fret_note.repr_alt(), fret_note.repr_oct()),
                size=4 if fret_n == 0 else 6,
                align='cl',
                colors=['blue']
            )
            string_line.append(note_display)


            sep = FString(
                '|' if fret_n == 0 or fret_n == 12 else '¦'
            )
            string_line.append(sep)

        return str(string_line)


class Tuning(object):

    tuners = 'O o . '
    tuners = '      '

    longness = 83

    _binding = {
        'upper': '_', 'lower': '‾',
        # 'upper': '=', 'lower': '=',
    }

    @classmethod
    def binding(cls, side='lower'):
        echo(cls.tuners + cls._binding[side] * cls.longness)

    @classmethod
    def fret_markers(cls, complete=False):

        i = 'I' if complete else ''
        ii = 'II' if complete else ''
        iv = 'IV' if complete else ''
        vi = 'VI' if complete else ''
        vi = 'VI' if complete else ''
        viii = 'VIII' if complete else ''
        x = 'X' if complete else ''
        xi = 'XI' if complete else ''

        Row(
            FString('0', size=6, align='cl', colors=['magenta']),
            FString(i, size=7, align='cl', colors=['magenta'], pad=None),
            FString(ii, size=7, align='cl', colors=['magenta']),
            FString('III', size=7, align='cl', colors=['magenta']),
            FString(iv, size=7, align='cl', colors=['magenta']),
            FString('V', size=7, align='cl', colors=['magenta']),
            FString(vi, size=7, align='cl', colors=['magenta']),
            FString('VII', size=7, align='cl', colors=['magenta']),
            FString(viii, size=7, align='cl', colors=['magenta']),
            FString('IX', size=7, align='cl', colors=['magenta']),
            FString(x, size=7, align='cl', colors=['magenta']),
            FString(xi, size=7, align='cl', colors=['magenta']),
            FString('XII', size=7, align='cl', colors=['magenta']),
            width=len(cls.tuners) +cls.longness
        ).echo()

    def __init__(self, *arg, **kwargs):
        self.strings = []
        string_args = dict( [(k.replace('string', ''), note) for k, note in kwargs.items() if k.startswith('string')] )

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
    def fretboard(self, scale=None):
        self.fret_markers()
        self.binding('upper')
        for string in self.strings:
            string_n = FString(self.strings.index(string) + 1, colors=['magenta'])
            string.set_scale(scale)
            echo(str(string_n) + str(string))
        self.binding('lower')

    def string(self, s):
        return self.strings[s -1]
