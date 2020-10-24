import os
import json
import argparse

from bestia.output import echo

from kord import *

MAX_FRETS = 36

JSON_DIR = 'instruments'

def list_json_instruments(directory):
    for f in os.listdir(directory):
        if f.endswith('.json'):
            yield f.split('.')[0]

def open_json_instrument(directory, instrument):
    try:
        with open('{}/{}.json'.format(directory, instrument)) as js:
            return json.load(js)
    except:
        return {}

def get_instruments_data():
    data = {}
    for instrument in list_json_instruments(JSON_DIR):

        instrument_data = open_json_instrument(JSON_DIR, instrument)
        if not instrument_data:
            echo('Ignoring {}.json (failed to parse file)'.format(instrument), 'red')
            continue

        for tuning, strings_list in instrument_data.items():
            for s, string in enumerate(strings_list):
                instrument_data[tuning][s] = (
                    # chr    , alt         , oct
                    string[0], string[1:-1], int(string[-1])
                )

        data[instrument] = instrument_data

    return data


INSTRUMENTS = get_instruments_data()

TONAL_CLASSES = {

    'chromatic': ChromaticKey,

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
    parser = argparse.ArgumentParser(
        description = '<<< Fretboard visualizer helper tool for the kord music framework >>>',
    )
    parser.add_argument('ROOT', help='select a ROOT key')

    parser.add_argument(
        '-m', '--mode',
        help='select the music mode to visualize',
        choices=[ m for m in TONAL_CLASSES.keys() ],
        default='major',
        # metavar=TONAL_CLASSES.keys(),
    )
    parser.add_argument(
        '-i', '--instrument',
        help='select instrument you want to visualize the fretboard of',
        choices=[ i for i in INSTRUMENTS.keys() ],
        default='guitar',
        metavar='',
        # dest='domain'

    )
    parser.add_argument(
        '-t', '--tuning',
        help='check the instrument.json file for available tunings',
        default='standard',
    )
    parser.add_argument(
        '-f', '--frets',
        help='limit the number of frets to display, max is {}'.format(MAX_FRETS),
        type=int,
        default=max_frets_on_screen(MAX_FRETS),
    )
    parser.add_argument(
        '-v', '--verbosity',
        help = 'set the amount of application verbosity, default is 1',
        choices = (0, 1, 2),
        type = int,
        default = 1,
    )

    args = parser.parse_args()

    if args.instrument not in INSTRUMENTS.keys():
        raise InvalidInstrument(args.instrument)

    if args.tuning not in INSTRUMENTS[args.instrument].keys():
        raise InvalidInstrument(args.tuning)

    args.tuning = INSTRUMENTS[args.instrument][args.tuning]

    note_char = args.ROOT[:1].upper()
    if note_char not in notes._CHARS:
        raise InvalidNote(note_char)

    note_alt = args.ROOT[1:]
    # if alt:
    #     alt = valid_alt(alt)

    args.ROOT = (note_char, note_alt)

    return args


if __name__ == '__main__':

    args = parse_arguments()

    INSTRUMENT = StringInstrument(
        *[ Note(*string) for string in args.tuning ]
    )

    CHR = args.ROOT[0]
    ALT = args.ROOT[1]
    TONALITY = TONAL_CLASSES[args.mode](CHR, ALT)

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
        limit=24
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