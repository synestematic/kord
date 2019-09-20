from collections import deque

from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

from kord.notes import *

class TonalKey(object):

    def __init__(self, tone, alt='', oct=0):
        # Major F##, C## work - G## dies...
        self.root = Note(tone, alt, 0)


    def __repr__(self):
        spell_line = Row()
        for d in self.scale(
            notes=len(self._intervals) +1, yield_all=False
        ):
            spell_line.append(
                FString(d, size=5)
            )
        return str(spell_line)


    def interval_from_root(self, d):
        ''' return degree's delta semitones from key's root '''
        if d > len(self._intervals):
            return self.interval_from_root(
                d - len(self._intervals)
            ) + OCTAVE
        return self._intervals[d -1]


    def _spell(self, notes=0, start_note=None, yield_all=True, filter_degrees=[]):

        notes_to_yield = notes if notes else len(self._intervals)
        start_note = start_note if start_note else self.root
        filter_degrees = deque(
            [ self.degree(d) for d in filter_degrees ]
        ) if filter_degrees else []

        yield_enabled = False
        d = 0
        while notes_to_yield:

            d += 1 # ignore 0

            degree = self.degree(d)
            if not degree:
                raise InvalidChord()

            # DETERMINE WHETHER THRESHOLD_NOTE HAS BEEN REACHED
            if not yield_enabled and degree >= start_note:
                yield_enabled = True

                # ROTATE FILTER_DEGREES TO APPROPRIATE_NOTE
                for fd in filter_degrees:
                    if Note(fd.tone, fd.alt) >= Note(degree.tone, degree.alt):
                        filter_degrees.rotate(
                            0 - filter_degrees.index(fd)
                        )
                        break

            if not yield_enabled:
                continue

            # CALCULATE AND YIELD NON-DIATONIC SEMITONES
            last_note_delta = self.interval_from_root(d) - self.interval_from_root(d -1)
            if last_note_delta > SEMITONE:
                for st in range(last_note_delta -1):
                    if yield_all and degree != start_note:
                        # AVOID YIELDING EXTRA NONE BEFORE START_NOTE
                        # WHEN SCALE DEG BEFORE IS > 1ST AWAY
                        yield None

            # DETERMINE WHETHER TO YIELD A DEGREE OR NOT
            yield_note = False if filter_degrees else True
            if filter_degrees:
                if degree.is_note(filter_degrees[0], ignore_oct=True):
                    yield_note = True
                    filter_degrees.rotate(-1)

            if yield_note:
                yield degree
                notes_to_yield -= 1
            else:
                if yield_all:
                    yield None

    def scale(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, filter_degrees=range(1, len(self._intervals) +1),
        )

    # def scale(self, notes=0, start_note=None, yield_all=True):
    #     ''' document better........
    #     yields Notes for diatonic degrees
    #     if all is set, Nones are yield for empty semi-tones '''

    #     notes_to_yield = notes if notes else len(self._intervals)
    #     start_note = start_note if start_note else self.root

    #     yield_enabled = False
    #     d = 0
    #     while notes_to_yield:

    #         d += 1 # ignore 0

    #         degree = self.degree(d)
    #         if not degree:
    #             raise InvalidScale(
    #                 '{}{} {}'.format(
    #                     self.root.tone,
    #                     self.root.repr_alt,
    #                     self.__class__.__name__,
    #                 )
    #             )

    #         if not yield_enabled and degree >= start_note:
    #             yield_enabled = True
    #         # DETERMINE WHETHER THRESHOLD_NOTE HAS BEEN REACHED
    #         if not yield_enabled:
    #             continue

    #         last_note_delta = self.interval_from_root(d) - self.interval_from_root(d -1)
    #         if last_note_delta > SEMITONE:
    #             for st in range(last_note_delta -1):
    #                 if yield_all and degree != start_note:
    #                     # AVOID YIELDING EXTRA NONE BEFORE START_NOTE
    #                     # WHEN SCALE DEG BEFORE IS > 1ST AWAY
    #                     yield None

    #         notes_to_yield -= 1
    #         yield degree


class DiatonicKey(TonalKey):

    def degree(self, d):

        if d == 1:
            return self.root

        # GET DEGREE's ROOT OFFSETS = OCTAVE + SPARE_STS
        octs_from_root, spare_sts = divmod(
            self.interval_from_root(d), OCTAVE
        )

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        next_degrees = [
            n for n in looped_list_item(
                self.root.enharmonic_row + spare_sts,
                ENHARMONIC_MATRIX
            ) if n.tone == self.root.adjacent_tone(d -1) # EXPECTED TONE
        ]

        if len(next_degrees) == 1:
            deg = next_degrees[0]
            # if deg.tone == 'C': increase_oct()
        
            # RETURN NEW OBJECT, DO NOT CHANGE OCT OF ENHARMONIC_MATRIX ITEM!
            return Note(
                deg.tone,
                deg.alt,
                octs_from_root if deg.enharmonic_row >= self.root.enharmonic_row else octs_from_root +1
            )


    def triad(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, filter_degrees=(1, 3, 5),
        )

    def seventh(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, filter_degrees=(1, 3, 5, 7),
        )

    def ninth(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, filter_degrees=(1, 3, 5, 7, 9),
        )

    def eleventh(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, filter_degrees=(1, 3, 5, 7, 9, 11),
        )

    def thirteenth(self, notes=0, start_note=None, yield_all=True):
        return self._spell(
            notes=notes, start_note=start_note,
            yield_all=yield_all, filter_degrees=(1, 3, 5, 7, 9, 11, 13),
        )


########################
### MAJOR KEYS/MODES ###
########################

class MajorKey(DiatonicKey):

    _intervals = (
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

    _intervals = (
        UNISON,
        MAJOR_SECOND,
        MAJOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH,
        MINOR_SEVENTH, # <<<
    )

class LydianMode(MajorKey):

    _intervals = (
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

    _intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )
    
class NaturalMinorKey(MinorKey):
    pass

class MelodicMinorKey(MinorKey):

    _intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH, # <<<
        MAJOR_SEVENTH, # <<<
    )

class HarmonicMinorKey(MinorKey):

    _intervals = (
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

    _intervals = (
        UNISON,
        MAJOR_SECOND,
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MAJOR_SIXTH, # <<<
        MINOR_SEVENTH,
    )

class PhrygianMode(MinorKey):

    _intervals = (
        UNISON,
        MINOR_SECOND, # <<<
        MINOR_THIRD,
        PERFECT_FOURTH,
        PERFECT_FIFTH,
        MINOR_SIXTH,
        MINOR_SEVENTH,
    )



class ChromaticKey(TonalKey):

    _intervals = (
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

        if d == 1:
            return self.root

        # GET DEGREE's ROOT OFFSETS = OCTAVE + SPARE_STS
        octs_from_root, spare_sts = divmod(
            self.interval_from_root(d), OCTAVE
        )

        # GET DEGREE PROPERTIES FROM ENHARMONIC MATRIX
        # DO I REALLY NEED THESE 3 CHECKS ?
        # MATCH ROOT_TONE
        next_degrees = [
            n for n in looped_list_item(
                self.root.enharmonic_row + spare_sts,
                ENHARMONIC_MATRIX
            ) if n.is_note(self.root, ignore_oct=True)
        ]

        if not next_degrees:
            # MATCH ROOT_ALT
            next_degrees = [
                n for n in looped_list_item(
                    self.root.enharmonic_row + spare_sts,
                    ENHARMONIC_MATRIX
                ) if n.alt == self.root.alt[:-1]
            ]

            if not next_degrees:
                # CHOOSE "#" or ""
                chosen_alt = '#' if self.root.alt == '' else self.root.alt
                next_degrees = [
                    n for n in looped_list_item(
                        self.root.enharmonic_row + spare_sts,
                        ENHARMONIC_MATRIX
                    ) if n.alt == chosen_alt
                ]

        if len(next_degrees) == 1:

            deg = next_degrees[0] # got from ENH_MATRIX
            # if Note(deg.tone, deg.alt) == Note('C'): increase_oct()

            # RETURN NEW OBJECT, DO NOT CHANGE OCT OF ENHARMONIC_MATRIX ITEM!
            return Note(
                deg.tone,
                deg.alt,
                octs_from_root if deg.enharmonic_row >= self.root.enharmonic_row else octs_from_root +1
            )
