import unittest
import time
import random

from bestia.output import echo

from .instruments import *

def dbg(t='Waiting...', c='magenta'):
    echo(f'** {t} **', c)
    input()

class KeyValidityTest(unittest.TestCase):

    ''' for a given key, allows to verify:
            * invalid roots        
            * octave changes
    '''

    def setUp(self):
        print()

        self.chromatic_key = ChromaticKey
        # test no invalid roots

        self.major_key = MajorKey
        # F𝄫¹ invalid MajorKey
        # B𝄪¹ invalid MajorKey
        # D𝄪¹ invalid MajorKey
        # E𝄪¹ invalid MajorKey
        # G𝄪¹ invalid MajorKey
        # A𝄪¹ invalid MajorKey

        self.minor_key = NaturalMinorKey
        # D𝄫² invalid NaturalMinorKey
        # F𝄫¹ invalid NaturalMinorKey
        # G𝄫¹ invalid NaturalMinorKey
        # C𝄫² invalid NaturalMinorKey
        # B𝄪¹ invalid NaturalMinorKey
        # E𝄪¹ invalid NaturalMinorKey

        self.mel_minor_key = MelodicMinorKey
        # F𝄫¹ invalid MelodicMinorKey
        # G𝄫¹ invalid MelodicMinorKey
        # C𝄫² invalid MelodicMinorKey
        # B𝄪¹ invalid MelodicMinorKey
        # D𝄪¹ invalid MelodicMinorKey
        # E𝄪¹ invalid MelodicMinorKey
        # G𝄪¹ invalid MelodicMinorKey
        # A𝄪¹ invalid MelodicMinorKey

        self.har_minor_key = HarmonicMinorKey
        # D𝄫² invalid HarmonicMinorKey
        # F𝄫¹ invalid HarmonicMinorKey
        # G𝄫¹ invalid HarmonicMinorKey
        # C𝄫² invalid HarmonicMinorKey
        # B𝄪¹ invalid HarmonicMinorKey
        # D𝄪¹ invalid HarmonicMinorKey
        # E𝄪¹ invalid HarmonicMinorKey
        # G𝄪¹ invalid HarmonicMinorKey
        # A𝄪¹ invalid HarmonicMinorKey


    def testValidRoots(self):

        for Key in [self.major_key,self.minor_key ]:

            echo('\nValid {}s'.format(Key.__name__), 'underline')

            for note in Key.valid_root_notes():

                line = Row()
                key = Key(*note)
                for d in key.scale(
                    note_count=len(key.root_intervals) +16, yield_all=False
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



class NoteEqualityTest(unittest.TestCase):

    DANGEROUS_NON_EQUALS = (
        # ''' Used mainly to test B#, Cd, etc... '''

        (Note('C', 'b', 3), Note('B', '#', 3)),

        (Note('C', 'b', 3), Note('B', '#', 3)),

        (Note('E', 'b', 5), Note('D', '#', 4)),

        (Note('B', '', 5), Note('C', 'b', 4)),

        (Note('E', '#', 3), Note('F', '', 4)),


        (Note('B', 'b'), Note('C', 'bb')),
        (Note('A', '#'), Note('C', 'bb')),

        (Note('B'     ), Note('C', 'b')),
        (Note('A', '##'), Note('C', 'b')),

        (Note('B', '#'), Note('C', '')),
        (Note('B', '#'), Note('D', 'bb')),

        (Note('B', '##'), Note('C', '#')),
        (Note('B', '##'), Note('D', 'b')),


        # these should eval False OK
        (Note('A', '#'), Note('B', 'b', 4)),
        (Note('A', '##'), Note('B', '', 4)),
        (Note('C', ''), Note('D', 'bb', 4)),
        (Note('C', '#'), Note('D', 'b', 4)),
    )

    def setUp(self):
        print()

    def testNotEnharmonic(self):
        for note_pair in self.DANGEROUS_NON_EQUALS:
            assert not note_pair[0] << note_pair[1], (note_pair[0], note_pair[1])
            assert not note_pair[0] >> note_pair[1], (note_pair[0], note_pair[1])
            assert note_pair[0] - note_pair[1] != 0, (note_pair[0], note_pair[1])


    def testAreEnharmonic(self):
        ''' checks note_pairs in enharmonic rows
            for different types of enharmonic equality '''
        for note_pair in EnharmonicMatrix:

            # DO NOT PASS STRICT EQUALITY
            assert not note_pair[0] == note_pair[1], (note_pair[0], note_pair[1])

            # PASS ENHARMONIC EQUALITY
            assert note_pair[0] << note_pair[1], (note_pair[0], note_pair[1])
            assert note_pair[0] >> note_pair[1], (note_pair[0], note_pair[1])

            # CHECK DELTA_ST === 0
            assert not note_pair[0] < note_pair[1], (note_pair[0], note_pair[1])
            assert not note_pair[0] > note_pair[1], (note_pair[0], note_pair[1])

            assert note_pair[0] <= note_pair[1], (note_pair[0], note_pair[1])
            assert note_pair[0] >= note_pair[1], (note_pair[0], note_pair[1])

            assert note_pair[0] - note_pair[1] == 0, (note_pair[0], note_pair[1])


    def testEnharmonicOperators(self):
        ''' '''
        print('Testing enharmonic operators')
        Cs5 = Note('C', '#', 5)
        Db3 = Note('D', 'b', 3)
        Cs3 = Note('C', '#', 3)
        assert Cs3 ** Cs5      # same pitch, OLD is_a(oct=None)
        assert Db3 << Cs3      # enh note
        assert Db3 >> Cs3      # enh note
        assert Cs3 << Db3      # enh note
        assert Cs3 >> Db3      # enh note
        assert not Db3 == Cs3  # same note


        # // enhr note, ignr oct
        # ** same note, ignr oct
        # == same note, same oct
        # << enhr note, same oct


class ChromaticKeysTest(unittest.TestCase):

    def setUp(self):
        print()
        self.c_chromatic = ChromaticKey('C')
        self.f_sharp_chromatic = ChromaticKey('F', '#')
        self.b_flat_chromatic = ChromaticKey('B', 'b')

    def testIntervalsCount(self):
        assert len(self.c_chromatic.root_intervals) == 12, self.c_chromatic.root_intervals
        assert len(self.f_sharp_chromatic.root_intervals) == 12, self.f_sharp_chromatic.root_intervals
        assert len(self.b_flat_chromatic.root_intervals) == 12, self.b_flat_chromatic.root_intervals


    def testCChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.c_chromatic.scale(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note == Note('C', '', 0), note
                # assert note == Note('C', '', 0), note
            elif i == 2:
                assert note == Note('C', '#', 0), note
            elif i == 3:
                assert note == Note('D', '', 0), note
            elif i == 4:
                assert note == Note('D', '#', 0), note
            elif i == 5:
                assert note == Note('E', '', 0), note
            elif i == 6:
                assert note == Note('F', '', 0), note
            elif i == 7:
                assert note == Note('F', '#', 0), note
            elif i == 8:
                assert note == Note('G', '', 0), note
            elif i == 9:
                assert note == Note('G', '#', 0), note
            elif i == 10:
                assert note == Note('A', '', 0), note
            elif i == 11:
                assert note == Note('A', '#', 0), note
            elif i == 12:
                assert note == Note('B', '', 0), note
            elif i == 13:
                assert note == Note('C', '', 1), note
            elif i == 14:
                assert note == Note('C', '#', 1), note
            elif i == 15:
                assert note == Note('D', '', 1), note
            elif i == 16:
                assert note == Note('D', '#', 1), note
            elif i == 17:
                assert note == Note('E', '', 1), note
            elif i == 18:
                assert note == Note('F', '', 1), note
            elif i == 19:
                assert note == Note('F', '#', 1), note
            elif i == 20:
                assert note == Note('G', '', 1), note
            elif i == 21:
                assert note == Note('G', '#', 1), note
            elif i == 22:
                assert note == Note('A', '', 1), note
            elif i == 23:
                assert note == Note('A', '#', 1), note
            elif i == 24:
                assert note == Note('B', '', 1), note
            elif i == 25:
                assert note == Note('C', '', 2), note
            # ..............................
            elif i == 97:
                assert note == Note('C', '', 8), note
            elif i == 98:
                assert note == Note('C', '#', 8), note
            elif i == 99:
                assert note == Note('D', '', 8), note
            elif i == 100:
                assert note == Note('D', '#', 8), note
            elif i == 101:
                assert note == Note('E', '', 8), note
            elif i == 102:
                assert note == Note('F', '', 8), note
            elif i == 103:
                assert note == Note('F', '#', 8), note
            elif i == 104:
                assert note == Note('G', '', 8), note
            elif i == 105:
                assert note == Note('G', '#', 8), note
            elif i == 106:
                assert note == Note('A', '', 8), note
            elif i == 107:
                assert note == Note('A', '#', 8), note
            elif i == 108:
                assert note == Note('B', '', 8), note
            elif i == 109:
                assert note == Note('C', '', 9), note
            # ..............................
            elif i == 205:
                assert note == Note('C', '', 17), note
            elif i == 206:
                assert note == Note('C', '#', 17), note
            elif i == 207:
                assert note == Note('D', '', 17), note
            elif i == 208:
                assert note == Note('D', '#', 17), note
            elif i == 209:
                assert note == Note('E', '', 17), note
            elif i == 210:
                assert note == Note('F', '', 17), note
            elif i == 211:
                assert note == Note('F', '#', 17), note
            elif i == 212:
                assert note == Note('G', '', 17), note
            elif i == 213:
                assert note == Note('G', '#', 17), note
            elif i == 214:
                assert note == Note('A', '', 17), note
            elif i == 215:
                assert note == Note('A', '#', 17), note
            elif i == 216:
                assert note == Note('B', '', 17), note
            elif i == 217:
                assert note == Note('C', '', 18), note


    def testFSharpChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.f_sharp_chromatic.scale(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note == Note('F', '#', 0), note
            elif i == 2:
                assert note == Note('G', '', 0), note
            elif i == 3:
                assert note == Note('G', '#', 0), note
            elif i == 4:
                assert note == Note('A', '', 0), note
            elif i == 5:
                assert note == Note('A', '#', 0), note
            elif i == 6:
                assert note == Note('B', '', 0), note
            elif i == 7:
                assert note == Note('C', '', 1), note
            elif i == 8:
                assert note == Note('C', '#', 1), note
            elif i == 9:
                assert note == Note('D', '', 1), note
            elif i == 10:
                assert note == Note('D', '#', 1), note
            elif i == 11:
                assert note == Note('E', '', 1), note
            elif i == 12:
                assert note == Note('F', '', 1), note
            elif i == 13:
                assert note == Note('F', '#', 1), note
            elif i == 14:
                assert note == Note('G', '', 1), note
            elif i == 15:
                assert note == Note('G', '#', 1), note
            elif i == 16:
                assert note == Note('A', '', 1), note
            elif i == 17:
                assert note == Note('A', '#', 1), note
            elif i == 18:
                assert note == Note('B', '', 1), note
            elif i == 19:
                assert note == Note('C', '', 2), note
            # ..............................
            elif i == 211:
                assert note == Note('C', '', 18), note
            elif i == 212:
                assert note == Note('C', '#', 18), note
            elif i == 213:
                assert note == Note('D', '', 18), note
            elif i == 214:
                assert note == Note('D', '#', 18), note
            elif i == 215:
                assert note == Note('E', '', 18), note
            elif i == 216:
                assert note == Note('F', '', 18), note
            elif i == 217:
                assert note == Note('F', '#', 18), note



    def testBFlatChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.b_flat_chromatic.scale(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note == Note('B', 'b', 0), note
            elif i == 2:
                assert note == Note('B', '', 0), note
            elif i == 3:
                assert note == Note('C', '', 1), note
            elif i == 4:
                assert note == Note('D', 'b', 1), note
            elif i == 5:
                assert note == Note('D', '', 1), note
            elif i == 6:
                assert note == Note('E', 'b', 1), note
            elif i == 7:
                assert note == Note('E', '', 1), note
            elif i == 8:
                assert note == Note('F', '', 1), note
            elif i == 9:
                assert note == Note('G', 'b', 1), note
            elif i == 10:
                assert note == Note('G', '', 1), note
            elif i == 11:
                assert note == Note('A', 'b', 1), note
            elif i == 12:
                assert note == Note('A', '', 1), note
            elif i == 13:
                assert note == Note('B', 'b', 1), note
            elif i == 14:
                assert note == Note('B', '', 1), note
            elif i == 15:
                assert note == Note('C', '', 2), note
            # ..............................
            elif i == 200:
                assert note == Note('F', '', 17), note
            elif i == 201:
                assert note == Note('G', 'b', 17), note
            elif i == 202:
                assert note == Note('G', '', 17), note
            elif i == 203:
                assert note == Note('A', 'b', 17), note
            elif i == 204:
                assert note == Note('A', '', 17), note
            elif i == 205:
                assert note == Note('B', 'b', 17), note
            elif i == 206:
                assert note == Note('B', '', 17), note
            elif i == 207:
                assert note == Note('C', '', 18), note
            elif i == 208:
                assert note == Note('D', 'b', 18), note
            elif i == 209:
                assert note == Note('D', '', 18), note
            elif i == 210:
                assert note == Note('E', 'b', 18), note
            elif i == 211:
                assert note == Note('E', '', 18), note
            elif i == 212:
                assert note == Note('F', '', 18), note
            elif i == 213:
                assert note == Note('G', 'b', 18), note
            elif i == 214:
                assert note == Note('G', '', 18), note
            elif i == 215:
                assert note == Note('A', 'b', 18), note
            elif i == 216:
                assert note == Note('A', '', 18), note
            elif i == 217:
                assert note == Note('B', 'b', 18), note





class MajorKeysExpectedNotesTest(unittest.TestCase):

    def setUp(self):
        print()
        self.c_major = MajorKey('C')
        self.b_major = MajorKey('B')            # 5 sharps
        self.d_flat_major = MajorKey('D', 'b')  # 5 flats

    def testIntervalsCount(self):
        assert len(self.c_major.root_intervals) == 7, self.c_major.root_intervals
        assert len(self.b_major.root_intervals) == 7, self.b_major.root_intervals
        assert len(self.d_flat_major.root_intervals) == 7, self.d_flat_major.root_intervals


    def testCMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.c_major.scale(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note == Note('C', '', 0), note
            elif i == 2:
                assert note == Note('D', '', 0), note
            elif i == 3:
                assert note == Note('E', '', 0), note
            elif i == 4:
                assert note == Note('F', '', 0), note
            elif i == 5:
                assert note == Note('G', '', 0), note
            elif i == 6:
                assert note == Note('A', '', 0), note
            elif i == 7:
                assert note == Note('B', '', 0), note
            elif i == 8:
                assert note == Note('C', '', 1), note
            elif i == 9:
                assert note == Note('D', '', 1), note
            elif i == 10:
                assert note == Note('E', '', 1), note
            elif i == 11:
                assert note == Note('F', '', 1), note
            elif i == 12:
                assert note == Note('G', '', 1), note
            elif i == 13:
                assert note == Note('A', '', 1), note
            elif i == 14:
                assert note == Note('B', '', 1), note
            elif i == 15:
                assert note == Note('C', '', 2), note
            # ..............................
            elif i == 64:
                assert note == Note('C', '', 9), note
            elif i == 65:
                assert note == Note('D', '', 9), note
            elif i == 66:
                assert note == Note('E', '', 9), note
            elif i == 67:
                assert note == Note('F', '', 9), note
            elif i == 68:
                assert note == Note('G', '', 9), note
            elif i == 69:
                assert note == Note('A', '', 9), note
            elif i == 70:
                assert note == Note('B', '', 9), note
            elif i == 71:
                assert note == Note('C', '', 10), note
            # ..............................
            elif i == 120:
                assert note == Note('C', '', 17), note
            elif i == 121:
                assert note == Note('D', '', 17), note
            elif i == 122:
                assert note == Note('E', '', 17), note
            elif i == 123:
                assert note == Note('F', '', 17), note
            elif i == 124:
                assert note == Note('G', '', 17), note
            elif i == 125:
                assert note == Note('A', '', 17), note
            elif i == 126:
                assert note == Note('B', '', 17), note
            elif i == 127:
                assert note == Note('C', '', 18), note


    def testBMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.b_major.scale(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note == Note('B', '', 0), note
            elif i == 2:
                assert note == Note('C', '#', 1), note
            elif i == 3:
                assert note == Note('D', '#', 1), note
            elif i == 4:
                assert note == Note('E', '', 1), note
            elif i == 5:
                assert note == Note('F', '#', 1), note
            elif i == 6:
                assert note == Note('G', '#', 1), note
            elif i == 7:
                assert note == Note('A', '#', 1), note
            elif i == 8:
                assert note == Note('B', '', 1), note
            elif i == 9:
                assert note == Note('C', '#', 2), note
            elif i == 10:
                assert note == Note('D', '#', 2), note
            elif i == 11:
                assert note == Note('E', '', 2), note
            elif i == 12:
                assert note == Note('F', '#', 2), note
            elif i == 13:
                assert note == Note('G', '#', 2), note
            elif i == 14:
                assert note == Note('A', '#', 2), note
            elif i == 15:
                assert note == Note('B', '', 2), note
            elif i == 16:
                assert note == Note('C', '#', 3), note
            # ..............................
            elif i == 64:
                assert note == Note('B', '', 9), note
            elif i == 65:
                assert note == Note('C', '#', 10), note
            elif i == 66:
                assert note == Note('D', '#', 10), note
            elif i == 67:
                assert note == Note('E', '', 10), note
            elif i == 68:
                assert note == Note('F', '#', 10), note
            elif i == 69:
                assert note == Note('G', '#', 10), note
            elif i == 70:
                assert note == Note('A', '#', 10), note
            elif i == 71:
                assert note == Note('B', '', 10), note
            # ..............................
            elif i == 120:
                assert note == Note('B', '', 17), note
            elif i == 121:
                assert note == Note('C', '#', 18), note
            elif i == 122:
                assert note == Note('D', '#', 18), note
            elif i == 123:
                assert note == Note('E', '', 18), note
            elif i == 124:
                assert note == Note('F', '#', 18), note
            elif i == 125:
                assert note == Note('G', '#', 18), note
            elif i == 126:
                assert note == Note('A', '#', 18), note
            elif i == 127:
                assert note == Note('B', '', 18), note



    def testDFlatMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.d_flat_major.scale(
                note_count=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note == Note('D', 'b', 0), note
            elif i == 2:
                assert note == Note('E', 'b', 0), note
            elif i == 3:
                assert note == Note('F', '', 0), note
            elif i == 4:
                assert note == Note('G', 'b', 0), note
            elif i == 5:
                assert note == Note('A', 'b', 0), note
            elif i == 6:
                assert note == Note('B', 'b', 0), note
            elif i == 7:
                assert note == Note('C', '', 1), note
            elif i == 8:
                assert note == Note('D', 'b', 1), note
            elif i == 9:
                assert note == Note('E', 'b', 1), note
            elif i == 10:
                assert note == Note('F', '', 1), note
            elif i == 11:
                assert note == Note('G', 'b', 1), note
            elif i == 12:
                assert note == Note('A', 'b', 1), note
            elif i == 13:
                assert note == Note('B', 'b', 1), note
            elif i == 14:
                assert note == Note('C', '', 2), note
            elif i == 15:
                assert note == Note('D', 'b', 2), note
            elif i == 16:
                assert note == Note('E', 'b', 2), note
            # ..............................
            elif i == 64:
                assert note == Note('D', 'b', 9), note
            elif i == 65:
                assert note == Note('E', 'b', 9), note
            elif i == 66:
                assert note == Note('F', '', 9), note
            elif i == 67:
                assert note == Note('G', 'b', 9), note
            elif i == 68:
                assert note == Note('A', 'b', 9), note
            elif i == 69:
                assert note == Note('B', 'b', 9), note
            elif i == 70:
                assert note == Note('C', '', 10), note
            elif i == 71:
                assert note == Note('D', 'b', 10), note
            elif i == 72:
                assert note == Note('E', 'b', 10), note
            # ..............................
            elif i == 120:
                assert note == Note('D', 'b', 17), note
            elif i == 121:
                assert note == Note('E', 'b', 17), note
            elif i == 122:
                assert note == Note('F', '', 17), note
            elif i == 123:
                assert note == Note('G', 'b', 17), note
            elif i == 124:
                assert note == Note('A', 'b', 17), note
            elif i == 125:
                assert note == Note('B', 'b', 17), note
            elif i == 126:
                assert note == Note('C', '', 18), note
            elif i == 127:
                assert note == Note('D', 'b', 18), note


    def testDegreeMethod(self):
        ''' tests __getitem__ == degree() '''
        degree = self.c_major.degree(1)
        item = self.c_major[1]
        note = Note('C', 0)
        assert degree == item, (degree, item)
        assert degree == note, (degree, note)



class TonalKeySpellMethodTest(unittest.TestCase):

    def setUp(self):
        print()
        self.keys = {
            'Ab_chromatic_key': ChromaticKey('A', 'b'),
            'B_major': MajorKey('B'),
            'Bb_minor': NaturalMinorKey('B', 'b'),
            'C_mel_minor': MelodicMinorKey('C'),
            'F#_har_minor': HarmonicMinorKey('F', '#'),
            # 'E7': SeventhDominant('E'),   # test chords too eventually
        }

    def testNoteCount(self):
        ''' tests yielded note count is what has been required '''
        for key in self.keys.values():
            max_notes = random.randint(2, 64)
            print(f'Testing {key.root.chr}{key.root.repr_alt} {key.__class__.__name__}._spell( note_count=1..{max_notes} ) ...')
            for count in range(max_notes):
                count += 1
                yielded_notes = len(
                    [ n for n in key._spell(
                        note_count=count, start_note=None, yield_all=False, degree_order=[]
                    ) ]
                )
                assert yielded_notes == count, (yielded_notes, count)


    def testDiatonicStartNote(self):
        ''' tests that first yielded note == diatonic start_note '''
        for key in self.keys.values():
            d = random.randint(2, 64)
            print(f'Testing {key.root.chr}{key.root.repr_alt} {key.__class__.__name__}._spell( start_note = degree({d}) ) ...')
            for note in key._spell(
                note_count=1, start_note=key.degree(d), yield_all=True, degree_order=[]
            ): 
                assert note == Note(*key.degree(d)), note


    def testNonDiatonicStartNoteYieldNotes(self):
        ''' tests 1st yielded item == expected diatonic note when:
                * start_note is non-diatonic to the scale
                * Nones ARE NOT being yielded
        '''
        test_parameters = [

            {
                'key': self.keys['Ab_chromatic_key'], 
                'non_diatonic_note': Note('A', '#', 1), # enharmonic
                'exp_diatonic_note': Note('B', 'b', 1), # equals
            },

            {
                'key': self.keys['B_major'], 
                'non_diatonic_note': Note('D', 1),      # missing note
                'exp_diatonic_note': Note('D', '#', 1), # next note
            },

            {
                'key': self.keys['Bb_minor'], 
                'non_diatonic_note': Note('D', '#', 1), # enharmonic
                'exp_diatonic_note': Note('E', 'b', 1), # equals
            },
            {
                'key': self.keys['C_mel_minor'], 
                'non_diatonic_note': Note('F', '#', 0), # missing note
                'exp_diatonic_note': Note('G', '',  0), # next note
            },
            {
                'key': self.keys['F#_har_minor'], 
                'non_diatonic_note': Note('C', 'b', 4), # enharmonic
                'exp_diatonic_note': Note('B', '' , 3), # equals
            },

            # {   # test chords too eventually
            #     'key': self.keys['E7'], 
            #     'non_diatonic_note': Note('A', '', 0), # missing note
            #     'exp_diatonic_note': Note('B', '', 0), # next note
            # },
        ]

        for param in test_parameters:
            key = param['key']
            non = param['non_diatonic_note']
            exp = param['exp_diatonic_note']
            print(f'Testing {key.root.chr}{key.root.repr_alt} {key.__class__.__name__}._spell( start_note = non_diatonic_note , yield_all = 0 ) ...')
            for note in key._spell(
                note_count=1, start_note=non, yield_all=False, degree_order=[]
            ): 
                assert note != None, type(note)         # yield all=False ensures no Nones
                assert note == Note(*exp), (note, exp)


    def testNonDiatonicStartNoteYieldAll(self):
        ''' tests 1st yielded item == expected value when:
                * start_note is non-diatonic to the scale
                * Nones ARE being yielded
        '''
        test_parameters = [
            {
                'key': self.keys['Ab_chromatic_key'], 
                'non_diatonic_note': Note('A', '#', 1), # enharmonic
                'exp_diatonic_note': Note('B', 'b', 1), # equals
            },
            {
                'key': self.keys['B_major'], 
                'non_diatonic_note': Note('D', 1),      # missing note
                'exp_diatonic_note': None,              # yields a None, not D#
            },
            {
                'key': self.keys['Bb_minor'], 
                'non_diatonic_note': Note('D', '#', 1), # enharmonic
                'exp_diatonic_note': Note('E', 'b', 1), # equals
            },
            {
                'key': self.keys['C_mel_minor'], 
                'non_diatonic_note': Note('F', '#', 0), # missing note
                'exp_diatonic_note': None,              # yields a None, not G
            },
            {
                'key': self.keys['F#_har_minor'], 
                'non_diatonic_note': Note('C', 'b', 4), # enharmonic
                'exp_diatonic_note': Note('B', '' , 3), # equals
            },
        ]

        for param in test_parameters:
            key = param['key']
            non = param['non_diatonic_note']
            exp = param['exp_diatonic_note']
            
            print(f'Testing {key.root.chr}{key.root.repr_alt} {key.__class__.__name__}._spell( start_note = non_diatonic_note , yield_all = 1 ) ...')
            
            for note in key._spell(
                note_count=1, start_note=non, yield_all=True, degree_order=[]
            ):

                assert note == exp, (note, exp)
                # if note is not None:
                #     assert note == Note(*exp), (note, exp)

                break # test only first yielded value even if not a note
                

    def testMajorNoneYields(self):
        for i, note in enumerate(MajorKey('C')._spell(
            note_count=64, start_note=None, yield_all=True, degree_order=[]
        )):
            # echo(note, 'yellow')
            if i == 0:
                assert note == Note('C', '', 0), note
            elif i == 1:
                assert note is None
            elif i == 2:
                assert note == Note('D', '', 0), note
            elif i == 3:
                assert note is None
            elif i == 4:
                assert note == Note('E', '', 0), note
            elif i == 5:
                assert note == Note('F', '', 0), note
            elif i == 6:
                assert note is None
            elif i == 7:
                assert note == Note('G', '', 0), note
            elif i == 8:
                assert note is None
            elif i == 9:
                assert note == Note('A', '', 0), note
            elif i == 10:
                assert note is None
            elif i == 11:
                assert note == Note('B', '', 0), note
            elif i == 12:
                assert note == Note('C', '', 1), note


    def testChromaticNoneYields(self):
        ''' tests Chromatic scale does NEVER yield None even with yield_all '''
        for i, note in enumerate(self.keys['Ab_chromatic_key']._spell(
            note_count=128, start_note=None, yield_all=True, degree_order=[]
        )):
            assert note != None


    def testDegreeOrder(self):
        sn = Note('C', '', 0)
        for i, note in enumerate(MajorKey('C')._spell(
            note_count=23, start_note=sn, yield_all=False, degree_order=[1, 3, 5, 7]
        )):
            echo(f'{note}  ', 'yellow', mode='raw')
            # time.sleep(0.3)


    def testDegreeOrderOverOct(self):
        for i, note in enumerate(MajorKey('C').ninth(
            note_count=6, start_note=None, yield_all=False
        )):
            i += 1
            if i == 1:
                assert note == Note('C', '', 0), note
            # elif i == 2:
            #     assert note == Note('E', '', 0), note
            # elif i == 3:
            #     assert note == Note('G', '', 0), note
            # elif i == 4:
            #     assert note == Note('B', '', 0), note
            # elif i == 5:
            #     assert note == Note('D', '', 1), note
            # elif i == 6:
            #     assert note == Note('C', '', 2), note


