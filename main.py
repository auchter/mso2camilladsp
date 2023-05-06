#!/usr/bin/env python3

import json
import yaml

channel_map = {
        'SL': 2,
        'SR': 3,
}

def convert_filters(filters):
    def convert(f):
        t = f['_type']
        if t == 'Delay':
            return {
                'type': 'Delay',
                'parameters': {
                    'delay': f['delay_val'],
                    'unit': 'ms',
                    'subsample': False,
                }
            }
        elif t == 'PeakingEQ':
            return {
                'type': 'Biquad',
                'parameters': {
                    'type': 'Peaking',
                    'freq': f['fc'],
                    'gain': f['gain'],
                    'q': f['q'],
                }
            }
        elif t == 'Gain':
            return {
                'type': 'Gain',
                'parameters': {
                    'gain': f['gain_val'],
                }
            }

        assert(False, f"unknown filter type: {t}")

    result = {}
    for f in filters:
        name = f['ref_desig']
        result[name] = convert(f)
    return result

def parse(filt):
    with open(filt, 'r') as f:
        j = json.load(f)

    
    filters = j['mso_filters']
    print(yaml.dump(convert_filters(filters)))
    pipeline = []
    for k, v in channel_map.items():
        f = {}
        f['type'] = 'Filter'
        f['channel'] = v
        f['names'] = [x['ref_desig'] for x in filters if k in x['chans']]
        pipeline.append(f)
    print(yaml.dump(pipeline))

def main():
    #parse("/home/a/filt.json")
    parse("/home/a/0505.json")

if __name__ == '__main__':
    main()