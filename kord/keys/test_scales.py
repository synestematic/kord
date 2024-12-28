import unittest
import random

from bestia.output import echo, Row, FString

from .scales import (
    ChromaticScale, MajorPentatonicScale, MajorScale,
    MinorScale, MelodicMinorScale, HarmonicMinorScale
)

from ..notes import NotePitch
from ..notes.constants import *

from ..errors import InvalidOctave

__all__ = [
    'ScaleValidityTest',
    'ChromaticScalesTest',
    'MajorScalesExpectedNotesTest',
    'TonalScaleSpellMethodTest',
]


class ScaleValidityTest(unittest.TestCase):

    ''' for a given key, allows to verify:
            * invalid roots
            * octave changes
    '''

    def setUp(self):
        print()

        self.chromatic_key = ChromaticScale
        # test no invalid roots

        self.major_key = MajorScale
        # F𝄫¹ invalid MajorScale
        # B𝄪¹ invalid MajorScale
        # D𝄪¹ invalid MajorScale
        # E𝄪¹ invalid MajorScale
        # G𝄪¹ invalid MajorScale
        # A𝄪¹ invalid MajorScale

        self.minor_key = MinorScale
        # D𝄫² invalid MinorScale
        # F𝄫¹ invalid MinorScale
        # G𝄫¹ invalid MinorScale
        # C𝄫² invalid MinorScale
        # B𝄪¹ invalid MinorScale
        # E𝄪¹ invalid MinorScale

        self.mel_minor_key = MelodicMinorScale
        # F𝄫¹ invalid MelodicMinorScale
        # G𝄫¹ invalid MelodicMinorScale
        # C𝄫² invalid MelodicMinorScale
        # B𝄪¹ invalid MelodicMinorScale
        # D𝄪¹ invalid MelodicMinorScale
        # E𝄪¹ invalid MelodicMinorScale
        # G𝄪¹ invalid MelodicMinorScale
        # A𝄪¹ invalid MelodicMinorScale

        self.har_minor_key = HarmonicMinorScale
        # D𝄫² invalid HarmonicMinorScale
        # F𝄫¹ invalid HarmonicMinorScale
        # G𝄫¹ invalid HarmonicMinorScale
        # C𝄫² invalid HarmonicMinorScale
        # B𝄪¹ invalid HarmonicMinorScale
        # D𝄪¹ invalid HarmonicMinorScale
        # E𝄪¹ invalid HarmonicMinorScale
        # G𝄪¹ invalid HarmonicMinorScale
        # A𝄪¹ invalid HarmonicMinorScale


    def testValidMethod(self):
        for Scale in [self.major_key]:
            assert Scale('c').validate()


    def testValidRoots(self):

        for Scale in [self.major_key,self.minor_key ]:

            echo('\nValid {}s'.format(Scale.__name__), 'underline')

            for note in Scale.valid_root_notes():

                line = Row()
                key = Scale(*note)
                for d in key.spell(
                    note_count=len(key.intervals) +16, yield_all=False
                ):
                    line.append(
                        FString(
                            d,
                            size=5,
                            fg='blue' if not (d.oct % 2) else 'white',
                        )
                    )
                line.echo()


    def testInvalidRoots(self):
        echo('\nInvalid {}s'.format(self.major_key.__name__), 'underline')
        for note in self.major_key.invalid_root_notes():
            echo(
                '{}{} invalid {}'.format(note.chr, note.repr_alt, self.major_key.__name__),
                'red', 'faint'
            )


class ChromaticScalesTest(unittest.TestCase):

    def setUp(self):
        print()
        self.c_chromatic = ChromaticScale('C')
        self.f_sharp_chromatic = ChromaticScale('F', '#')
        self.b_flat_chromatic = ChromaticScale('B', 'b')


    def testIntervalsCount(self):
        assert len(self.c_chromatic.intervals) == 12, self.c_chromatic.intervals
        assert len(self.f_sharp_chromatic.intervals) == 12, self.f_sharp_chromatic.intervals
        assert len(self.b_flat_chromatic.intervals) == 12, self.b_flat_chromatic.intervals


    def testCChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.c_chromatic.spell(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            print(i)
            if i == 1:
                assert note >> C_0, note
            elif i == 2:
                assert note >> C_SHARP_0, note
            elif i == 3:
                assert note >> D_0, note
            elif i == 4:
                assert note >> D_SHARP_0, note
            elif i == 5:
                assert note >> E_0, note
            elif i == 6:
                assert note >> F_0, note
            elif i == 7:
                assert note >> F_SHARP_0, note
            elif i == 8:
                assert note >> G_0, note
            elif i == 9:
                assert note >> G_SHARP_0, note
            elif i == 10:
                assert note >> A_0, note
            elif i == 11:
                assert note >> A_SHARP_0, note
            elif i == 12:
                assert note >> B_0, note
            elif i == 13:
                assert note >> C_1, note
            elif i == 14:
                assert note >> C_SHARP_1, note
            elif i == 15:
                assert note >> D_1, note
            elif i == 16:
                assert note >> D_SHARP_1, note
            elif i == 17:
                assert note >> E_1, note
            elif i == 18:
                assert note >> F_1, note
            elif i == 19:
                assert note >> F_SHARP_1, note
            elif i == 20:
                assert note >> G_1, note
            elif i == 21:
                assert note >> G_SHARP_1, note
            elif i == 22:
                assert note >> A_1, note
            elif i == 23:
                assert note >> A_SHARP_1, note
            elif i == 24:
                assert note >> B_1, note
            elif i == 25:
                assert note >> C_2, note
            # ..............................
            elif i == 97:
                assert note >> C_8, note
            elif i == 98:
                assert note >> C_SHARP_8, note
            elif i == 99:
                assert note >> D_8, note
            elif i == 100:
                assert note >> D_SHARP_8, note
            elif i == 101:
                assert note >> E_8, note
            elif i == 102:
                assert note >> F_8, note
            elif i == 103:
                assert note >> F_SHARP_8, note
            elif i == 104:
                assert note >> G_8, note
            elif i == 105:
                assert note >> G_SHARP_8, note
            elif i == 106:
                assert note >> A_8, note
            elif i == 107:
                assert note >> A_SHARP_8, note
            elif i == 108:
                assert note >> B_8, note
            elif i == 109:
                assert note >> C_9, note
            # ..............................
            elif i == 205:
                assert note >> NotePitch('C', '', 17), note


    def testFSharpChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.f_sharp_chromatic.spell(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note >> F_SHARP_0, note
            elif i == 2:
                assert note >> G_0, note
            elif i == 3:
                assert note >> G_SHARP_0, note
            elif i == 4:
                assert note >> A_0, note
            elif i == 5:
                assert note >> A_SHARP_0, note
            elif i == 6:
                assert note >> B_0, note
            elif i == 7:
                assert note >> C_1, note
            elif i == 8:
                assert note >> C_SHARP_1, note
            elif i == 9:
                assert note >> D_1, note
            elif i == 10:
                assert note >> D_SHARP_1, note
            elif i == 11:
                assert note >> E_1, note
            elif i == 12:
                assert note >> F_1, note
            elif i == 13:
                assert note >> F_SHARP_1, note
            elif i == 14:
                assert note >> G_1, note
            elif i == 15:
                assert note >> G_SHARP_1, note
            elif i == 16:
                assert note >> A_1, note
            elif i == 17:
                assert note >> A_SHARP_1, note
            elif i == 18:
                assert note >> B_1, note
            elif i == 19:
                assert note >> C_2, note
            # ..............................
            elif i == 211:
                assert note >> NotePitch('C', '', 18), note


    def testBFlatChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.b_flat_chromatic.spell(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note >> B_FLAT_0, note
            elif i == 2:
                assert note >> B_0, note
            elif i == 3:
                assert note >> C_1, note
            elif i == 4:
                assert note >> D_FLAT_1, note
            elif i == 5:
                assert note >> D_1, note
            elif i == 6:
                assert note >> E_FLAT_1, note
            elif i == 7:
                assert note >> E_1, note
            elif i == 8:
                assert note >> F_1, note
            elif i == 9:
                assert note >> G_FLAT_1, note
            elif i == 10:
                assert note >> G_1, note
            elif i == 11:
                assert note >> A_FLAT_1, note
            elif i == 12:
                assert note >> A_1, note
            elif i == 13:
                assert note >> B_FLAT_1, note
            elif i == 14:
                assert note >> B_1, note
            elif i == 15:
                assert note >> C_2, note
            # ..............................
            elif i == 200:
                assert note >> NotePitch('F', '', 17), note


class MajorScalesExpectedNotesTest(unittest.TestCase):

    def setUp(self):
        print()
        self.c_major = MajorScale('C')
        self.b_major = MajorScale('B')            # 5 sharps
        self.d_flat_major = MajorScale('D', 'b')  # 5 flats

    def testIntervalsCount(self):
        assert len(self.c_major.intervals) == 7, self.c_major.intervals
        assert len(self.b_major.intervals) == 7, self.b_major.intervals
        assert len(self.d_flat_major.intervals) == 7, self.d_flat_major.intervals


    def testCMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.c_major.spell(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note >> C_0, note
            elif i == 2:
                assert note >> D_0, note
            elif i == 3:
                assert note >> E_0, note
            elif i == 4:
                assert note >> F_0, note
            elif i == 5:
                assert note >> G_0, note
            elif i == 6:
                assert note >> A_0, note
            elif i == 7:
                assert note >> B_0, note
            elif i == 8:
                assert note >> C_1, note
            elif i == 9:
                assert note >> D_1, note
            elif i == 10:
                assert note >> E_1, note
            elif i == 11:
                assert note >> F_1, note
            elif i == 12:
                assert note >> G_1, note
            elif i == 13:
                assert note >> A_1, note
            elif i == 14:
                assert note >> B_1, note
            elif i == 15:
                assert note >> C_2, note
            # ..............................
            elif i == 64:
                assert note >> C_9, note
            elif i == 65:
                assert note >> D_9, note
            elif i == 66:
                assert note >> E_9, note
            elif i == 67:
                assert note >> F_9, note
            elif i == 68:
                assert note >> G_9, note
            elif i == 69:
                assert note >> A_9, note
            elif i == 70:
                assert note >> B_9, note
            elif i == 71:
                assert note >> NotePitch('C', '', 10), note


    def testBMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.b_major.spell(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note >> B_0, note
            elif i == 2:
                assert note >> C_SHARP_1, note
            elif i == 3:
                assert note >> D_SHARP_1, note
            elif i == 4:
                assert note >> E_1, note
            elif i == 5:
                assert note >> F_SHARP_1, note
            elif i == 6:
                assert note >> G_SHARP_1, note
            elif i == 7:
                assert note >> A_SHARP_1, note
            elif i == 8:
                assert note >> B_1, note
            elif i == 9:
                assert note >> C_SHARP_2, note
            elif i == 10:
                assert note >> D_SHARP_2, note
            elif i == 11:
                assert note >> E_2, note
            elif i == 12:
                assert note >> F_SHARP_2, note
            elif i == 13:
                assert note >> G_SHARP_2, note
            elif i == 14:
                assert note >> A_SHARP_2, note
            elif i == 15:
                assert note >> B_2, note
            elif i == 16:
                assert note >> C_SHARP_3, note
            # ..............................
            elif i == 64:
                assert note >> B_9, note
            elif i == 65:
                assert note >> NotePitch('C', '#', 10), note


    def testDFlatMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.d_flat_major.spell(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note >> D_FLAT_0, note
            elif i == 2:
                assert note >> E_FLAT_0, note
            elif i == 3:
                assert note >> F_0, note
            elif i == 4:
                assert note >> G_FLAT_0, note
            elif i == 5:
                assert note >> A_FLAT_0, note
            elif i == 6:
                assert note >> B_FLAT_0, note
            elif i == 7:
                assert note >> C_1, note
            elif i == 8:
                assert note >> D_FLAT_1, note
            elif i == 9:
                assert note >> E_FLAT_1, note
            elif i == 10:
                assert note >> F_1, note
            elif i == 11:
                assert note >> G_FLAT_1, note
            elif i == 12:
                assert note >> A_FLAT_1, note
            elif i == 13:
                assert note >> B_FLAT_1, note
            elif i == 14:
                assert note >> C_2, note
            elif i == 15:
                assert note >> D_FLAT_2, note
            elif i == 16:
                assert note >> E_FLAT_2, note
            # ..............................
            elif i == 64:
                assert note >> D_FLAT_9, note
            elif i == 65:
                assert note >> E_FLAT_9, note
            elif i == 66:
                assert note >> F_9, note
            elif i == 67:
                assert note >> G_FLAT_9, note
            elif i == 68:
                assert note >> A_FLAT_9, note
            elif i == 69:
                assert note >> B_FLAT_9, note
            elif i == 70:
                assert note >> NotePitch('C', '', 10), note


class TonalScaleSpellMethodTest(unittest.TestCase):

    def setUp(self):
        print()
        self.scales = {
            'Ab_chromatic': ChromaticScale('A', 'b'),
            'B_major': MajorScale('B'),
            'Bb_minor': MinorScale('B', 'b'),
            'C_mel_minor': MelodicMinorScale('C'),
            'F#_har_minor': HarmonicMinorScale('F', '#'),
        }

    def testNoteCount(self):
        ''' tests yielded note count is what has been required '''
        for key in self.scales.values():
            max_notes = random.randint(2, 64)
            # max_notes = 65
            print(
                'Testing {}{} {}._count_notes( note_count=1..{} ) ...'.format(
                    key.root.chr, key.root.repr_alt, key.name(), max_notes
                )
            )
            for count in range(max_notes):
                count += 1
                yielded_notes = len(
                    [ n for n in key._count_notes(
                        note_count=count, start_note=None, yield_all=False
                    ) ]
                )
                assert yielded_notes == count, (yielded_notes, count)


    def testDiatonicStartNote(self):
        ''' tests that first yielded note == diatonic start_note '''
        for key in self.scales.values():
            d = random.randint(2, 64)
            print(
                'Testing {}{} {}._count_notes( start_note = note({}) ) ...'.format(
                    key.root.chr, key.root.repr_alt, key.name(), d
                )
            )
            for note in key._count_notes(
                note_count=1, start_note=key[d], yield_all=True
            ):
                assert note >> NotePitch(*key[d]), note


    def testNonDiatonicStartNoteYieldNotes(self):
        ''' tests 1st yielded item == expected diatonic note when:
                * start_note is non-diatonic to the scale
                * Nones ARE NOT being yielded
        '''
        test_parameters = [

            {
                'scale': self.scales['Ab_chromatic'],
                'non_diatonic_note': A_SHARP_1, # enharmonic
                'exp_diatonic_note': B_FLAT_1, # equals
            },

            {
                'scale': self.scales['B_major'],
                'non_diatonic_note': D_1,      # missing note
                'exp_diatonic_note': D_SHARP_1, # next note
            },

            {
                'scale': self.scales['Bb_minor'],
                'non_diatonic_note': D_SHARP_1, # enharmonic
                'exp_diatonic_note': E_FLAT_1, # equals
            },
            {
                'scale': self.scales['C_mel_minor'],
                'non_diatonic_note': F_SHARP_0, # missing note
                'exp_diatonic_note': G_0, # next note
            },
            {
                'scale': self.scales['F#_har_minor'],
                'non_diatonic_note': C_FLAT_4, # enharmonic
                'exp_diatonic_note': B_3, # equals
            },

        ]

        for param in test_parameters:
            key = param['scale']
            non = param['non_diatonic_note']
            exp = param['exp_diatonic_note']
            print(
                'Testing {}{} {}._count_notes( start_note = non_diatonic_note , yield_all = 0 ) ...'.format(
                        key.root.chr, key.root.repr_alt, key.name()
                )
            )
            for note in key._count_notes(
                note_count=1, start_note=non, yield_all=False
            ):
                assert note != None, type(note)         # yield all=False ensures no Nones
                assert note >> NotePitch(*exp), (note, exp)


    def testNonDiatonicStartNoteYieldAll(self):
        ''' tests 1st yielded item == expected value when:
                * start_note is non-diatonic to the scale
                * Nones ARE being yielded
        '''
        test_parameters = [
            {
                'scale': self.scales['Ab_chromatic'],
                'non_diatonic_note': A_SHARP_1, # enharmonic
                'exp_diatonic_note': B_FLAT_1, # equals
            },
            {
                'scale': self.scales['B_major'],
                'non_diatonic_note': D_1,      # missing note
                'exp_diatonic_note': None,              # yields a None, not D#
            },
            {
                'scale': self.scales['Bb_minor'],
                'non_diatonic_note': D_SHARP_1, # enharmonic
                'exp_diatonic_note': E_FLAT_1, # equals
            },
            {
                'scale': self.scales['C_mel_minor'],
                'non_diatonic_note': F_SHARP_0, # missing note
                'exp_diatonic_note': None,              # yields a None, not G
            },
            {
                'scale': self.scales['F#_har_minor'],
                'non_diatonic_note': C_FLAT_4, # enharmonic
                'exp_diatonic_note': B_3, # equals
            },
        ]

        for param in test_parameters:
            key = param['scale']
            non = param['non_diatonic_note']
            exp = param['exp_diatonic_note']

            print(
                'Testing {}{} {}._count_notes( start_note = non_diatonic_note , yield_all = 1 ) ...'.format(
                    key.root.chr, key.root.repr_alt, key.name()
                )
            )

            for note in key._count_notes(
                note_count=1, start_note=non, yield_all=True
            ):
                if note == None:
                    assert note == exp, (note, exp)
                else:
                    assert note >> exp, (note, exp)

                break # test only first yielded value even if not a note


    def testMajorNoneYields(self):
        for i, note in enumerate(MajorScale('C')._count_notes(
            note_count=64, start_note=None, yield_all=True
        )):
            if i == 0:
                assert note >> C_0, note
            elif i == 1:
                assert note == None
            elif i == 2:
                assert note >> D_0, note
            elif i == 3:
                assert note == None
            elif i == 4:
                assert note >> E_0, note
            elif i == 5:
                assert note >> F_0, note
            elif i == 6:
                assert note == None
            elif i == 7:
                assert note >> G_0, note
            elif i == 8:
                assert note == None
            elif i == 9:
                assert note >> A_0, note
            elif i == 10:
                assert note == None
            elif i == 11:
                assert note >> B_0, note
            elif i == 12:
                assert note >> C_1, note


    def testChromaticNoneYields(self):
        ''' tests Chromatic scale does NEVER yield None even with yield_all '''
        for i, note in enumerate(self.scales['Ab_chromatic']._count_notes(
            note_count=128, start_note=None, yield_all=True
        )):
            assert note != None


    def testDegreeOrderOverOct(self):
        for i, note in enumerate(
            MajorScale('A').spell(
            note_count=6,
            start_note=None,
            yield_all=True,
        )):
            i += 1
            if i == 1:
                assert note >> A_0, note
            elif i == 2:
                assert not note, note
            elif i == 3:
                assert note >> B_0, note
            elif i == 4:
                assert not note, note
            elif i == 5:
                assert note >> C_SHARP_1, note
            elif i == 6:
                assert note >> D_1, note
            elif i == 7:
                assert not note, note
            elif i == 8:
                assert note >> E_1, note



    def testCustomDegrees(self):
        '''
        B is not part of C major pentatonic =>
            * 1st note should be None
            * 2nd note should be C
        '''
        for i, note in enumerate(
            MajorPentatonicScale('C').spell(
                yield_all=1,
                start_note=B_3,
                note_count=3
            )
        ):
            i += 1
            if i == 1:
                assert not note, note
            if i == 2:
                assert note, note
                assert note >> C_4, note


    def testMaxOctave(self):
        try:
            note = NotePitch('C', NotePitch.MAXIMUM_OCTAVE + 1)
        except InvalidOctave:
            note = None
        finally:
            assert not note
