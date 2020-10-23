import os
import json
import argparse

from bestia.output import echo

from kord import *

def json_instruments(d):
    for f in os.listdir(d):
        if f.endswith('.json'):
            yield f.split('.')[0]

def get_instrument_data():
    d = {}
    for instrument in json_instruments('instruments'):
        with open('instruments/{}.json'.format(instrument)) as js:
            d[instrument] = json.load(js)
    return d

INSTRUMENTS = get_instrument_data()

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
        description = 'fretboard',
    )
    parser.add_argument('note')

    parser.add_argument(
        '-i', '--instrument',
        # help = 'select string instrument',
        choices = INSTRUMENTS.keys(),
        default = 'guitar',
    )

    parser.add_argument(
        '-t', '--tuning',
        # help = 'set specific tuning',
        choices = [ INSTRUMENTS[i].keys() for i in INSTRUMENTS.keys() ],
        default = 'standard',
    )

    parser.add_argument(
        '-f', '--frets',
        # help = 'number of frets to display',
        type = int,
        default = max_frets_on_screen(),
    )
    parser.add_argument(
        '-v', '--verbosity',
        # help = 'amount of verbosity',
        choices = (0, 1, 2),
        type = int,
        default = 1,
    )
    parser.add_argument(
        '-k', '--key',
        # help = 'key to display',
        choices = TONAL_CLASSES.keys(),
        default = 'major',
    )

    # parser.add_argument(
    #     '-c', '--chord',
    #     help = 'chord to display',
    # )

    args = parser.parse_args()

    if args.instrument not in INSTRUMENTS.keys():
        raise InvalidInstrument(args.instrument)

    if args.tuning not in INSTRUMENTS[args.instrument].keys():
        raise InvalidInstrument(args.tuning)

    args.tuning = INSTRUMENTS[args.instrument][args.tuning]

    args.key = TONAL_CLASSES[args.key]

    note_char = args.note[:1].upper()
    if note_char not in notes._CHARS:
        raise InvalidNote(note_char)

    note_alt = args.note[1:]
    # if alt:
    #     alt = valid_alt(alt)

    args.note = (note_char, note_alt)

    return args



if __name__ == '__main__':

    args = parse_arguments()

    INSTRUMENT = StringInstrument(
        *[ Note(*string) for string in args.tuning ]  # maigc is here
    )

    CHR = args.note[0]
    ALT = args.note[1]
    TONALITY = args.key(CHR, ALT)
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
