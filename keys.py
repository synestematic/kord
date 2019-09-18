from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

from notes import *

class TonalKey(object):

    def __init__(self, tone, alt='', oct=0):
        # Major F##, C## work - G## dies...
        self.current_oct = 0
        self.root = Note(tone, alt, 0)


    def __repr__(self):
        spell_line = Row()
        for d in self.scale(notes=len(self._intervals) +1, all=False):
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


    def scale(self, notes=0, start=None, all=True):
        ''' document better........
        yields Notes for diatonic degrees
        if all is set, Nones are yield for empty semi-tones '''

        # self.current_oct = 0

        notes_to_yield = notes if notes else len(self._intervals)
        start_note = start if start else self.root

        yield_enabled = False
        d = 1 # ignore 0
        while notes_to_yield:

            # IMMEDIATELY DETERMINE WHETHER YIELD MUST BE ENABLED
            degree = self.degree(d)
            # echo(degree, mode='raw')
            if not yield_enabled and degree >= start_note:
                yield_enabled = True

            last_note_delta = self.interval_from_root(d) - self.interval_from_root(d -1)
            if last_note_delta > SEMITONE:
                for st in range(last_note_delta -1):
                    if yield_enabled and all:

                        if degree != start_note:
                        # AVOID YIELDING EXTRA NONE @START_NOTE
                        # WHEN SCALE DEG BEFORE IS > 1ST AWAY
                            yield None

            if yield_enabled:
                notes_to_yield -= 1
                yield degree

            d += 1



    # def _chord(self, root=1, count=3):
    #     n = root
    #     for c in range(count):
    #         yield self.degree(n)
    #         n += 2
  
    # def triad(self, root=1):
    #     return self._chord(root, count=3)

    # def seventh(self, root=1):
    #     return self._chord(root, count=4)

    # def ninth(self, root=1):
    #     return self._chord(root, count=5)

    # def eleventh(self, root=1):
    #     return self._chord(root, count=6)

    # def thirteenth(self, root=1):
    #     return self._chord(root, count=7)


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
            # large intervals that do not hace C will need to compare last and next
            # if deg.tone == 'C':
            #     self.current_oct += 1

            # RETURN NEW OBJECT, DO NOT CHANGE OCT OF ENHARMONIC_MATRIX ITEM!
            return Note(
                deg.tone,
                deg.alt,
                octs_from_root if deg.enharmonic_row >= self.root.enharmonic_row else octs_from_root +1
            )

        raise InvalidScale(
            '{}{} {}'.format(
                self.root.tone,
                self.root.repr_alt,
                self.__class__.__name__,
            )
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

        row_index = self.root.enharmonic_row + self.interval_from_root(d)

        # better also here to get an "expected_tone"

        #  DO I REALLY NEED THESE 3 CHECKS ?

        next_degrees = [
            note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.is_note(self.root, ignore_oct=True)
        ]

        if not next_degrees:
            next_degrees = [
                note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == self.root.alt[:-1]
            ]

            if not next_degrees:
                chosen_alt = '#' if self.root.alt == '' else self.root.alt
                next_degrees = [
                    note for note in looped_list_item(row_index, ENHARMONIC_MATRIX) if note.alt == chosen_alt
                ]

        if len(next_degrees) == 1:

            deg = next_degrees[0] # got from ENH_MATRIX

            if Note(deg.tone, deg.alt) == Note('C'):
                self.current_oct += 1

            # init new note, DO NOT change octave of ENHARMONIC_MATRIX note!
            return Note(
                deg.tone, deg.alt, self.current_oct
            )

        raise InvalidScale(
            '{}{} {}'.format(
                self.root.tone,
                self.root.repr_alt,
                self.__class__.__name__,
            )
        )

