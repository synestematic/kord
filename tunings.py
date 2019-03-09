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

        for fret_n, fret_note in enumerate(self.scale.scale(notes=self._DISPLAY_FRETS, start_note=self.fret[0])):

            note_display = FString(
                '{}{}{}'.format(fret_note.tone, fret_note.repr_alt(), fret_note.repr_oct()),
                size=4 if fret_n == 0 else 6,
                align='cr',
                colors=['green'] if fret_note.tone == self.scale.degree(1).tone and fret_note.alt == self.scale.degree(1).alt else ['yellow']
            )
            string_line.append(note_display)

            fret_separator = FString(
                '|' if fret_n % 12 == 0 else '¦'
            )
            string_line.append(fret_separator)

        return str(string_line)


class Tuning(object):

    fret_size = 7

    _binding = {
        'upper': '_', 'lower': '‾',
        # 'upper': '=', 'lower': '=',
    }

    @classmethod
    def binding(cls, side='lower', frets=12):
        tuners = '      ' # 'O o . '
        fret_binding = cls._binding[side] * cls.fret_size
        output = tuners + fret_binding * frets
        echo(output[:-1])

    @classmethod
    def fret_inlays(cls, verbose=1, frets=12):

        if not verbose:
            return

        fret_n_color = ['blue']

        inlays = [
            '',
            'I' if verbose == 2 else '',
            'II' if verbose == 2 else '',
            'III',
            'IV' if verbose == 2 else '',
            'V',
            'VI' if verbose == 2 else '',
            'VII',
            'VIII' if verbose == 2 else '',
            'IX',
            'X' if verbose == 2 else '',
            'XI' if verbose == 2 else '',
            'XII',
        ]

        inlay_row = Row(
            FString(inlays[0], size=6, align='cl', colors=fret_n_color),
            # width=6 +83
        )

        i = 1
        while frets:
            inlay_row.append(
                FString(inlays[i], size=cls.fret_size, align='cl', colors=fret_n_color)
            )
            frets -= 1
            i += 1

        inlay_row.echo()

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
    def fretboard(self, scale=None, frets=None):

        string_n_color = ['blue']

        self.fret_inlays(verbose=2, frets=frets)
        self.binding('upper', frets=frets)
        for string in self.strings:
            string_n = FString(self.strings.index(string) + 1, colors=string_n_color)
            string.set_scale(scale)
            echo(str(string_n) + str(string))
        self.binding('lower', frets=frets)

    def string(self, s):
        return self.strings[s -1]
