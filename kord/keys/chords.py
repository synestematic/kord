'''
degrees tuple is not explicitly defined anymore but is inherited from parent class:

    class TriadChord(Chord):
    class SeventhChord(Chord):
    class SixthChord(Chord):
    class NinthChord(Chord):


parent scale is now a separate class atrribute
parent_scale_degree allows to form chords from degrees other than I


'''

from .scales import (
    MajorScale, MinorScale, AugmentedScale, DiminishedScale,
    IonianMode, AeolianMode, MixolydianMode, LocrianMode, DorianMode,
    HarmonicMinorScale, MelodicMinorScale
)
from .scales import TonalKey

from ..notes.intervals import Intervals

from ..errors import InvalidNote


__all__ = [
    'PowerChord',
    'Suspended4Chord',
    'Suspended2Chord',

    'MajorTriad',
    'MinorTriad',
    'AugmentedTriad',
    'DiminishedTriad',

    'MajorSixthChord',
    'MinorSixthChord',

    'MajorSeventhChord',
    'MinorSeventhChord',
    'DominantSeventhChord',
    'HalfDiminishedSeventhChord',
    'DiminishedSeventhChord',

    'MajorAdd9Chord',
    'MinorAdd9Chord',
    'AugmentedAdd9Chord',
    'DiminishedAdd9Chord',

    'MajorNinthChord',
    'MinorNinthChord',
    'DominantNinthChord',
    'DominantMinorNinthChord',
]


class Chord(TonalKey):
    parent_scale = MajorScale
    parent_scale_degree = 1
    degrees = (1, 3, 5,)

    @classmethod
    def find_parent_scale_root(cls, match_note):
        ''' finds char for which your parent_scale will match your chord's root
            at parent_scale_degree
        '''
        scales_found = []
        for n in cls.parent_scale.valid_root_notes():
            scale = cls.parent_scale(*n)
            if scale[cls.parent_scale_degree] ** match_note:
                scales_found.append(scale)

        assert len(scales_found) <= 1
        if scales_found:
            return scales_found[0]
        return None


    @classmethod
    def _parent_scale_root_offset(cls) -> int:
        ''' if I am an E7 chord and my parent_scale is A Major
            my offset from parent_scale root is 7 semitones
        '''
        return cls.parent_scale._calc_intervals()[cls.parent_scale_degree - 1]


    @classmethod
    def _calc_intervals(cls):
        # intervals is an empty tuple for chords
        offset_from_root = cls._parent_scale_root_offset()
        arranged_intervals = []
        for parent_scale_interval in cls.parent_scale._calc_intervals():
            new_interval = parent_scale_interval - offset_from_root
            if new_interval < 0:
                new_interval += Intervals.PERFECT_OCTAVE
            arranged_intervals.append(new_interval)
        arranged_intervals.sort()
        return arranged_intervals


class PowerChord(Chord):
    ''' C  G  '''
    notations = (
        '5',
    )
    degrees = (1, 5, )

class SusFourChord(Chord):
    degrees = (1, 4, 5, )

class SusTwoChord(Chord):
    degrees = (1, 2, 5, )

class TriadChord(Chord):
    degrees = (1, 3, 5, )

class SixthChord(Chord):
    degrees = (1, 3, 5, 6, )

class SeventhChord(Chord):
    degrees = (1, 3, 5, 7, )

class AddNineChord(Chord):
    degrees = (1, 3, 5, 9, )

class NinthChord(Chord):
    degrees = (1, 3, 5, 7, 9, )


########################
### SUSPENDED CHORDS ###
########################

class Suspended4Chord(SusFourChord):
    ''' C  F  G '''
    parent_scale = IonianMode
    notations = (
        'sus4',
        'sus',
    )

class Suspended2Chord(SusTwoChord):
    ''' C  D  G '''
    parent_scale = IonianMode
    notations = (
        'sus2',
        'sus9',
    )


####################
### TRIAD CHORDS ###
####################

class MajorTriad(TriadChord):
    ''' C  E  G  '''
    parent_scale = MajorScale
    notations = (
        'maj',
        '',
        'major',
    )

class MinorTriad(TriadChord):
    ''' C  Eb G  '''
    parent_scale = MinorScale
    notations = (
        'min',
        '-',
        'm',
        'minor',
    )

class AugmentedTriad(TriadChord):
    ''' C  E  G#  '''
    parent_scale = HarmonicMinorScale
    parent_scale_degree = 3
    notations = (
        'aug',
        'augmented',
    )

class DiminishedTriad(TriadChord):
    ''' C  Eb Gb  '''
    parent_scale = MajorScale
    parent_scale_degree = 7
    notations = (
        'dim',
        'diminished',
    )


####################
### SIXTH CHORDS ###
####################

class MajorSixthChord(SixthChord):
    ''' C  E  G  A '''
    parent_scale = IonianMode
    notations = (
        '6',
        'add6',
    )

class MinorSixthChord(SixthChord):
    ''' C  Eb G  A '''
    parent_scale = DorianMode
    notations = (
        'm6',
        # 'madd6',
        'min6',
    )


######################
### SEVENTH CHORDS ###
######################

class MajorSeventhChord(SeventhChord):
    ''' C  E  G  B  '''
    parent_scale = IonianMode
    notations = (
        'maj7',
        'M7',  # careful with these 2 if ever using .lower() to compare
        'Δ7',
        'Δ',
        'major7',
    )

class MinorSeventhChord(SeventhChord):
    ''' C  Eb G  Bb '''
    parent_scale = AeolianMode
    notations = (
        'min7',
        'm7',  # careful with these 2 if ever using .lower() to compare
        '-7',
        'minor7',
    )

class DominantSeventhChord(SeventhChord):
    ''' C  E  G  Bb '''
    parent_scale = MixolydianMode
    notations = (
        '7',
        'dom7',
        'dominant7',
    )

class HalfDiminishedSeventhChord(SeventhChord):
    ''' C  Eb Gb Bb '''
    parent_scale = LocrianMode
    notations = (
        'm7b5',
        'm7-5',
        'min7dim5',
        'm7(b5)',
        'ø7',
    )

class DiminishedSeventhChord(SeventhChord):
    ''' C  Eb Gb Bbb'''
    parent_scale = HarmonicMinorScale
    parent_scale_degree = 7
    notations = (
        'dim7',
        'o7',
        'diminished7',
    )


###################
### ADD9 CHORDS ###
###################

class MajorAdd9Chord(AddNineChord):
    ''' C  E  G  D '''
    parent_scale = IonianMode
    notations = (
        'add9',
        'Add9',
    )

class MinorAdd9Chord(AddNineChord):
    ''' C  Eb G  D '''
    parent_scale = AeolianMode
    notations = (
        'madd9',
        'mAdd9',
    )

class AugmentedAdd9Chord(AddNineChord):
    ''' C  E  G# D '''
    parent_scale = HarmonicMinorScale
    parent_scale_degree = 3
    notations = (
        'augadd9',
        'augAdd9',
    )

class DiminishedAdd9Chord(AddNineChord):
    ''' C  Eb Gb D '''
    parent_scale = MelodicMinorScale
    parent_scale_degree = 6
    notations = (
        'dimadd9',
        'dimAdd9',
    )


####################
### NINTH CHORDS ###
####################

class MajorNinthChord(NinthChord):
    ''' C  E  G  B  D  '''
    parent_scale = IonianMode
    notations = (
        'maj9',
        'M9',
        'major9',
    )

class MinorNinthChord(NinthChord):
    ''' C  Eb G  Bb D  '''
    parent_scale = AeolianMode
    notations = (
        'm9',
        'min9',
        '-9',
        'minor9',
    )

class DominantNinthChord(NinthChord):
    ''' C  E  G  Bb D  '''
    parent_scale = MixolydianMode
    notations = (
        '9',
        'dom9',
    )

class DominantMinorNinthChord(NinthChord):
    ''' C  E  G  Bb Db '''
    parent_scale = HarmonicMinorScale
    parent_scale_degree = 5
    notations = (
        '7b9',
    )

