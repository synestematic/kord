#!/usr/bin/env  python3

"""
this script displays a command-line representation of your instrument's fretboard, tuned to your liking
note patterns will be displayed for any given mode (scale/chord) for any given root note
the tunings directory already contains some pre-defined instrument tunings in the form of .json files
modify them or add your own and they will automaticaly become available at runtime
"""

import sys
import argparse

from kord import (
    MajorScale, MinorScale, MelodicMinorScale, HarmonicMinorScale,
    MajorPentatonicScale, MinorPentatonicScale,
    IonianMode, LydianMode, MixolydianMode,
    AeolianMode, DorianMode, PhrygianMode, LocrianMode,
    ChromaticScale
)

from kord import (
    MajorTriad, MinorTriad, AugmentedTriad, DiminishedTriad,
    MajorSeventhChord, MinorSeventhChord, DominantSeventhChord,
    DiminishedSeventhChord, HalfDiminishedSeventhChord,
    MajorNinthChord, MinorNinthChord, DominantNinthChord
)

from kord import (
    MAXIMUM_FRETS, PluckedStringInstrument, MusicNote, max_frets_on_screen
)

from kord import InvalidInstrument, InvalidNote, InvalidAlteration

from bestia.output import echo

import tuner

SCALES = {
    'major': MajorScale,

    'minor': MinorScale,
    'melodic_minor': MelodicMinorScale,
    'harmonic_minor': HarmonicMinorScale,

    'major_pentatonic': MajorPentatonicScale,
    'minor_pentatonic': MinorPentatonicScale,

    'ionian': IonianMode,
    'lydian': LydianMode,
    'mixolydian': MixolydianMode,

    'aeolian': AeolianMode,
    'dorian': DorianMode,
    'phrygian': PhrygianMode,
    'locrian': LocrianMode,

    'chromatic': ChromaticScale,
}

CHORDS = {
    'maj': MajorTriad,
    'min': MinorTriad,
    'aug': AugmentedTriad,
    'dim': DiminishedTriad,

    'maj7': MajorSeventhChord,
    'min7': MinorSeventhChord,
    '7': DominantSeventhChord,
    'dim7': DiminishedSeventhChord, # °7  
    'min7dim5': HalfDiminishedSeventhChord, # ⦰7

    'maj9': MajorNinthChord,
    'min9': MinorNinthChord,
    '9': DominantNinthChord,
}

TUNINGS = tuner.load_tuning_data()

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='<<< Fretboard visualizer tool for the kord framework >>>',
    )
    parser.add_argument(
        'root',
        help='select key ROOT note',
    )

    parser.add_argument(
        '-d', '--degrees',
        help='show degree numbers instead of note pitches',
        action='store_true',
    )

    mode_group = parser.add_mutually_exclusive_group()

    scale_choices = list( SCALES.keys() )
    mode_group.add_argument(
        '-s', '--scale',
        help='{}'.format(str(scale_choices).lstrip('[').rstrip(']').replace('\'', '')),
        choices=scale_choices,
        default='',
        metavar='',
    )

    chord_choices = list( CHORDS.keys() )
    mode_group.add_argument(
        '-c', '--chord',
        help='{}'.format(str(chord_choices).lstrip('[').rstrip(']').replace('\'', '')),
        choices=chord_choices,
        default='maj',
        metavar='',
    )

    instr_choices = list( TUNINGS.keys() )
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
        help='1, 2, .., {}'.format(MAXIMUM_FRETS),
        choices=[ f+1 for f in range(MAXIMUM_FRETS) ],
        default=max_frets_on_screen(),
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
        if args.tuning not in TUNINGS[args.instrument].keys():
            raise InvalidInstrument(
                "fretboard.py: error: argument -t/--tuning: invalid choice: '{}' (choose from {}) ".format(
                    args.tuning,
                    str( list( TUNINGS[args.instrument].keys() ) ).lstrip('[').rstrip(']'),
                )
            )

        # validate root note
        note_chr = args.root[:1].upper()
        if note_chr not in MusicNote.possible_chars():
            raise InvalidNote(
                "fretboard.py: error: argument ROOT: invalid note: '{}' (choose from {}) ".format(
                    note_chr,
                    str( MusicNote.possible_chars() ).lstrip('[').rstrip(']')
                )
            )

        # validate root alteration
        note_alt = args.root[1:]
        if note_alt and note_alt not in MusicNote.input_alterations():
            raise InvalidAlteration(
                "fretboard.py: error: argument ROOT: invalid alteration: '{}' (choose from {}) ".format(
                    note_alt,
                    str( MusicNote.input_alterations() ).lstrip('[').rstrip(']')
                )
            )

        args.root = (note_chr, note_alt)

    except Exception as x:
        parser.print_usage()
        print(x)
        args = None

    return args

def print_mode(mode):
    clr = 'blue'
    mode = '{} {}'.format(
        str(mode.root)[:-1],
        mode.name(),
    )
    echo(mode, clr)

def print_instrument(instrument, tuning):
    clr = 'yellow'
    echo(instrument.title(), clr, 'underline', mode='raw')
    echo(': ', clr, mode='raw')
    echo('{} tuning'.format(tuning), clr)


def run(args):
    
    # default mode is chord, so use scale if set
    if args.scale:
        KeyMode = SCALES[args.scale]
    elif args.chord:
        KeyMode = CHORDS[args.chord]

    root = MusicNote(args.root[0], args.root[1])
    key_mode = KeyMode(*root)
    if not key_mode.validate():
        print(
            '{} {} cannot be visualized'.format(
                str(root)[:-1],
                key_mode.name(),
            )
        )
        return -1

    if args.verbosity:
        print_instrument(args.instrument, args.tuning)

    instrument = PluckedStringInstrument(
        * TUNINGS[args.instrument][args.tuning]
    )

    instrument.render_fretboard(
        mode=key_mode,
        frets=args.frets,
        verbose=args.verbosity,
        show_degrees=args.degrees,
    )

    if args.verbosity:
        print_mode(key_mode)

    return 0


if __name__ == '__main__':
    rc = -1
    valid_args = parse_arguments()
    if not valid_args:
        rc = 2
    else:
        rc = run(valid_args)
    sys.exit(rc)
