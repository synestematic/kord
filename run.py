import os
import sys
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

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='<<< Fretboard visualizer helper tool for the kord music framework >>>',
    )
    parser.add_argument(
        'ROOT', help='select a ROOT key'
    )
    parser.add_argument(
        '-m', '--mode',
        help='music mode to visualize: {}'.format([ m for m in TONAL_CLASSES.keys() ]),
        choices=[ m for m in TONAL_CLASSES.keys() ],
        default='major',
        metavar='',
    )
    parser.add_argument(
        '-i', '--instrument',
        help='instrument fretboard to visualize: {}'.format([ i for i in INSTRUMENTS.keys() ]),
        choices=[ i for i in INSTRUMENTS.keys() ],
        default='guitar',
        metavar='',
    )
    parser.add_argument(
        '-t', '--tuning',
        help='instrument tuning: check your .json files for available options',
        default='standard',
        metavar='',
    )
    parser.add_argument(
        '-f', '--frets',
        help='number of displayed frets: [0, 1, 2, .. , {}]'.format(MAX_FRETS),
        type=int,
        default=max_frets_on_screen(MAX_FRETS),
        metavar='',
    )
    parser.add_argument(
        '-v', '--verbosity',
        help='application verbosity: [0, 1, 2]',
        choices= (0, 1, 2),
        type=int,
        default=1,
        metavar='',
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


def run(args):

    INSTRUMENT = StringInstrument(
        *[ Note(*string) for string in args.tuning ]
    )

    CHR = args.ROOT[0]
    ALT = args.ROOT[1]
    MODE = TONAL_CLASSES[args.mode](CHR, ALT)

    FRETS = args.frets
    VERBOSE = args.verbosity

    echo('{}{} {}'.format(CHR, ALT, MODE.__class__.__name__), 'blue', 'underline')
    INSTRUMENT.fretboard(
        display=MODE.scale,
        # display=MinorKey('F', '').scale,
        # display=MajorKey('C').degree(5).seventh,
        # display=SeventhDominantChord('G'),
        frets=FRETS,
        verbose=VERBOSE,
        limit=24
    )

    return 0


if __name__ == '__main__':
    args = parse_arguments()
    rc = run(args)
    sys.exit(rc)
