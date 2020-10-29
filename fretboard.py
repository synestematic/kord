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
        'ROOT',
        help='select a root note',
    )
    parser.add_argument(
        '-m', '--mode',
        help='set mode: {}'.format([ m for m in TONAL_CLASSES.keys() ]),
        choices=[ m for m in TONAL_CLASSES.keys() ],
        default='major',
        metavar='',
    )
    parser.add_argument(
        '-i', '--instrument',
        help='set instrument fretboard: {}'.format([ i for i in INSTRUMENTS.keys() ]),
        choices=[ i for i in INSTRUMENTS.keys() ],
        default='guitar',
        metavar='',
    )
    parser.add_argument(
        '-t', '--tuning',
        help='set instrument tuning: check .json files for available options',
        default='standard',
        metavar='',
    )
    parser.add_argument(
        '-f', '--frets',
        help='set number of displayed frets: [1, 2, .. , {}]'.format(MAX_FRETS),
        choices=[ f+1 for f in range(MAX_FRETS) ],
        default=max_frets_on_screen(MAX_FRETS),
        metavar='',
        type=int,
    )
    parser.add_argument(
        '-v', '--verbosity',
        help='set application verbosity: [0, 1, 2]',
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

        # validate ROOT note
        note_chr = args.ROOT[:1].upper()
        if note_chr not in notes._CHARS:
            raise InvalidNote(
                "fretboard.py: error: argument ROOT: invalid note: '{}' (choose from {}) ".format(
                    note_chr,
                    str( [ n for n in notes._CHARS if n ] ).lstrip('[').rstrip(']')
                )
            )

        # validate ROOT alteration
        note_alt = args.ROOT[1:]
        if note_alt and note_alt not in list(notes._ALTS.keys()):
            raise InvalidNote(
                "fretboard.py: error: argument ROOT: invalid alteration: '{}' (choose from {}) ".format(
                    note_alt,
                    str( list(notes._ALTS.keys()) ).lstrip('[').rstrip(']')
                )
            )

        args.ROOT = (note_chr, note_alt)

    except Exception as x:
        parser.print_usage()
        print(x)
        args = None

    return args


def run(args):
    
    try:
        rc = 0

        INSTRUMENT = PluckedStringInstrument(
            *[ Note(*string_tuning) for string_tuning in INSTRUMENTS[args.instrument][args.tuning] ]
        )

        MODE = TONAL_CLASSES[args.mode](chr=args.ROOT[0], alt=args.ROOT[1])

        echo('{} {} on {} ({} tuning)'.format(str(MODE.root)[:-1], MODE.name, args.instrument, args.tuning), 'blue', '')

        INSTRUMENT.fretboard(
            # display=MODE.scale,
            display=MODE.triad,
            frets=args.frets,
            verbose=args.verbosity,
            limit=24
        )

    except Exception as x:
        print(x)
        rc = -1

    finally:
        return rc


def bla():
        # c = Note('C', '', 3)
    # print(
    #     c.oversteps_oct(Note('C', 'b', 4))
    # )

    asd = MajorKey( 'C' )
    for n in asd.triad(
    # for n in asd.scale(
        note_count=8,
        yield_all=1,
        # start_note=Note('C', '', 3),
    ):
        # pass
        echo(n, 'red')


if __name__ == '__main__':
    # try:
        rc = -1
        valid_args = parse_arguments()
        if not valid_args:
            rc = 2
        else:
            rc = bla()
            # rc = run(valid_args)
        sys.exit(rc)

    # except:
    #     print()
'''
scale, triad

    _spell
                count notes
                filter Nones

    _filter_degrees
                order degrees

    _solmizate
                start_note
                yield Nones
                change oct


        # calculate distance between octaves of first and last items of degree_order
        octave_delta = self.degree(degree_order[-1]).oct - self.degree(degree_order[0]).oct
        if not octave_delta:  # this cannot be 0 ...
            octave_delta = 1


        i = 0
        while True:

            #   7 for Major, 12 for Chromatic
            o = len(self.root_intervals) * i

            for degree_index, _ in enumerate(degree_order):

                this = degree_order[degree_index]   + o  #  8 = 1 + 7*1
                prev = degree_order[degree_index-1] + o  # 12 = 5 + 7*1
                if degree_index == 0:
                    prev -= len(self.root_intervals) # should be 5

                if i != 0 and degree_index == 0 and self.degree(prev).oversteps_oct(self.degree(this)):
                    # input([prev, self.degree(prev), this, self.degree(this)])
                    i += octave_delta
                    o = len(self.root_intervals) * i
                    this = degree_order[degree_index]   + o
                    # input([prev, self.degree(prev), this, self.degree(this)])

                if self.degree(this) < start_note:
                    continue


                # dont yield Nones before start_note
                if self.degree(this) != start_note:
                    # yield non-diatonic semitones
                    last_interval =  self.degree(this) - self.degree(prev)
                    for st in range(last_interval - 1):
                        yield None

                yield  self.degree(this)

            i += octave_delta

        input('DONE')
        return



'''
