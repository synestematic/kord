from bestia.output import Row, FString, echo

from .notes import *

class TonalKey(object):

    degrees = ()

    @classmethod
    def allowed_degrees(cls):
        rs = cls.degrees if cls.degrees else [n+1 for n in range( len(cls.root_intervals) )] 
        out = []
        for o in range(MAX_OCT):
            for r in rs:
                out.append(
                    r + len(cls.root_intervals) * o
                )
        return out

    def __init__(self, chr, alt='', oct=0):
        self.root = Note(chr, alt, 0) # ignore note.oct

    def __repr__(self):
        spell_line = Row()
        for d in self.spell(
            note_count=len(self.root_intervals) +1, yield_all=False
        ):
            spell_line.append(
                FString(d, size=5)
            )
        return str(spell_line)

    @property
    def name(self):
        return self.__class__.__name__

    @classmethod
    def __possible_root_notes(cls, valids=True):
        ''' checks all possible notes for validity as root of given key '''
        valid_roots = []
        invalid_roots = []

        for note in notes_by_alts():

            try:
                invalid_root = False
                for _ in cls(*note).spell(note_count=len(cls.root_intervals) +1, yield_all=0):
                    # if any degree fails, scale is not spellable
                    pass

            except InvalidNote:
                invalid_root = True

            finally:
                if invalid_root:
                    invalid_roots.append(note)
                else:
                    valid_roots.append(note)

        return valid_roots if valids else invalid_roots

    @classmethod
    def valid_root_notes(cls):
        ''' returns only valid root notes for given key class '''
        return cls.__possible_root_notes(valids=True)

    @classmethod
    def invalid_root_notes(cls):
        ''' returns only invalid root notes for given key class '''
        return cls.__possible_root_notes(valids=False)

    def degree_root_interval(self, d):
        ''' return degree's delta semitones from key's root '''
        if d > len(self.root_intervals):
            return self.degree_root_interval(
                d - len(self.root_intervals)
            ) + OCTAVE
        return self.root_intervals[d -1]


    def _spell(self, note_count=-1, start_note=None, yield_all=True, note_order=[]):
        ''' * returns when note_count == 0
            * positive note_count yields notes exactly
            * negative note_count yields notes indefinetly
            * filters Nones if needed
        '''
        if not start_note:
            start_note = self.root

        if not note_order:
            note_order = [
                n+1 for n in range( len(self.root_intervals) )
            ]

        for note in self._solmizate(
            start_note=start_note
        ):
            if note_count == 0:
                return

            if note:
                yield note
                note_count -= 1

            elif yield_all:
                yield None



    def _solmizate(self, start_note):
        ''' * yields based on allowed_degrees
            * always yields Nones
            * changes octs by using self[d]
            * start_note (diatonic, non-diatonic)
        '''
        degrees = self.allowed_degrees()

        for d, _ in enumerate(degrees):

            this = self[ degrees[d] ]

            if this < start_note:
                ## start_note not yet reached
                continue

            # dont yield the Nones before the starting note
            if this != start_note:
                # yield Nones for non-diatonic semitones
                prev = self[ degrees[d-1] ]
                last_interval = this - prev # dont yield last st, yield the note below
                for semitone in range(last_interval - 1):
                    yield None

            yield this

    def spell(self, note_count=None, start_note=None, yield_all=True):
        if note_count == None:
            note_count = len(self.root_intervals)
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, note_order=range(1, len(self.root_intervals) +1),
        )


class DiatonicKey(TonalKey):

    def __getitem__(self, d):

        if d < 1:
            return

        if self.degrees and d not in self.allowed_degrees():
            return

        if d == 1:
            return self.root

        # GET DEGREE's ROOT OFFSETS = OCTAVE + SPARE_STS
        octs_from_root, spare_sts = divmod(
            self.degree_root_interval(d), OCTAVE
        )
        note_oct = octs_from_root

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        next_notes = [
            n for n in EnharmonicMatrix[
                self.root.enharmonic_row + spare_sts
            ] if n.chr == self.root.adjacent_chr(d - 1) # EXPECTED TONE
        ]

        if len(next_notes) == 1:
            # AT THIS POINT DEG_OCT CAN EITHER STAY | +1
            if self.root.oversteps_oct(next_notes[0]):
                note_oct += 1

            # RETURN NEW OBJECT, DO NOT CHANGE ENHARMONIC MATRIX ITEM!
            return Note(next_notes[0].chr, next_notes[0].alt, note_oct)

        raise InvalidNote


########################
### MAJOR KEYS/MODES ###
########################

class MajorKey(DiatonicKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )

class MajorPentatonicKey(MajorKey):
    degrees = (1, 2, 3, 5, 6)

class AugmentedKey(DiatonicKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        AUGMENTED_SIXTH, # <<<
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )

class IonianMode(MajorKey):
    pass

class MixolydianMode(MajorKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH, # <<<
    )


class LydianMode(MajorKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        AUGMENTED_FOURTH, # <<<
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )

########################
### MINOR KEYS/MODES ###
########################

class MinorKey(DiatonicKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )

class DiminishedKey(DiatonicKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        DIMINISHED_FIFTH, # <<<
        MINOR_SIXTH,
        DIMINISHED_SEVENTH, # <<<
    )


class MinorPentatonicKey(MinorKey):
    degrees = (1, 3, 4, 5, 7)

# class Hokkaido(MinorKey):
#     degrees = (1, 2, 3, 4, 5, 6)

class MelodicMinorKey(MinorKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH, # <<<
        MAJOR_SEVENTH, # <<<
    )

class HarmonicMinorKey(MinorKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SEVENTH, # <<<
    )

class AeolianMode(MinorKey):
    pass

class DorianMode(MinorKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH, # <<<
        MINOR_SEVENTH,
    )

class PhrygianMode(MinorKey):
    root_intervals = (
        UNISON,
        MINOR_SECOND, # <<<
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )

class LocrianMode(MinorKey):
    root_intervals = (
        UNISON,
        MINOR_SECOND, # <<<
        MINOR_THIRD,
        PERFECT_FOURTH,
        DIMINISHED_FIFTH, # <<<
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )


####################
### TRIAD CHORDS ###
####################

class MajorTriad(MajorKey):
    degrees = (1, 3, 5)

class MinorTriad(MinorKey):
    degrees = (1, 3, 5)

class AugmentedTriad(AugmentedKey):
    degrees = (1, 3, 5)

class DiminishedTriad(DiminishedKey):
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

class DiminishedSeventhChord(DiminishedKey):
    degrees = (1, 3, 5, 7)


#####################
### CHROMATIC KEY ###
#####################

class ChromaticKey(TonalKey):

    root_intervals = (
        UNISON,
        MINOR_SECOND,
        MAJOR_SECOND,
        MINOR_THIRD,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        AUGMENTED_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH,
        MAJOR_SEVENTH,
    )

    def __getitem__(self, d):

        if d < 1:
            return

        if d == 1:
            return self.root

        # GET DEGREE's ROOT OFFSETS = OCTAVE + SPARE_STS
        octs_from_root, spare_sts = divmod(
            self.degree_root_interval(d), OCTAVE
        )
        note_oct = octs_from_root

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        # DO I REALLY NEED THESE 3 CHECKS ?
        # MATCH ROOT_TONE
        next_notes = [
            n for n in EnharmonicMatrix[
                self.root.enharmonic_row + spare_sts
            ] if n ** self.root
        ]

        if not next_notes:
            # MATCH ROOT_ALT

            next_notes = [
                n for n in EnharmonicMatrix[
                    self.root.enharmonic_row + spare_sts
                ] if n.alt == self.root.alt[:-1]
            ]

            if not next_notes:
                # CHOOSE "#" or ""
                chosen_alt = '#' if self.root.alt == '' else self.root.alt
                next_notes = [
                    n for n in EnharmonicMatrix[
                        self.root.enharmonic_row + spare_sts
                    ] if n.alt == chosen_alt
                ]

        if len(next_notes) == 1:
            # AT THIS POINT DEG_OCT CAN EITHER STAY | +1
            if self.root.oversteps_oct(next_notes[0]):
                note_oct += 1

            # RETURN NEW OBJECT, DO NOT CHANGE ENHARMONIC MATRIX ITEM!
            return Note(next_notes[0].chr, next_notes[0].alt, note_oct)

        raise InvalidNote


SCALES = {
    'major': MajorKey,

    'minor': MinorKey,
    'melodic_minor': MelodicMinorKey,
    'harmonic_minor': HarmonicMinorKey,

    'major_pentatonic': MajorPentatonicKey,
    'minor_pentatonic': MinorPentatonicKey,

    'ionian': IonianMode,
    'lydian': LydianMode,
    'mixo': MixolydianMode,

    'aeolian': AeolianMode,
    'dorian': DorianMode,
    'phrygian': PhrygianMode,
    'locrian': LocrianMode,

    'chromatic': ChromaticKey,
}

CHORDS = {
    'maj': MajorTriad,
    'min': MinorTriad,
    'aug': AugmentedTriad,
    'dim': DiminishedTriad,

    '7': DominantSeventhChord,
    'maj7': MajorSeventhChord,
    'min7': MinorSeventhChord,
    'dim7': DiminishedSeventhChord, # °7  
    'min7dim5': HalfDiminishedSeventhChord, # ⦰7
}
