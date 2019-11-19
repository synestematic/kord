from collections import deque

from bestia.output import Row, FString, echo

from .notes import *
# from cFlat.notes import *

class TonalKey(object):

    def __init__(self, c, alt='', oct=0):
        self.root = Note(c, alt, 0) # ignore note.oct

    def __repr__(self):
        spell_line = Row()
        for d in self.scale(
            note_count=len(self._root_intervals) +1, yield_all=False
        ):
            spell_line.append(
                FString(d, size=5)
            )
        return str(spell_line)

    def __getitem__(self, i):
        return self.degree(i)


    @classmethod
    def __possible_root_notes(cls, valids=True):
        ''' checks all possible notes for validity as root of given key '''
        valid_roots = []
        invalid_roots = []

        for note in notes_by_alts():
            try:
                invalid_root = False
                for _ in cls(*note).scale(yield_all=0):
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
        if d > len(self._root_intervals):
            return self.degree_root_interval(
                d - len(self._root_intervals)
            ) + OCTAVE
        return self._root_intervals[d -1]


    def _spell(self, note_count=0, start_note=None, yield_all=True, degree_order=[]):
        '''
            features to support:
                * yield notes count
                * octave change, BUT degree() takes care of it
                * diatonic start_note
                * non-diatonic start_note
                * yield None for empty semi-tones
                * degree order for chords, modes, etc
        '''

        notes_to_yield = note_count if note_count else len(self._root_intervals)
        start_note = start_note if start_note else self.root

        degree_order = deque(
            [ self[d] for d in degree_order ]
        ) if degree_order else []

        d = 0
        # yield_enabled = False
        while notes_to_yield:
            d += 1

            # DETERMINE WHETHER THRESHOLD_NOTE HAS BEEN REACHED
            if self[d] < start_note:
                continue

            # CALCULATE AND YIELD NON-DIATONIC SEMITONES
            # DO NOT CALCULATE PREV_INT ON ROOT DEGREE
            previous_interval = 0 if d == 1 else self[d] - self[d -1]

            # AVOID YIELDING EXTRA NONE BEFORE START_NOTE
            # WHEN SCALE DEG BEFORE IS > 1ST AWAY
            if yield_all and self[d] != start_note:
                for st in range(previous_interval -1):
                    yield


            yield self[d]
            notes_to_yield -= 1







    def __oldspell(self, note_count=0, start_note=None, yield_all=True, degree_order=[]):

        while notes_to_yield:
            d += 1
            if not yield_enabled and self[d] >= start_note:
                yield_enabled = True

                # ROTATE DEGREE_ORDER TO APPROPRIATE_NOTE
                for o, _ in enumerate(degree_order):

                    if self.__check_degree_order(self[d].chr, o, degree_order):
                        degree_order.rotate(
                            0 - degree_order.index(
                                degree_order[o]
                            ) - 1
                        )
                        break

            if not yield_enabled:
                continue


            # CALCULATE AND YIELD NON-DIATONIC SEMITONES
            # DO NOT CALCULATE PREV_INT ON ROOT DEGREE
            previous_interval = 0 if d == 1 else self[d] - self[d -1]

            # AVOID YIELDING EXTRA NONE BEFORE START_NOTE
            # WHEN SCALE DEG BEFORE IS > 1ST AWAY
            if yield_all and self[d] != start_note:
                for st in range(previous_interval -1):
                    yield

            # DETERMINE WHETHER TO YIELD DEGREE OR NONE
            yield_note = False if degree_order else True
            if degree_order:
                if self[d].is_a(degree_order[0].chr, degree_order[0].alt):
                    yield_note = True
                    degree_order.rotate(-1)

            if yield_note:
                yield self[d]
                notes_to_yield -= 1
            elif yield_all:
                yield


    def __check_degree_order(self, check_chr, o, degree_order):
        ''' helper function to spell method
            checks degree order items one at a time
            to decide when it's time to rotate
        '''

        c = 1
        while True:

            d_next_char = degree_order[o].adjacent_chr(c)

            if d_next_char  == check_chr:
                # found rotate position
                return True

            if d_next_char == degree_order[o + 1].chr:
                # reached next degree_order.chr
                return

            c += 1



    def scale(self, note_count=0, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=range(1, len(self._root_intervals) +1),
        )


    def is_diatonic(self, note):
        ''' checks if a note object is a degree in the scale,
            returns degree number
        '''
        for d, degree in enumerate(self.scale(yield_all=False, note_count=666)):
            d += 1
            if note == degree:
                return d


class DiatonicKey(TonalKey):

    def degree(self, d):

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


    def triad(self, note_count=0, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5),
        )

    def seventh(self, note_count=0, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7),
        )

    def ninth(self, note_count=0, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7, 9),
        )

    def eleventh(self, note_count=0, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7, 9, 11),
        )

    def thirteenth(self, note_count=0, start_note=None, yield_all=True):
        return self._spell(
            note_count=note_count, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7, 9, 11, 13),
        )


########################
### MAJOR KEYS/MODES ###
########################

class MajorKey(DiatonicKey):

    _root_intervals = (
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

    _root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH, # <<<
    )

class LydianMode(MajorKey):

    _root_intervals = (
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

    _root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )
    
class MinorPentatonicKey(MinorKey):

    _root_intervals = (
        UNISON,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SEVENTH,
    )

class Hokkaido(MinorKey):

    _root_intervals = (
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

    _root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH, # <<<
        MAJOR_SEVENTH, # <<<
    )

class HarmonicMinorKey(MinorKey):

    _root_intervals = (
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

    _root_intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH, # <<<
        MINOR_SEVENTH,
    )

class PhrygianMode(MinorKey):

    _root_intervals = (
        UNISON,
        MINOR_SECOND, # <<<
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )


#####################
### CHROMATIC KEY ###
#####################

class ChromaticKey(TonalKey):

    _root_intervals = (
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

    def degree(self, d):

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
            ] if n.is_a(self.root.chr, self.root.alt)
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
