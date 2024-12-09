from bestia.output import Row, FString

from ..notes import MusicNote, notes_by_alts, _EnharmonicMatrix

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

from ..errors import InvalidNote, InvalidOctave

__all__ = [
    'TonalKey',
    'MajorScale',
    'MajorPentatonicScale',
    'AugmentedScale',
    'IonianMode',
    'MixolydianMode',
    'LydianMode',
    'MinorScale',
    'DiminishedScale',
    'MinorPentatonicScale',
    'MelodicMinorScale',
    'HarmonicMinorScale',
    'AeolianMode',
    'DorianMode',
    'PhrygianMode',
    'LocrianMode',
    'ChromaticScale',
]


class TonalKey:

    notations = ()
    intervals = ()
    degrees = ()

    @classmethod
    def allowed_degrees(cls):
        ''' returns list of each degree, once '''
        if cls.degrees:
            return list(cls.degrees)
        return [ n+1 for n in range( len(cls.intervals) ) ]

    @classmethod
    def all_degrees(cls):
        ''' returns list of each degree, over all octaves '''
        degrees = cls.allowed_degrees()

        # floors over-octave degrees into in-octave
        for d, deg in enumerate(degrees):
            if deg > len(cls.intervals):
                degrees[d] -= len(cls.intervals)
                # ie.  9th  => 2nd
                # ie.  11th => 4th

        # remove duplicates
        degrees = list( set(degrees) )

        # sort order
        degrees.sort()

        # calculate all possible octaves
        all_degrees = []
        for o in range(MusicNote.MAXIMUM_OCTAVE):
            for deg in degrees:
                all_degrees.append(
                    deg + len(cls.intervals) * o
                )
        # input(all_degrees)
        return tuple(all_degrees)

    @classmethod
    def name(cls):
        n = ''
        for c in cls.__name__:
            if c.isupper():
                n += ' '
            n += c.lower()
        return n.strip()

    @classmethod
    def __possible_root_notes(cls, valids=True):
        ''' checks all possible notes for validity as root of given key '''
        valid_roots = []
        invalid_roots = []

        for note in notes_by_alts():

            try:
                invalid_root = False
                for _ in cls(*note).spell(
                    note_count=len(cls.intervals) +1,
                    yield_all=False,
                ):
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


    def __init__(self, chr, alt='', oct=0):
        self.root = MusicNote(chr, alt, 0) # ignore note.oct

    def __repr__(self):
        ''' prints first octave of MusicNote items '''
        spell_line = Row()
        for d in self.spell(
            note_count=None, yield_all=False
        ):
            spell_line.append(
                FString(d, size=5)
            )
        return str(spell_line)

    def __getitem__(self, d):

        if d < 1:
            return

        if self.degrees and d not in self.all_degrees():
            return

        if d == 1:
            return self.root

        # GET DEGREE's ROOT OFFSETS = PERFECT_OCTAVE + SPARE_STS
        octs_from_root, spare_sts = divmod(
            self.degree_root_interval(d), PERFECT_OCTAVE
        )
        note_oct = octs_from_root

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        next_notes = [
            n for n in _EnharmonicMatrix[
                self.root.enharmonic_row + spare_sts
            ] if n.chr == self.root.adjacent_chr(d - 1) # EXPECTED TONE
        ]

        if len(next_notes) == 1:
            # AT THIS POINT DEG_OCT CAN EITHER STAY | +1
            if self.root.oversteps_oct(next_notes[0]):
                note_oct += 1

            # RETURN NEW OBJECT, DO NOT CHANGE ENHARMONIC MATRIX ITEM!
            return MusicNote(next_notes[0].chr, next_notes[0].alt, note_oct)

        raise InvalidNote


    def validate(self):
        for note in self.invalid_root_notes():
            if note ** self.root:
                return False
        return True


    def degree_root_interval(self, d):
        ''' return degree's delta semitones from key's root '''
        if d > len(self.intervals):
            return self.degree_root_interval(
                d - len(self.intervals)
            ) + PERFECT_OCTAVE
        return self.intervals[d -1]


    def _count_notes(self, note_count=-1, start_note=None, yield_all=True):
        ''' * returns when note_count == 0
            * positive note_count yields notes exactly
            * negative note_count yields notes indefinetly
            * filters received Nones when needed
        '''
        if not start_note:
            start_note = self.root

        for note in self.__solmizate(start_note=start_note):

            if note_count == 0:
                return

            if note:
                yield note
                note_count -= 1

            elif yield_all:
                yield None


    def __solmizate(self, start_note):
        ''' uses __get_item__ to retrieve notes to yield:
            before yielding a note, calulates semitone
            difference with previous note and yields Nones

            * yields based on all_degrees
            * always yields Nones
            * changes octs by using self[d]
            * start_note (diatonic, non-diatonic)
        '''
        degrees = self.all_degrees()

        for d, _ in enumerate(degrees):

            this = self[ degrees[d] ]

            if this < start_note:
                ## start_note not yet reached
                continue

            #####################################################
            # calculate Nones to yield for non-diatonic semitones
            #####################################################
            if this != start_note: # do not yield the Nones before starting note

                prev = self[ degrees[d-1] ]
                if prev >= start_note:
                    # dont yield last st, yield the note below
                    last_interval = this - prev - 1

                else:
                    # to calculate Nones to yield, dont go all way back to prev
                    # when prev is lower than starting note
                    last_interval = this - start_note

                for semitone in range(last_interval):
                    yield None

            yield this


    def spell(self, note_count=None, start_note=None, yield_all=False):
        if note_count == None:
            note_count = len(self.degrees) if self.degrees else len(self.intervals)
            note_count += 1  # also include next octave root note
        try:
            return self._count_notes(
                note_count=note_count,
                start_note=start_note,
                yield_all=yield_all,
            )
        except InvalidOctave:
            pass


########################
### MAJOR KEYS/MODES ###
########################

class MajorScale(TonalKey):
    notations = (
        'major',
    )
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )

class MajorPentatonicScale(MajorScale):
    notations = (
        'major_pentatonic',
    )
    degrees = (1, 2, 3, 5, 6)

class AugmentedScale(TonalKey):
    notations = (
        'augmented',
    )
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        AUGMENTED_FIFTH, # <<<
        MAJOR_SIXTH,
        MAJOR_SEVENTH,
    )

class IonianMode(MajorScale):
    notations = (
        'ionian',
    )

class MixolydianMode(MajorScale):
    notations = (
        'mixolydian',
    )
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH, # <<<
    )

class LydianMode(MajorScale):
    notations = (
        'lydian',
    )
    intervals = (
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

class MinorScale(TonalKey):
    notations = (
        'minor',
    )
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )

class DiminishedScale(TonalKey):
    notations = (
        'diminished',
    )
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        DIMINISHED_FIFTH, # <<<
        MINOR_SIXTH,
        DIMINISHED_SEVENTH, # <<<
    )

class MinorPentatonicScale(MinorScale):
    notations = (
        'minor_pentatonic',
    )
    degrees = (1, 3, 4, 5, 7)

class MelodicMinorScale(MinorScale):
    notations = (
        'melodic_minor',
    )
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH, # <<<
        MAJOR_SEVENTH, # <<<
    )

class HarmonicMinorScale(MinorScale):
    notations = (
        'harmonic_minor',
    )
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MAJOR_SEVENTH, # <<<
    )

class AeolianMode(MinorScale):
    notations = (
        'aeolian',
    )

class DorianMode(MinorScale):
    notations = (
        'dorian',
    )
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH, # <<<
        MINOR_SEVENTH,
    )

class PhrygianMode(MinorScale):
    notations = (
        'phrygian',
    )
    intervals = (
        UNISON,
        MINOR_SECOND, # <<<
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )

class LocrianMode(MinorScale):
    notations = (
        'locrian',
    )
    intervals = (
        UNISON,
        MINOR_SECOND, # <<<
        MINOR_THIRD,
        PERFECT_FOURTH,
        DIMINISHED_FIFTH, # <<<
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )


#####################
### CHROMATIC KEY ###
#####################

class ChromaticScale(TonalKey):
    notations = (
        'chromatic',
    )
    intervals = (
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

        # GET DEGREE's ROOT OFFSETS = PERFECT_OCTAVE + SPARE_STS
        octs_from_root, spare_sts = divmod(
            self.degree_root_interval(d), PERFECT_OCTAVE
        )
        note_oct = octs_from_root

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        # DO I REALLY NEED THESE 3 CHECKS ?
        # MATCH ROOT_TONE
        next_notes = [
            n for n in _EnharmonicMatrix[
                self.root.enharmonic_row + spare_sts
            ] if n ** self.root
        ]

        if not next_notes:
            # MATCH ROOT_ALT
            next_notes = [
                n for n in _EnharmonicMatrix[
                    self.root.enharmonic_row + spare_sts
                ] if n.alt == self.root.alt[:-1]
            ]

            if not next_notes:
                # CHOOSE "#" or ""
                chosen_alt = '#' if self.root.alt == '' else self.root.alt
                next_notes = [
                    n for n in _EnharmonicMatrix[
                        self.root.enharmonic_row + spare_sts
                    ] if n.alt == chosen_alt
                ]

        if len(next_notes) == 1:
            # AT THIS POINT DEG_OCT CAN EITHER STAY | +1
            if self.root.oversteps_oct(next_notes[0]):
                note_oct += 1

            # RETURN NEW OBJECT, DO NOT CHANGE ENHARMONIC MATRIX ITEM!
            return MusicNote(next_notes[0].chr, next_notes[0].alt, note_oct)

        raise InvalidNote
