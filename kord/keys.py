from collections import deque

from bestia.output import Row, FString, echo

from kord.notes import *

class TonalKey(object):

    def __init__(self, c, alt='', oct=0):
        self.root = Note(c, alt, 0) # ignore note.oct

    def __repr__(self):
        spell_line = Row()
        for d in self.scale(
            notes=len(self._root_intervals) +1, yield_all=False
        ):
            spell_line.append(
                FString(d, size=5)
            )
        return str(spell_line)

    def __getitem__(self, i):
        return self.degree(i)

    def degree_root_interval(self, d):
        ''' return degree's delta semitones from key's root '''
        if d > len(self._root_intervals):
            return self.degree_root_interval(
                d - len(self._root_intervals)
            ) + OCTAVE
        return self._root_intervals[d -1]

    def _spell(self, notes=0, start_note=None, yield_all=True, degree_order=[]):

        notes_to_yield = notes if notes else len(self._root_intervals)
        start_note = start_note if start_note else self.root
        degree_order = deque(
            [ self[d] for d in degree_order ]
        ) if degree_order else []

        yield_enabled = False
        d = 0
        while notes_to_yield:

            d += 1 # ignore 0

            # DETERMINE WHETHER THRESHOLD_NOTE HAS BEEN REACHED
            if not yield_enabled and self[d] >= start_note:
                yield_enabled = True

                # ROTATE DEGREE_ORDER TO APPROPRIATE_NOTE
                for fd in degree_order:
                    if Note(fd.chr, fd.alt) >= Note(self[d].chr, self[d].alt):
                        degree_order.rotate(
                            0 - degree_order.index(fd)
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

            # DETERMINE WHETHER TO YIELD DEGREE OR NOT
            yield_note = False if degree_order else True
            if degree_order:
                if self[d].is_note(degree_order[0], ignore_oct=True):
                    yield_note = True
                    degree_order.rotate(-1)

            if yield_note:
                yield self[d]
                notes_to_yield -= 1
            elif yield_all:
                yield

    def scale(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, degree_order=range(1, len(self._root_intervals) +1),
        )


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

            # at this point deg_oct can either stay | +1
            if self.root.chr != 'C':

                delta = deg.enharmonic_row - self.root.enharmonic_row

                if deg.enharmonic_row < self.root.enharmonic_row:
                    if not deg.is_note(Note('B', '#'), ignore_oct=1):
                        deg_oct += 1

                elif self.root.is_note(Note('B', '#'), 1):
                    if not deg.is_note(self.root, 1):
                        deg_oct += 1

                elif deg.is_note(Note('C', 'bb'), ignore_oct=1):
                        deg_oct += 1

                elif deg.is_note(Note('C', 'b'), ignore_oct=1):
                        deg_oct += 1

            # RETURN NEW OBJECT, DO NOT CHANGE ENHARMONIC MATRIX ITEM!
            return Note(
                deg.chr,
                deg.alt,
                deg_oct,
            )

        raise InvalidNote


    def triad(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5),
        )

    def seventh(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7),
        )

    def ninth(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7, 9),
        )

    def eleventh(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, degree_order=(1, 3, 5, 7, 9, 11),
        )

    def thirteenth(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
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

    # bla = [
    #     TONE, 
    #     SEMITONE,
    #     TONE, 
    # ]

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

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        # DO I REALLY NEED THESE 3 CHECKS ?
        # MATCH ROOT_TONE
        next_degrees = [
            n for n in EnharmonicMatrix[
                self.root.enharmonic_row + spare_sts
            ] if n.is_note(self.root, ignore_oct=True)
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
            # if Note(deg.chr, deg.alt) == Note('C'): increase_oct()

            # RETURN NEW OBJECT, DO NOT CHANGE OCT OF ENHARMONIC MATRIX ITEM!
            return Note(
                deg.chr,
                deg.alt,
                octs_from_root if deg.enharmonic_row >= self.root.enharmonic_row else octs_from_root +1
            )

        raise InvalidNote
