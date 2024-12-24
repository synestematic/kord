
from .scales import (
    MajorScale, MinorScale, AugmentedScale, DiminishedScale,
    IonianMode, AeolianMode, MixolydianMode, LocrianMode, DorianMode,
    HarmonicMinorScale,
)
from .scales import TonalKey

from ..notes import (
    UNISON, DIMINISHED_SECOND,          #0
    MINOR_SECOND, AUGMENTED_UNISON,     #1
    MAJOR_SECOND, DIMINISHED_THIRD,     #2
    MINOR_THIRD, AUGMENTED_SECOND,      #3
    DIMINISHED_FOURTH, MAJOR_THIRD,     #4
    PERFECT_FOURTH, AUGMENTED_THIRD,    #5
    AUGMENTED_FOURTH, DIMINISHED_FIFTH, #6
    PERFECT_FIFTH, DIMINISHED_SIXTH,    #7
    MINOR_SIXTH, AUGMENTED_FIFTH,       #8
    MAJOR_SIXTH, DIMINISHED_SEVENTH,    #9
    MINOR_SEVENTH, AUGMENTED_SIXTH,     #10
    MAJOR_SEVENTH, DIMINISHED_OCTAVE,   #11
    PERFECT_OCTAVE, AUGMENTED_SEVENTH,  #12
)

from ..errors import InvalidNote


__all__ = [
    'PowerChord',

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
    'DominantMinorNinthChord',

    'MajorSixthChord',
    'MinorSixthChord',

    'SuspendedFourChord',
    'SuspendedTwoChord',

    'Chord',
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
    def root_to_parent_scale_degree_offset(cls):
        return cls.parent_scale._calc_intervals()[cls.parent_scale_degree - 1]


    @classmethod
    def _calc_intervals(cls):
        # intervals is an empty tuple for chords
        offset_from_root = cls.root_to_parent_scale_degree_offset()
        arranged_intervals = []
        for parent_scale_interval in cls.parent_scale._calc_intervals():
            new_interval = parent_scale_interval - offset_from_root
            if new_interval < 0:
                new_interval += PERFECT_OCTAVE
            arranged_intervals.append(new_interval)
        arranged_intervals.sort()
        return arranged_intervals


class TriadChord(Chord):
    degrees = (1, 3, 5, )

class SeventhChord(Chord):
    degrees = (1, 3, 5, 7, )

class SixthChord(Chord):
    degrees = (1, 3, 5, 6, )

class NinthChord(Chord):
    # degrees = ()
    degrees = (1, 3, 5, 7, 9, )

class DominantMinorNinthChord(NinthChord):
    parent_scale = HarmonicMinorScale
    parent_scale_degree = 5
    notations = (
        '7b9',
    )
    # intervals = (
    #     UNISON,
    #     MINOR_SECOND, # <<<
    #     MAJOR_THIRD,
    #     PERFECT_FOURTH,
    #     PERFECT_FIFTH,
    #     MAJOR_SIXTH,
    #     MINOR_SEVENTH,
    # )


##################
### NON-CHORDS ###
##################

class PowerChord(MajorScale):
    notations = (
        '5',
    )
    degrees = (1, 5)


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
        'm',
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
        'M7',  # careful with these 2 if ever using .lower() to compare
        'Δ7',
        'Δ',
        'major7',
    )
    degrees = (1, 3, 5, 7)

class MinorSeventhChord(AeolianMode):
    notations = (
        'min7',
        'm7',  # careful with these 2 if ever using .lower() to compare
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
        'diminished7',
    )
    degrees = (1, 3, 5, 7)

class HalfDiminishedSeventhChord(LocrianMode):
    notations = (
        'm7b5',
        'm7-5',
        'min7dim5',
        'm7(b5)',
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
        'major9',
    )
    degrees = (1, 3, 5, 7, 9)

class MinorNinthChord(AeolianMode):
    notations = (
        'm9',
        'min9',
        '-9',
        'minor9',
    )
    degrees = (1, 3, 5, 7, 9)

class DominantNinthChord(MixolydianMode):
    notations = (
        '9',
        'dom9',
    )
    degrees = (1, 3, 5, 7, 9)

# class DominantMinorNinthChord(MixolydianMode):
#     ''' needs to be expressed as:
#         dominant 9th chord formed on 5th degree of harmonic minor scale
#     '''
#     notations = (
#         '7b9',
#     )
#     intervals = (
#         UNISON,
#         MINOR_SECOND, # <<<
#         MAJOR_THIRD,
#         PERFECT_FOURTH,
#         PERFECT_FIFTH,
#         MAJOR_SIXTH,
#         MINOR_SEVENTH,
#     )
#     degrees = (1, 3, 5, 7, 9)


####################
### SIXTH CHORDS ###
####################

# 6th is always major, 3rd can be major|minor

class MajorSixthChord(IonianMode):
    notations = (
        '6',
        'add6',
    )
    degrees = (1, 3, 5, 6)

class MinorSixthChord(DorianMode):
    notations = (
        'm6',
        # 'madd6',
        'min6',
    )
    degrees = (1, 3, 5, 6)


# class AddNineChord(DorianMode):
#     notations = (
#         'add9',
#     )
#     degrees = (1, 3, 5, 9)


########################
### SUSPENDED CHORDS ###
########################

class SuspendedFourChord(IonianMode):
    notations = (
        'sus4',
        'sus',
    )
    degrees = (1, 4, 5)

class SuspendedTwoChord(IonianMode):
    notations = (
        'sus2',
        'sus9',
    )
    degrees = (1, 2, 5)
