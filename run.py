from argparse import ArgumentParser
from bestia.output import echo

from cFlat import *

TUNINGS = {

    # COMMON TUNINGS
    'gtr': [
        ('E', 4),
        ('B', 3),
        ('G', 3),
        ('D', 3),
        ('A', 2),
        ('E', 2),
    ],
    'dropDgtr': [
        ('E', 4),
        ('B', 3),
        ('G', 3),
        ('D', 3),
        ('A', 2),
        ('D', 2),
    ],
    '7stringgtr': [
        ('E', 4),
        ('B', 3),
        ('G', 3),
        ('D', 3),
        ('A', 2),
        ('E', 2),
        ('B', 1),
    ],

    # OPEN TUNINGS
    'openEgtr': [
        ('E', 4),
        ('B', 3),
        ('G', '#', 3),
        ('E', 3),
        ('B', 2),
        ('E', 2),
    ],
    'openDgtr': [
        ('D', 4),
        ('A', 3),
        ('F', '#', 3),
        ('D', 3),
        ('A', 2),
        ('D', 2),
    ],
    'openGgtr': [
        ('D', 4),
        ('B', 3),
        ('G', 3),
        ('D', 3),
        ('G', 2),
        ('D', 2),
    ],
    'openF#gtr': [
        ('C', '#', 4),
        ('A', '#', 3),
        ('F', '#', 3),
        ('C', '#', 3),
        ('F', '#', 2),
        ('C', '#', 2),
    ],

    # OTHER INSTRUMENTS
    'bass': [
        ('G', 2),
        ('D', 2),
        ('A', 1),
        ('E', 1),
        # ('B', 0),
    ],
    '5stringbass': [
        ('G', 2),
        ('D', 2),
        ('A', 1),
        ('E', 1),
        ('B', 0),
    ],
    '6stringbass': [
        ('C', 3),
        ('G', 2),
        ('D', 2),
        ('A', 1),
        ('E', 1),
        ('B', 0),
    ],
    'ukulele': [
        ('A', 3),
        ('E', 3),
        ('C', 3),
        ('G', 3),
    ],
    'banjo': [
        ('D', 3),
        ('B', 2),
        ('G', 2),
        ('D', 2),
    ],

}

TONAL_CLASSES = {

    'major': MajorKey,

    'minor': MinorKey,
    'natural_minor': NaturalMinorKey,
    'melodic_minor': MelodicMinorKey,
    'harmonic_minor': HarmonicMinorKey,

    'ionian': IonianMode,
    'lydian': LydianMode,
    'mixo': MixolydianMode,
    'aeolian': AeolianMode,
    'dorian': DorianMode,
    'phrygian': PhrygianMode,

    # 'hokkaido': Hokkaido,

}


# CHORDS = {
#     # TRIADS ########################
#     '': MajorTriadChord,
#     'M': MajorTriadChord,

#     'm': MinorTriadChord,

#     'a': AugmentedTriadChord,
    #  '+': AugmentedTriadChord,

#     'd': DiminishedTriadChord,
#     '-': DiminishedTriadChord,

#     # SEVENTH #######################
#     '7': DominantSeventhChord,
#     'dom7': DominantSeventhChord,

#     'M7': MajorSeventhChord,
#     'maj7': MajorSeventhChord,
#     '△7': MajorSeventhChord,

#     'm7': MinorSeventhChord,
#     'min7': MinorSeventhChord,
    
#     'D7': DiminishedSeventhChord,
#     'dim7': DiminishedSeventhChord,
#     '°7': DiminishedSeventhChord,

#     'd7': HalfDiminishedSeventhChord, # isnt this one usually used for diminished (instead of D7)?
#     'm7-5': HalfDiminishedSeventhChord,
#     '⦰7': HalfDiminishedSeventhChord,

# }

def parse_arguments():
    parser = ArgumentParser(
        description = 'fretboard',
    )
    parser.add_argument('note')

    parser.add_argument(
        '-i', '--instrument',
        help = 'set instrument & tuning',
        choices=TUNINGS.keys(),
        default=list(
            TUNINGS.keys()
        )[0],
    )

    parser.add_argument(
        '-f', '--frets',
        help = 'number of frets to display',
        type = int,
        default=max_frets_on_screen()
    )
    parser.add_argument(
        '-v', '--verbosity',
        help = 'amount of verbosity',
        choices=(0, 1, 2),
        type = int,
        default=1
    )
    parser.add_argument(
        '-t', '--tonality',   # --key ??
        help = 'tonality to display',
        default='major'
    )

    parser.add_argument(
        '-c', '--chord',
        help = 'chord to display',
    )

    args = parser.parse_args()

    instrument = args.instrument
    if instrument not in TUNINGS.keys():
        raise InvalidInstrument
    args.instrument = TUNINGS[instrument]

    args.tonality = TONAL_CLASSES[args.tonality]

    note_char = args.note[:1].upper()
    if note_char not in notes._CHARS:
        raise InvalidTone

    note_alt = args.note[1:]
    # if alt:
    #     alt = valid_alt(alt)

    args.note = (note_char, note_alt)

    return args



if __name__ == '__main__':

    args = parse_arguments()

    INSTRUMENT = StringInstrument(
        *[ Note(*s) for s in args.instrument ]
    )

    CHR = args.note[0]
    ALT = args.note[1]
    TONALITY = args.tonality(CHR, ALT)
    # CHORD = args.chord

    FRETS = args.frets
    VERBOSE = args.verbosity

    # try:

    echo('{}{} {}'.format(CHR, ALT, TONALITY.__class__.__name__), 'blue', 'underline')
    INSTRUMENT.fretboard(
        display=TONALITY.scale,
        # display=MinorKey('F', '').scale,
        # display=MajorKey('C').degree(5).seventh,
        # display=SeventhDominantChord('G'),
        frets=FRETS,
        verbose=VERBOSE,
    )

    # except KeyboardInterrupt:
    #     echo()

    # except Exception as x:
    #     print("Unexpected error:", sys.exc_info()[0])
    #     raise x

    # finally:
    #     exit(0)

    # g = ChordVoicing(
    #     3,
    #     3,
    #     0,
    #     0,
    #     2,
    #     3
    # )
