from bestia.output import Row, FString, echo

from .notes import *

class TonalKey(object):

    @classmethod
    def Scale(cls, chr, alt=''):
        return cls(chr, alt).scale

    def __init__(self, chr, alt='', oct=0):
        self.root = Note(chr, alt, 0) # ignore note.oct

    def __repr__(self):
        spell_line = Row()
        for d in self.scale(
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
                for _ in cls(*note).scale(note_count=len(cls.root_intervals) +1, yield_all=0):
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


    def _spell(self, note_count=-1, start_note=None, yield_all=True, degree_order=[]):
        ''' 
            * returns when note_count == 0
            * positive note_count yields notes exactly
            * negative note_count yields notes indefinetly
            * filters Nones if needed
        '''
        if not start_note:
            start_note = self.root

        if not degree_order:
            degree_order = [
                n+1 for n in range( len(self.root_intervals) )
            ]

        for note in self._filter_degrees(
            start_note=start_note, degree_order=degree_order
        ):
            if note_count == 0:
                return

            if note:
                yield note
                note_count -= 1

            elif yield_all:
                yield None


    def _filter_degrees(self, start_note=None, degree_order=[]):
        ''' 
            * enforces degree_order for chords, modes, etc
            * yields None when received note is NOT in degrees
        '''
        degrees = [ self[n] for n in degree_order ]

        for _, note in self._solmizate(start_note=start_note):

            # if solmizate sends a None, yield it immediately
            if note == None:
                yield None
                continue

            # if solmizate sends a note, check if it's in degrees and
            # if not, yield a None
            # ensures correct amount of non-diatonic Nones for chords
            note_or_none = None
            for deg in degrees:
                if note ** deg:
                    note_or_none = note
                    break

            yield note_or_none


    def _solmizate(self, start_note):
        '''
        * yields forever
        * always yields 
        * yields degree number
        * changes octs by using self[d]
        * start_note (diatonic, non-diatonic)
        '''
        d = 0
        while True:
            d += 1

            if self[d] < start_note:
                ## start_note not yet reached
                continue

            # dont yield the Nones before the starting note
            if self[d] != start_note:
                # yield Nones non-diatonic semitones
                last_interval = self[d] - self[d-1]
                for semitone in range(last_interval - 1): # dont yield last st, yield the note below
                    yield d, None

            yield d, self[d]


    def scale(self, note_count, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=range(1, len(self.root_intervals) +1),
        )


class DiatonicKey(TonalKey):

    @classmethod
    def Triad(cls, chr, alt=''):
        return cls(chr, alt).triad

    @classmethod
    def SeventhChord(cls, chr, alt=''):
        return cls(chr, alt).seventh

    def __getitem__(self, d):

        if d < 1:
            return

        if d == 1:
            return self.root

        # GET DEGREE's ROOT OFFSETS = OCTAVE + SPARE_STS
        octs_from_root, spare_sts = divmod(
            self.degree_root_interval(d), OCTAVE
        )
        deg_oct = octs_from_root

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        next_degrees = [
            n for n in EnharmonicMatrix[
                self.root.enharmonic_row + spare_sts
            ] if n.chr == self.root.adjacent_chr(d -1) # EXPECTED TONE
        ]

        if len(next_degrees) == 1:
            deg = next_degrees[0]

            # AT THIS POINT DEG_OCT CAN EITHER STAY | +1
            if self.root.oversteps_oct(deg):
                deg_oct += 1

            # RETURN NEW OBJECT, DO NOT CHANGE ENHARMONIC MATRIX ITEM!
            return Note(deg.chr, deg.alt, deg_oct)

        raise InvalidNote


    def triad(self, note_count=3+1, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5),
        )

    def seventh(self, note_count=4+1, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7),
        )

    def ninth(self, note_count=5+1, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7, 9),
        )

    def eleventh(self, note_count=6+1, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7, 9, 11),
        )

    def thirteenth(self, note_count=7+1, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7, 9, 11, 13),
        )


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
    
class MinorPentatonicKey(MinorKey):
    root_intervals = (
        UNISON,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SEVENTH,
    )

class Hokkaido(MinorKey):
    root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
    )


class NaturalMinorKey(MinorKey):
    pass

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

class MajorTriad(DiatonicKey):
    root_intervals = (
        UNISON,
        # MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )

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
        deg_oct = octs_from_root

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        # DO I REALLY NEED THESE 3 CHECKS ?
        # MATCH ROOT_TONE
        next_degrees = [
            n for n in EnharmonicMatrix[
                self.root.enharmonic_row + spare_sts
            ] if n ** self.root
        ]

        if not next_degrees:
            # MATCH ROOT_ALT

            next_degrees = [
                n for n in EnharmonicMatrix[
                    self.root.enharmonic_row + spare_sts
                ] if n.alt == self.root.alt[:-1]
            ]

            if not next_degrees:
                # CHOOSE "#" or ""
                chosen_alt = '#' if self.root.alt == '' else self.root.alt
                next_degrees = [
                    n for n in EnharmonicMatrix[
                        self.root.enharmonic_row + spare_sts
                    ] if n.alt == chosen_alt
                ]

        if len(next_degrees) == 1:

            deg = next_degrees[0] # got from ENH_MATRIX

            # AT THIS POINT DEG_OCT CAN EITHER STAY | +1
            if self.root.oversteps_oct(deg):
                deg_oct += 1

            # RETURN NEW OBJECT, DO NOT CHANGE ENHARMONIC MATRIX ITEM!
            return Note(deg.chr, deg.alt, deg_oct)

        raise InvalidNote

SCALES = {

    'major': MajorKey.Scale,

    'minor': MinorKey.Scale,
    'natural_minor': NaturalMinorKey.Scale,
    'melodic_minor': MelodicMinorKey.Scale,
    'harmonic_minor': HarmonicMinorKey.Scale,

    'ionian': IonianMode.Scale,
    'lydian': LydianMode.Scale,
    'mixo': MixolydianMode.Scale,
    'aeolian': AeolianMode.Scale,
    'dorian': DorianMode.Scale,
    'phrygian': PhrygianMode.Scale,

    # 'hokkaido': Hokkaido.Scale,

    'chromatic': ChromaticKey.Scale,

}

CHORDS = {
    # TRIADS ########################
    'maj': MajorKey.Triad,
    'min': MinorKey.Triad,
    'aug': None,
    'dim': None,

    # SEVENTH #######################
    '7': MixolydianMode.SeventhChord,
    'maj7': MajorKey.SeventhChord,
    'min7': MinorKey.SeventhChord,


    # diminished, °7  
    'dim7': PhrygianMode.SeventhChord,

    # half-diminished, ⦰7
    'min7dim5': PhrygianMode.SeventhChord,

}
