from bestia.output import Row, FString, echo

from notes import *
from scales import *

class String(object):

    # fret = [] # WHY IS THIS SHARED BETWEEN MY STRING OBJECTS???
    _DISPLAY_FRETS = 1 +12

    def __init__(self, tone, alt='', octave=0):

        open_note = Note(tone, alt, octave)
        scale_generator = ChromaticScale(
            open_note.tone,
            open_note.alt
        ).scale(notes=self._DISPLAY_FRETS)

        self.fret = []
        for degree in scale_generator:
            self.fret.append(degree)

        self.matching_scale = None
        self.set_matching_scale()
 
    def __repr__(self):
        ''' prints string notes matching given scale '''
        string_line = Row()

        for fret_n, fret_note in enumerate(self.fret):

            tone = fret_note.tone if fret_note in self.match_scale.degrees else ''
            alt = fret_note.alt if fret_note in self.match_scale.degrees else ''
            octave = fret_note.octave if fret_note in self.match_scale.degrees else ''
            sz = 4 if fret_n == 0 else 6

            note_display = FString(
                '{}{}{}'.format(tone, alt, octave),
                size=sz, align='cr', colors=['blue']
            )
            string_line.append(note_display)

            sep = FString(
                '|' if fret_n == 0 or fret_n == 12 else '¦'
            )
            string_line.append(sep)
        
        return str(string_line)

    def set_matching_scale(self, scale=None):
        self.match_scale = ChromaticScale('C') if not scale else scale


class Guitar(object):

    tuners = 'O o .'
    tuners = '     '

    longness = 83

    @classmethod
    def binding(cls, side='lower'):
        _binding = '_' if side == 'upper' else '‾'
        echo(cls.tuners + _binding * cls.longness)

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

        r = Row(
            FString('', size=5),
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

        # FILTER STRING ARGS
        string_args = dict( [(k.replace('string', ''), note) for k, note in kwargs.items() if k.startswith('string')] )

        self._init_strings(len(string_args))
        self._assign_strings(string_args)

    ### INIT FUNCTIONS

    def _init_strings(self, string_count):
        for n in range(string_count):
            self.strings.append(None)

    def _assign_strings(self, string_args):
        for k, note in string_args.items():
            self.strings[int(k) -1] = String(
                note.tone, note.alt, note.octave
            )

    ### REPR FUNCTIONS

    def fretboard(self, scale=None):
        self.fret_markers()
        self.binding('upper')
        for string in self.strings:
            string.set_matching_scale(scale)
            echo(string)
        self.binding('lower')

    def string(self, s):
        return self.strings[s -1]

    # def echo_string(self, s):
    #     echo(self.string(s))
