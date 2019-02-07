from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

_TONE = 2
_SEMITONE = 1

_UNISON = 0
_MINOR_SECOND = 1
_MAJOR_SECOND = 2
_MINOR_THIRD = 3
_MAJOR_THIRD = 4
_PERFECT_FOURTH = 5
_AUGMENTED_FOURTH = 6
_DIMINISHED_FIFTH = 6
_PERFECT_FIFTH = 7
_MINOR_SIXTH = 8
_MAJOR_SIXTH = 9
_MINOR_SEVENTH = 10
_MAJOR_SEVENTH = 11
_OCTAVE = 12

_SHARP = 1
_FLAT = -1

_TONES = [

    [ ('B', '#' ), ('C', '' ), ('D', 'bb')],

    [ ('B', '##'), ('C', '#'), ('D', 'b' )],
    
    [ ('C', '##'), ('D', '' ), ('E', 'bb')],
    
    [ ('F', 'bb'), ('D', '#' ), ('E', 'b')],

    [ ('D', '##'), ('E', ''  ), ('F', 'b')],

    [ ('G', 'bb'), ('F', ''  ), ('E', '#')],

    [ ('E', '##'), ('F', '#' ), ('G', 'b')],

    [ ('F', '##'), ('G', '' ), ('A', 'bb')],

    [ ('?', '??'), ('G', '#'), ('A', 'b')],

    [ ('G', '##'), ('A', '' ), ('B', 'bb')],

    [ ('C', 'bb'), ('A', '#' ), ('B', 'b')],

    [ ('A', '##'), ('B', '' ), ('C', 'b')],

]

class Note(object):

    _ORDER = ('C', 'D', 'E', 'F', 'G', 'A', 'B')

    def __init__(self, tone, alt=''):
        self.tone = tone.upper()
        self.alt = alt.lower()

        self.tone_index = None
        self.alt_index = None
        self.get_indeces()

        self.octave = None

    def get_indeces(self):
        for t_i, _tones in enumerate(_TONES):
            for a_i, _tone in enumerate(_tones):
                if self.tone == _tone[0] and self.alt == _tone[1]:
                    self.tone_index = t_i
                    self.alt_index = a_i
                    break

    def next(self):
        my_index = self._ORDER.index(self.tone)
        return looped_list_item(my_index +1, self._ORDER)

    def previous(self):
        my_index = self._ORDER.index(self.tone)
        return looped_list_item(my_index -1, self._ORDER)

    def __repr__(self):
        return '{}{}'.format(self.tone, self.alt)


class Scale(object):

    def __init__(self, key='C', alt=''):

        self.degree = []
        self.init_degrees()

        self.tonic = Note(key, alt)
        self.add_degree(1, self.tonic)

        for d in range(2, 9):
            self.calculate_degree(d)

    def __repr__(self):
        spell_line = Row()
        for i in range(1, 9):
            spell_line.append(FString(self.degree[i], size=4, colors=['yellow']))
        return str(spell_line)

    def init_degrees(self):
        for n in range(13):
            self.degree.append(None)

    def add_degree(self, n, note):
        self.degree[n] = note

    def calculate_degree(self, d=2):
        row_index = self.tonic.tone_index +self.interval[d]
        next_degree = [t for t in looped_list_item(row_index, _TONES) if t[0] == self.degree[d -1].next()]

        if len(next_degree) != 1:
            echo('Failed to get degree[{}] of {} {}'.format(d, self.tonic, self.__class__.__name__), 'red')
            input()

        self.add_degree(d, Note(*next_degree[0]))

class MajorScale(Scale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MAJOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MAJOR_SIXTH,
        _MAJOR_SEVENTH,
        _OCTAVE,
    ]


class MinorScale(Scale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MINOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MINOR_SIXTH,
        _MINOR_SEVENTH,
        _OCTAVE,
    ]

if __name__ == '__main__':

    try:
        c_major = MajorScale('C')
        eb_major = MajorScale('E', 'b')
        e_major = MajorScale('E')
        fs_major = MajorScale('F', '#')

        ab_major = MajorScale('A', 'b')
        a_minor = MinorScale('A')
        b_minor = MinorScale('B')

        print(b_minor)

    except KeyboardInterrupt:
        echo()
