import os
import sys
import json
import argparse

from bestia.output import echo

from kord import *

JSON_DIR = '{}/tunings'.format( os.path.dirname(os.path.realpath(__file__)) )

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
        description='<<< Fretboard visualizer sample tool for the kord music framework >>>',
    )
    parser.add_argument(
        'root',
        help='select key ROOT note',
    )

    group = parser.add_mutually_exclusive_group()

    scale_choices = [ m for m in SCALES.keys() ]
    group.add_argument(
        '-s', '--scale',
        help='{}'.format(str(scale_choices).lstrip('[').rstrip(']').replace('\'', '')),
        choices=scale_choices,
        default='',
        metavar='',
    )

    chord_choices = [ m for m in CHORDS.keys() ]
    group.add_argument(
        '-c', '--chord',
        help='{}'.format(str(chord_choices).lstrip('[').rstrip(']').replace('\'', '')),
        choices=chord_choices,
        default='maj',
        metavar='',
    )

    instr_choices = [ i for i in INSTRUMENTS.keys() ]
    parser.add_argument(
        '-i', '--instrument',
        help='{}'.format(str(instr_choices).lstrip('[').rstrip(']').replace('\'', '')),
        choices=instr_choices,
        default='guitar',
        metavar='',
    )
    parser.add_argument(
        '-t', '--tuning',
        help='check .json files for available options',
        default='standard',
        metavar='',
    )
    parser.add_argument(
        '-f', '--frets',
        help='1, 2, .., {}'.format(MAX_FRETS),
        choices=[ f+1 for f in range(MAX_FRETS) ],
        default=max_frets_on_screen(MAX_FRETS),
        metavar='',
        type=int,
    )
    parser.add_argument(
        '-v', '--verbosity',
        help='0, 1, 2',
        choices= (0, 1, 2),
        default=1,
        metavar='',
        type=int,
    )
    args = parser.parse_args()

    # some args require extra validation than what argparse can offer, let's do that here...
    try:
        # validate tuning
        if args.tuning not in INSTRUMENTS[args.instrument].keys():
            raise InvalidInstrument(
                "fretboard.py: error: argument -t/--tuning: invalid choice: '{}' (choose from {}) ".format(
                    args.tuning,
                    str( list( INSTRUMENTS[args.instrument].keys() ) ).lstrip('[').rstrip(']'),
                )
            )

        # validate root note
        note_chr = args.root[:1].upper()
        if note_chr not in notes._CHARS:
            raise InvalidNote(
                "fretboard.py: error: argument ROOT: invalid note: '{}' (choose from {}) ".format(
                    note_chr,
                    str( [ n for n in notes._CHARS if n ] ).lstrip('[').rstrip(']')
                )
            )

        # validate root alteration
        note_alt = args.root[1:]
        if note_alt and note_alt not in list(notes._ALTS.keys()):
            raise InvalidNote(
                "fretboard.py: error: argument ROOT: invalid alteration: '{}' (choose from {}) ".format(
                    note_alt,
                    str( list(notes._ALTS.keys()) ).lstrip('[').rstrip(']')
                )
            )

        args.root = (note_chr, note_alt)

    except Exception as x:
        parser.print_usage()
        print(x)
        args = None

    return args

def run(args):
    
    instrument = PluckedStringInstrument(
        *[ Note(*string_tuning) for string_tuning in INSTRUMENTS[args.instrument][args.tuning] ]
    )

    if args.scale:
        MODE = SCALES[args.scale]
    elif args.chord:
        MODE = CHORDS[args.chord]

    mode = MODE(chr=args.root[0], alt=args.root[1])

    echo(
        '{} {}\t\t{} ({} tuning)'.format(
            str(mode.root)[:-1],
            mode.name,
            args.instrument,
            args.tuning
        ),
        'blue'
    )

    instrument.fretboard(
        display=mode,
        frets=args.frets,
        verbose=args.verbosity,
        limit=24
    )

    return 0

if __name__ == '__main__':
    rc = -1
    valid_args = parse_arguments()
    if not valid_args:
        rc = 2
    else:
        rc = run(valid_args)
    sys.exit(rc)
