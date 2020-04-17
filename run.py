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

SCALES = {

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
    parser.add_argument('key')

    parser.add_argument(
        '-t', '--tuning',
        help = 'set string number/tuning',
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
        '-s', '--scale',
        help = 'scale to display',
        default='major'
    )

    parser.add_argument(
        '-c', '--chord',
        help = 'chord to display',
    )

    args = parser.parse_args()

    tuning = args.tuning
    if tuning not in TUNINGS.keys():
        raise InvalidInstrument
    args.tuning = TUNINGS[tuning]

    args.scale = SCALES[args.scale]

    key_char = args.key[:1].upper()
    if key_char not in notes._CHARS:
        raise InvalidTone

    key_alt = args.key[1:]
    # if alt:
    #     alt = valid_alt(alt)

    args.key = (key_char, key_alt)

    return args



if __name__ == '__main__':

    args = parse_arguments()

    INSTRUMENT = StringInstrument(
        *[ Note(*s) for s in args.tuning ]
    )

    KEY = args.key
    SCALE = args.scale
    # CHORD = args.chord

    DISPLAY = SCALE(*KEY).scale

    FRETS = args.frets
    VERBOSE = args.verbosity

    try:
        echo(SCALE, 'blue', 'underline')
        INSTRUMENT.fretboard(
            display=DISPLAY,
            # display=MinorKey('F', '').scale,
            # display=MajorKey('C').degree(5).seventh,
            # display=SeventhDominantChord('G'),
            frets=FRETS,
            verbose=VERBOSE,
        )

    except KeyboardInterrupt:
        echo()

    except Exception as x:
        print("Unexpected error:", sys.exc_info()[0])
        raise x

    finally:
        exit(0)

    # g = ChordVoicing(
    #     3,
    #     3,
    #     0,
    #     0,
    #     2,
    #     3
    # )
