from bestia.output import Row, FString, echo

from .notes import *

class MusicKey(object):

    intervals = ()
    degrees = ()

    @classmethod
    def allowed_degrees(cls):
        ''' calculates all possible degree numbers for MusicKey

        '''
        if cls.degrees:
            degrees = list(cls.degrees)
        else:
            degrees = [
                n+1 for n in range( len(cls.intervals) )
            ]

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
        for o in range(MAX_OCT):
            for deg in degrees:
                all_degrees.append(
                    deg + len(cls.intervals) * o
                )
        return tuple(all_degrees)

    @classmethod
    def name(cls):
        n = cls.__name__[0]
        for c in cls.__name__[1:]:
            if c.isupper():
                n += ' '
            n += c
        return n

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
        self.root = Note(chr, alt, 0) # ignore note.oct

    def __repr__(self):
        spell_line = Row()
        for d in self.spell(
            note_count=len(self.intervals) +1, yield_all=False
        ):
            spell_line.append(
                FString(d, size=5)
            )
        return str(spell_line)

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
            ) + OCTAVE
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

            * yields based on allowed_degrees
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
            note_count = len(self.intervals)
        return self._count_notes(
            note_count=note_count,
            start_note=start_note,
            yield_all=yield_all,
        )


########################
### MAJOR KEYS/MODES ###
########################

class MajorScale(MusicKey):
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
    degrees = (1, 2, 3, 5, 6)

class AugmentedScale(MusicKey):
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
    pass

class MixolydianMode(MajorScale):
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

class MinorScale(MusicKey):
    intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )

class DiminishedScale(MusicKey):
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
    degrees = (1, 3, 4, 5, 7)

class MelodicMinorScale(MinorScale):
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
    pass

class DorianMode(MinorScale):
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
    intervals = (
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


#####################
### CHROMATIC KEY ###
#####################

class ChromaticScale(MusicKey):

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
