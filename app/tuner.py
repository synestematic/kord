import os
import json

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
