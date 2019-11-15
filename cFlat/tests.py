import unittest
from random import randint
# from uuid import uuid4

from instruments import *
from keys import *
from notes import *
from errors import *

# from cFlat.instruments import *
# from cFlat.keys import *
# from cFlat.notes import *
# from cFlat.errors import *

from bestia.output import echo

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
                    notes=len(key._root_intervals) +16, yield_all=False
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

    def testNotEnharmonic(self):
        for note_pair in self.DANGEROUS_NON_EQUALS:
            assert note_pair[0] != note_pair[1]


    def testAreEnharmonic(self):
        ''' checks note_pairs in enharmonic rows
            for different types of equality '''
        for note_pair in EnharmonicMatrix:
            assert note_pair[0] == note_pair[1]
            assert note_pair[0] -  note_pair[1] == 0








class ChromaticKeysTest(unittest.TestCase):

    def setUp(self):
        print()
        self.c_chromatic = ChromaticKey('C')
        self.f_sharp_chromatic = ChromaticKey('F', '#')
        self.b_flat_chromatic = ChromaticKey('B', 'b')

    def testIntervalsCount(self):
        assert len(self.c_chromatic._root_intervals) == 12, self.c_chromatic._root_intervals
        assert len(self.f_sharp_chromatic._root_intervals) == 12, self.f_sharp_chromatic._root_intervals
        assert len(self.b_flat_chromatic._root_intervals) == 12, self.b_flat_chromatic._root_intervals


    def testCChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.c_chromatic.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('C', '', 0), note
            elif i == 2:
                assert note.is_a('C', '#', 0), note
            elif i == 3:
                assert note.is_a('D', '', 0), note
            elif i == 4:
                assert note.is_a('D', '#', 0), note
            elif i == 5:
                assert note.is_a('E', '', 0), note
            elif i == 6:
                assert note.is_a('F', '', 0), note
            elif i == 7:
                assert note.is_a('F', '#', 0), note
            elif i == 8:
                assert note.is_a('G', '', 0), note
            elif i == 9:
                assert note.is_a('G', '#', 0), note
            elif i == 10:
                assert note.is_a('A', '', 0), note
            elif i == 11:
                assert note.is_a('A', '#', 0), note
            elif i == 12:
                assert note.is_a('B', '', 0), note
            elif i == 13:
                assert note.is_a('C', '', 1), note
            elif i == 14:
                assert note.is_a('C', '#', 1), note
            elif i == 15:
                assert note.is_a('D', '', 1), note
            elif i == 16:
                assert note.is_a('D', '#', 1), note
            elif i == 17:
                assert note.is_a('E', '', 1), note
            elif i == 18:
                assert note.is_a('F', '', 1), note
            elif i == 19:
                assert note.is_a('F', '#', 1), note
            elif i == 20:
                assert note.is_a('G', '', 1), note
            elif i == 21:
                assert note.is_a('G', '#', 1), note
            elif i == 22:
                assert note.is_a('A', '', 1), note
            elif i == 23:
                assert note.is_a('A', '#', 1), note
            elif i == 24:
                assert note.is_a('B', '', 1), note
            elif i == 25:
                assert note.is_a('C', '', 2), note
            # ..............................
            elif i == 97:
                assert note.is_a('C', '', 8), note
            elif i == 98:
                assert note.is_a('C', '#', 8), note
            elif i == 99:
                assert note.is_a('D', '', 8), note
            elif i == 100:
                assert note.is_a('D', '#', 8), note
            elif i == 101:
                assert note.is_a('E', '', 8), note
            elif i == 102:
                assert note.is_a('F', '', 8), note
            elif i == 103:
                assert note.is_a('F', '#', 8), note
            elif i == 104:
                assert note.is_a('G', '', 8), note
            elif i == 105:
                assert note.is_a('G', '#', 8), note
            elif i == 106:
                assert note.is_a('A', '', 8), note
            elif i == 107:
                assert note.is_a('A', '#', 8), note
            elif i == 108:
                assert note.is_a('B', '', 8), note
            elif i == 109:
                assert note.is_a('C', '', 9), note
            # ..............................
            elif i == 205:
                assert note.is_a('C', '', 17), note
            elif i == 206:
                assert note.is_a('C', '#', 17), note
            elif i == 207:
                assert note.is_a('D', '', 17), note
            elif i == 208:
                assert note.is_a('D', '#', 17), note
            elif i == 209:
                assert note.is_a('E', '', 17), note
            elif i == 210:
                assert note.is_a('F', '', 17), note
            elif i == 211:
                assert note.is_a('F', '#', 17), note
            elif i == 212:
                assert note.is_a('G', '', 17), note
            elif i == 213:
                assert note.is_a('G', '#', 17), note
            elif i == 214:
                assert note.is_a('A', '', 17), note
            elif i == 215:
                assert note.is_a('A', '#', 17), note
            elif i == 216:
                assert note.is_a('B', '', 17), note
            elif i == 217:
                assert note.is_a('C', '', 18), note


    def testFSharpChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.f_sharp_chromatic.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('F', '#', 0), note
            elif i == 2:
                assert note.is_a('G', '', 0), note
            elif i == 3:
                assert note.is_a('G', '#', 0), note
            elif i == 4:
                assert note.is_a('A', '', 0), note
            elif i == 5:
                assert note.is_a('A', '#', 0), note
            elif i == 6:
                assert note.is_a('B', '', 0), note
            elif i == 7:
                assert note.is_a('C', '', 1), note
            elif i == 8:
                assert note.is_a('C', '#', 1), note
            elif i == 9:
                assert note.is_a('D', '', 1), note
            elif i == 10:
                assert note.is_a('D', '#', 1), note
            elif i == 11:
                assert note.is_a('E', '', 1), note
            elif i == 12:
                assert note.is_a('F', '', 1), note
            elif i == 13:
                assert note.is_a('F', '#', 1), note
            elif i == 14:
                assert note.is_a('G', '', 1), note
            elif i == 15:
                assert note.is_a('G', '#', 1), note
            elif i == 16:
                assert note.is_a('A', '', 1), note
            elif i == 17:
                assert note.is_a('A', '#', 1), note
            elif i == 18:
                assert note.is_a('B', '', 1), note
            elif i == 19:
                assert note.is_a('C', '', 2), note
            # ..............................
            elif i == 211:
                assert note.is_a('C', '', 18), note
            elif i == 212:
                assert note.is_a('C', '#', 18), note
            elif i == 213:
                assert note.is_a('D', '', 18), note
            elif i == 214:
                assert note.is_a('D', '#', 18), note
            elif i == 215:
                assert note.is_a('E', '', 18), note
            elif i == 216:
                assert note.is_a('F', '', 18), note
            elif i == 217:
                assert note.is_a('F', '#', 18), note



    def testBFlatChromaticScaleGenerator(self):

        octaves_to_test = 18
        intervals = 12
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 12 + 1 = 217

        for i, note in enumerate(
            self.b_flat_chromatic.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('B', 'b', 0), note
            elif i == 2:
                assert note.is_a('B', '', 0), note
            elif i == 3:
                assert note.is_a('C', '', 1), note
            elif i == 4:
                assert note.is_a('D', 'b', 1), note
            elif i == 5:
                assert note.is_a('D', '', 1), note
            elif i == 6:
                assert note.is_a('E', 'b', 1), note
            elif i == 7:
                assert note.is_a('E', '', 1), note
            elif i == 8:
                assert note.is_a('F', '', 1), note
            elif i == 9:
                assert note.is_a('G', 'b', 1), note
            elif i == 10:
                assert note.is_a('G', '', 1), note
            elif i == 11:
                assert note.is_a('A', 'b', 1), note
            elif i == 12:
                assert note.is_a('A', '', 1), note
            elif i == 13:
                assert note.is_a('B', 'b', 1), note
            elif i == 14:
                assert note.is_a('B', '', 1), note
            elif i == 15:
                assert note.is_a('C', '', 2), note
            # ..............................
            elif i == 200:
                assert note.is_a('F', '', 17), note
            elif i == 201:
                assert note.is_a('G', 'b', 17), note
            elif i == 202:
                assert note.is_a('G', '', 17), note
            elif i == 203:
                assert note.is_a('A', 'b', 17), note
            elif i == 204:
                assert note.is_a('A', '', 17), note
            elif i == 205:
                assert note.is_a('B', 'b', 17), note
            elif i == 206:
                assert note.is_a('B', '', 17), note
            elif i == 207:
                assert note.is_a('C', '', 18), note
            elif i == 208:
                assert note.is_a('D', 'b', 18), note
            elif i == 209:
                assert note.is_a('D', '', 18), note
            elif i == 210:
                assert note.is_a('E', 'b', 18), note
            elif i == 211:
                assert note.is_a('E', '', 18), note
            elif i == 212:
                assert note.is_a('F', '', 18), note
            elif i == 213:
                assert note.is_a('G', 'b', 18), note
            elif i == 214:
                assert note.is_a('G', '', 18), note
            elif i == 215:
                assert note.is_a('A', 'b', 18), note
            elif i == 216:
                assert note.is_a('A', '', 18), note
            elif i == 217:
                assert note.is_a('B', 'b', 18), note





class MajorKeysExpectedNotesTest(unittest.TestCase):

    def setUp(self):
        print()
        self.c_major = MajorKey('C')
        self.b_major = MajorKey('B')            # 5 sharps
        self.d_flat_major = MajorKey('D', 'b')  # 5 flats

    def testIntervalsCount(self):
        assert len(self.c_major._root_intervals) == 7, self.c_major._root_intervals
        assert len(self.b_major._root_intervals) == 7, self.b_major._root_intervals
        assert len(self.d_flat_major._root_intervals) == 7, self.d_flat_major._root_intervals


    def testCMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.c_major.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('C', '', 0), note
            elif i == 2:
                assert note.is_a('D', '', 0), note
            elif i == 3:
                assert note.is_a('E', '', 0), note
            elif i == 4:
                assert note.is_a('F', '', 0), note
            elif i == 5:
                assert note.is_a('G', '', 0), note
            elif i == 6:
                assert note.is_a('A', '', 0), note
            elif i == 7:
                assert note.is_a('B', '', 0), note
            elif i == 8:
                assert note.is_a('C', '', 1), note
            elif i == 9:
                assert note.is_a('D', '', 1), note
            elif i == 10:
                assert note.is_a('E', '', 1), note
            elif i == 11:
                assert note.is_a('F', '', 1), note
            elif i == 12:
                assert note.is_a('G', '', 1), note
            elif i == 13:
                assert note.is_a('A', '', 1), note
            elif i == 14:
                assert note.is_a('B', '', 1), note
            elif i == 15:
                assert note.is_a('C', '', 2), note
            # ..............................
            elif i == 64:
                assert note.is_a('C', '', 9), note
            elif i == 65:
                assert note.is_a('D', '', 9), note
            elif i == 66:
                assert note.is_a('E', '', 9), note
            elif i == 67:
                assert note.is_a('F', '', 9), note
            elif i == 68:
                assert note.is_a('G', '', 9), note
            elif i == 69:
                assert note.is_a('A', '', 9), note
            elif i == 70:
                assert note.is_a('B', '', 9), note
            elif i == 71:
                assert note.is_a('C', '', 10), note
            # ..............................
            elif i == 120:
                assert note.is_a('C', '', 17), note
            elif i == 121:
                assert note.is_a('D', '', 17), note
            elif i == 122:
                assert note.is_a('E', '', 17), note
            elif i == 123:
                assert note.is_a('F', '', 17), note
            elif i == 124:
                assert note.is_a('G', '', 17), note
            elif i == 125:
                assert note.is_a('A', '', 17), note
            elif i == 126:
                assert note.is_a('B', '', 17), note
            elif i == 127:
                assert note.is_a('C', '', 18), note


    def testBMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.b_major.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('B', '', 0), note
            elif i == 2:
                assert note.is_a('C', '#', 1), note
            elif i == 3:
                assert note.is_a('D', '#', 1), note
            elif i == 4:
                assert note.is_a('E', '', 1), note
            elif i == 5:
                assert note.is_a('F', '#', 1), note
            elif i == 6:
                assert note.is_a('G', '#', 1), note
            elif i == 7:
                assert note.is_a('A', '#', 1), note
            elif i == 8:
                assert note.is_a('B', '', 1), note
            elif i == 9:
                assert note.is_a('C', '#', 2), note
            elif i == 10:
                assert note.is_a('D', '#', 2), note
            elif i == 11:
                assert note.is_a('E', '', 2), note
            elif i == 12:
                assert note.is_a('F', '#', 2), note
            elif i == 13:
                assert note.is_a('G', '#', 2), note
            elif i == 14:
                assert note.is_a('A', '#', 2), note
            elif i == 15:
                assert note.is_a('B', '', 2), note
            elif i == 16:
                assert note.is_a('C', '#', 3), note
            # ..............................
            elif i == 64:
                assert note.is_a('B', '', 9), note
            elif i == 65:
                assert note.is_a('C', '#', 10), note
            elif i == 66:
                assert note.is_a('D', '#', 10), note
            elif i == 67:
                assert note.is_a('E', '', 10), note
            elif i == 68:
                assert note.is_a('F', '#', 10), note
            elif i == 69:
                assert note.is_a('G', '#', 10), note
            elif i == 70:
                assert note.is_a('A', '#', 10), note
            elif i == 71:
                assert note.is_a('B', '', 10), note
            # ..............................
            elif i == 120:
                assert note.is_a('B', '', 17), note
            elif i == 121:
                assert note.is_a('C', '#', 18), note
            elif i == 122:
                assert note.is_a('D', '#', 18), note
            elif i == 123:
                assert note.is_a('E', '', 18), note
            elif i == 124:
                assert note.is_a('F', '#', 18), note
            elif i == 125:
                assert note.is_a('G', '#', 18), note
            elif i == 126:
                assert note.is_a('A', '#', 18), note
            elif i == 127:
                assert note.is_a('B', '', 18), note



    def testDFlatMajorScaleGenerator(self):

        octaves_to_test = 18
        intervals = 7
        notes_to_test = octaves_to_test * intervals + 1  # 18 * 7 + 1 = 127

        for i, note in enumerate(
            self.d_flat_major.scale(
                notes=notes_to_test, yield_all=False
            )
        ):
            i += 1
            if i == 1:
                assert note.is_a('D', 'b', 0), note
            elif i == 2:
                assert note.is_a('E', 'b', 0), note
            elif i == 3:
                assert note.is_a('F', '', 0), note
            elif i == 4:
                assert note.is_a('G', 'b', 0), note
            elif i == 5:
                assert note.is_a('A', 'b', 0), note
            elif i == 6:
                assert note.is_a('B', 'b', 0), note
            elif i == 7:
                assert note.is_a('C', '', 1), note
            elif i == 8:
                assert note.is_a('D', 'b', 1), note
            elif i == 9:
                assert note.is_a('E', 'b', 1), note
            elif i == 10:
                assert note.is_a('F', '', 1), note
            elif i == 11:
                assert note.is_a('G', 'b', 1), note
            elif i == 12:
                assert note.is_a('A', 'b', 1), note
            elif i == 13:
                assert note.is_a('B', 'b', 1), note
            elif i == 14:
                assert note.is_a('C', '', 2), note
            elif i == 15:
                assert note.is_a('D', 'b', 2), note
            elif i == 16:
                assert note.is_a('E', 'b', 2), note
            # ..............................
            elif i == 64:
                assert note.is_a('D', 'b', 9), note
            elif i == 65:
                assert note.is_a('E', 'b', 9), note
            elif i == 66:
                assert note.is_a('F', '', 9), note
            elif i == 67:
                assert note.is_a('G', 'b', 9), note
            elif i == 68:
                assert note.is_a('A', 'b', 9), note
            elif i == 69:
                assert note.is_a('B', 'b', 9), note
            elif i == 70:
                assert note.is_a('C', '', 10), note
            elif i == 71:
                assert note.is_a('D', 'b', 10), note
            elif i == 72:
                assert note.is_a('E', 'b', 10), note
            # ..............................
            elif i == 120:
                assert note.is_a('D', 'b', 17), note
            elif i == 121:
                assert note.is_a('E', 'b', 17), note
            elif i == 122:
                assert note.is_a('F', '', 17), note
            elif i == 123:
                assert note.is_a('G', 'b', 17), note
            elif i == 124:
                assert note.is_a('A', 'b', 17), note
            elif i == 125:
                assert note.is_a('B', 'b', 17), note
            elif i == 126:
                assert note.is_a('C', '', 18), note
            elif i == 127:
                assert note.is_a('D', 'b', 18), note


    def testDegreeMethod(self):
        assert self.c_major.degree(1) == self.c_major[1], 'degree() != __get_item__()'
        assert self.c_major.degree(1).is_a('C'), 'diocane'



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
        ''' tests yielded note count  '''
        for key in self.keys.values():
            print(f'Testing {key.root.chr}{key.root.repr_alt} {key.__class__.__name__}._spell( notes ) argument ...')
            for count in range(64):
                count += 1
                yielded_notes = len(
                    [ n for n in key._spell(
                        notes=count, start_note=None, yield_all=False,
                    ) ]
                )
                assert yielded_notes == count, (yielded_notes, count)


    def testDiatonicStartNote(self):
        ''' tests that first yielded note == diatonic start_note '''
        for key in self.keys.values():
            print(f'Testing {key.root.chr}{key.root.repr_alt} {key.__class__.__name__}._spell( start_note = diatonic_note ) argument ...')
            diatonic_note = key.degree( randint(2, 128) )
            for note in key._spell(
                notes=1, start_note=diatonic_note, yield_all=True
            ): 
                assert note.is_a(*diatonic_note), note


    def testNonDiatonicStartNote(self):
        ''' tests that first yielded note == expected diatonic note,
            when start_note is a note non diatonic to the scale        
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
            print(f'Testing {key.root.chr}{key.root.repr_alt} {key.__class__.__name__}._spell( start_note = non_diatonic_note ) argument ...')
            for note in key._spell(
                notes=1, start_note=non, yield_all=False
            ): 
                # assert note != None, type(note)
                assert note.is_a(*exp), (note, exp)



    # def testNoneYields(self):
    #     for i, note in enumerate(MajorKey('C')._spell(
    #         notes=2, start_note=None, yield_all=True
    #     )):
    #         echo(note, 'yellow')
    #         if i == 0:
    #             assert note.is_a('C', '', 0)
    #         if i == 1:
    #             assert note is None
    #         if i == 2:
    #             assert note.is_a('D', '', 0)
            



if __name__ == '__main__':
    '''
    TDD:
        * write test
        * fail test RED
        * write code
        * pass test GREEN
        * remove duplication REFACTOR
        * pass test
    '''
    unittest.main()
