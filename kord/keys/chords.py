
from .scales import (
    MajorScale, MinorScale, AugmentedScale, DiminishedScale,
    IonianMode, AeolianMode, MixolydianMode, LocrianMode
)


__all__ = [
    'MajorTriad',
    'MinorTriad',
    'AugmentedTriad',
    'DiminishedTriad',

    'MajorSeventhChord',
    'MinorSeventhChord',
    'DominantSeventhChord',
    'HalfDiminishedSeventhChord',
    'DiminishedSeventhChord',

    'MajorNinthChord',
    'MinorNinthChord',
    'DominantNinthChord',
]


####################
### TRIAD CHORDS ###
####################

class MajorTriad(MajorScale):
    notations = (
        'maj',
        '',
        'major',
    )
    degrees = (1, 3, 5)

class MinorTriad(MinorScale):
    notations = (
        'min',
        '-',
        'minor',
    )
    degrees = (1, 3, 5)

class AugmentedTriad(AugmentedScale):
    notations = (
        'aug',
        'augmented',
    )
    degrees = (1, 3, 5)

class DiminishedTriad(DiminishedScale):
    notations = (
        'dim',
        'diminished',
    )
    degrees = (1, 3, 5)


######################
### SEVENTH CHORDS ###
######################

class MajorSeventhChord(IonianMode):
    notations = (
        'maj7',
        # 'M7',
        'Δ7',
        'major7',
    )
    degrees = (1, 3, 5, 7)

class MinorSeventhChord(AeolianMode):
    notations = (
        'min7',
        # 'm7',
        '-7',
        'minor7',
    )
    degrees = (1, 3, 5, 7)

class DominantSeventhChord(MixolydianMode):
    notations = (
        '7',
        'dom7',
        'dominant7',
    )
    degrees = (1, 3, 5, 7)

class DiminishedSeventhChord(DiminishedScale):
    notations = (
        'dim7',
        'o7',
        'diminished7'
    )
    degrees = (1, 3, 5, 7)

class HalfDiminishedSeventhChord(LocrianMode):
    notations = (
        'm7b5',
        'min7dim5',
        'm7(b5)'
        'ø7',
    )
    degrees = (1, 3, 5, 7)


####################
### NINTH CHORDS ###
####################

class MajorNinthChord(IonianMode):
    notations = (
        'maj9',
        'M9',
    )
    degrees = (1, 3, 5, 7, 9)

class MinorNinthChord(AeolianMode):
    notations = (
        'min9',
        'm9',
    )
    degrees = (1, 3, 5, 7, 9)

class DominantNinthChord(MixolydianMode):
    notations = (
        '9',
        'dom9',
    )
    degrees = (1, 3, 5, 7, 9)

