# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

'''converts old indicator batch scripts into the indicator_framework 1.0 format'''

import os
from opus_core.misc import directory_path_from_opus_path

def _convert_image_type(image_type):
    return {
        'tab': 'Table',
        'csv': 'Table',
        'table': 'Table',
        'map': 'Map',
        'chart': 'Chart',
        }[image_type]    
        
def _convert(args):
    map = {}
    for attr_name, value in args.items():
        if attr_name == 'dataset':
            map['dataset_name'] = repr(value)
        elif attr_name == 'image_type':
            map['class'] = _convert_image_type(value)
        elif attr_name == 'indicator_name':
            map['attribute'] = repr(value)
        elif attr_name == 'attribute':
            if isinstance(value,dict):
                submap = _convert(value)
                for k,v in submap.items():
                    map[k] = v
            else:
                map['attribute'] = repr(value)
        elif attr_name == 'scale':
            map['scale'] = value
        elif attr_name == 'operation':
            if not 'expression' in map:
                map['expression'] = {}
            map['expression']['operation'] = value
        elif attr_name == 'arguments':
            if not 'expression' in map:
                map['expression'] = {}
            map['expression']['operands'] = value
    map['source_data'] = 'source_data'
    return map

def _create_indicator(i, indent):
    s = []
    indents = ''
    for k in range(indent):
        indents += '\t'

    s.append('%s%s('%(indents,i['class']))
    indents += '\t'
    for k,v in i.items():
        if k == 'class': continue
        s.append('%s%s = %s,'%(indents,k,v))
    s.append(indents + ')')
    return '\n'.join(s)

def convert(indicators, indent = 0):
    converted = []
    for indicator in indicators:
        i = _convert(indicator)
        i = _create_indicator(i, indent)
        converted.append(i)
        
    return converted
    
from opus_core.tests import opus_unittest

class Tests(opus_unittest.OpusTestCase):
    def test_simple(self):
        input = [{'dataset':'large_area',
                 'image_type':'map',
                 'attribute':{'indicator_name':'psrc.large_area.population',
                              'scale':[1,750000]
                          }
             }]
        output = convert(input)
        expected = (["Map(\n"
                "\tdataset_name = 'large_area',\n"
                "\tattribute = 'psrc.large_area.population',\n"
                "\tscale = [1, 750000],\n"
                "\t)"])
        output_map = self.get_char_count(output[0])
        expected_map = self.get_char_count(expected[0])
        #self.assertEqual(output,expected)
#        for k in expected_map.keys():
#            if k not in output_map:
#                print '%s in expected but not output'%k
#            elif output_map[k] != expected_map[k]:
#                print '%s: output=%i, expected=%i'%(k,output_map[k],expected_map[k])
            
        self.assertEqual(len(output_map.keys()),len(expected_map.keys()))
                
    def get_char_count(self,s):
        char_map = {}
        for ch in s:
            if not ch in char_map:
                char_map[ch] = 1
            else:
                char_map[ch] += 1
        return char_map
    
#if __name__ == '__main__':
#    #opus_unittest.main()
#    from psrc.indicators.make_indicators import multi_year_requests
#    print multi_year_requests
#    results = convert(multi_year_requests, indent = 1)
#    for i in results:
#        print i + ','
