"""
this module is in charge of loading the data of the .json files in the tunings directory and make it available to the fretboard application.

"""

import os
import json

JSON_DIR = '{}/tunings'.format( os.path.dirname(os.path.realpath(__file__)) )

def list_json_instruments():
    for f in os.listdir(JSON_DIR):
        if f.endswith('.json'):
            yield f.split('.')[0]

def open_json_instrument(instrument):
    try:
        with open('{}/{}.json'.format(JSON_DIR, instrument)) as js:
            return json.load(js)
    except:
        return {}

def load_tuning_data():
    data = {}
    for instrument in list_json_instruments():

        instrument_data = open_json_instrument(instrument)
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
