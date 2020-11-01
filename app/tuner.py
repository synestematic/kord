"""
this module is in charge of loading the data of the .json files in the tunings directory and make it available to the fretboard application.
"""

import os
import json

from kord.notes import Note

JSON_DIR = '{}/tunings'.format( os.path.dirname(os.path.realpath(__file__)) )

def json_instruments():
    return [
        f.split('.')[0] for f in os.listdir(JSON_DIR) if f.endswith('.json')
    ]

def open_instrument(instrument):
    try:
        with open('{}/{}.json'.format(JSON_DIR, instrument)) as js:
            return json.load(js)
    except:
        return {}

def load_tuning_data():
    data = {}
    for instrument in json_instruments():

        instrument_data = open_instrument(instrument)
        if not instrument_data:
            print('WARNING: {}.json is not valid json, ignoring file...'.format(instrument))
            continue

        for tuning, strings_list in instrument_data.items():
            for s, string in enumerate(strings_list):
                try:
                    # validates the note attributes
                    instrument_data[tuning][s] = Note(
                        string[0], string[1:-1], string[-1]
                    )
                except:
                    print(
                        'WARNING: "{}" is not a valid note, ignoring {}.json "{}" tuning...'.format(string, instrument, tuning)
                    )

        data[instrument] = instrument_data

    return data
