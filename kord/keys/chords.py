
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
    degrees = (1, 3, 5)

class MinorTriad(MinorScale):
    degrees = (1, 3, 5)

class AugmentedTriad(AugmentedScale):
    degrees = (1, 3, 5)

class DiminishedTriad(DiminishedScale):
    degrees = (1, 3, 5)


######################
### SEVENTH CHORDS ###
######################

class MajorSeventhChord(IonianMode):
    degrees = (1, 3, 5, 7)

class MinorSeventhChord(AeolianMode):
    degrees = (1, 3, 5, 7)

class DominantSeventhChord(MixolydianMode):
    degrees = (1, 3, 5, 7)

class HalfDiminishedSeventhChord(LocrianMode):
    degrees = (1, 3, 5, 7)

class DiminishedSeventhChord(DiminishedScale):
    degrees = (1, 3, 5, 7)


####################
### NINTH CHORDS ###
####################

class MajorNinthChord(IonianMode):
    degrees = (1, 3, 5, 7, 9)

class MinorNinthChord(AeolianMode):
    degrees = (1, 3, 5, 7, 9)

class DominantNinthChord(MixolydianMode):
    degrees = (1, 3, 5, 7, 9)

