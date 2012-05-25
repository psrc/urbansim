# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import yaml
import yaml.constructor
from opus_core.logger import logger
from opus_core.misc import directory_path_from_opus_path
from collections import OrderedDict

class Shifters(object):
    path = directory_path_from_opus_path('urbansim_parcel.proposal')
    filename = os.path.join(path, 'shifters.yaml')

    def __init__(self, filename=None):
        if filename is not None:
            self.filename = filename
        self.load()

    def __getitem__(self, key):
        return self.shifters[key]

    def _recursive_get(self, adict):
        results = []
        for k, v in adict.iteritems():
            if isinstance(v, dict):
                results += self._recursive_get(v)
            else:
                results += v if type(v) in (list, tuple) else [v]
        return results

    def getall(self):
        """concatenate all values"""
        return self._recursive_get(self.shifters)

    def _recursive_set(self, adict, alist):
        i = 0
        for k, v in adict.iteritems():
            if isinstance(v, dict):
                i += self._recursive_set(v, alist[i:])
            else:
                size = len(v) if type(v) in (list, tuple) else 1
                new_val = alist[i:(i+size)]
                adict[k] = new_val if size > 1 else new_val[0]
                i += size
        return i

    def setall(self, values, filename=None):
        self._recursive_set(self.shifters, values)
        self.flush(filename=filename)

    def load(self):
        if os.path.exists(self.filename):
            stream = file(self.filename, 'r')
            #self.shifters = yaml.load(stream, OrderedDictYAMLLoader)
            yaml_dict = yaml.load(stream)
            self.shifters = OrderedDict(sorted(yaml_dict.items(),key=lambda x: x[0]))
            stream.close()
        else:
            logger.log_warning("File %s does not exist; return {}" % self.filename)
            self.shifters = {}

    def flush(self, filename=None):
        if filename is None:
            filename = self.filename
        stream = file(filename, 'w')
        items = yaml.dump(self.shifters, stream)
        stream.close()

vars = locals()
_shifters = Shifters().shifters
for k, v in _shifters.iteritems():
    #eval("vars['{}']={}".format(k, v))
    vars[k]=eval('{}'.format(v))

from opus_core.tests import opus_unittest
class Tests(opus_unittest.OpusTestCase):
    def test_ordered(self):
        test_path = directory_path_from_opus_path('urbansim_parcel.tests.test_files')
        test_file1 = os.path.join(test_path, 'test01.yaml')
        test_file2 = os.path.join(test_path, 'test02.yaml')
        test_file3 = os.path.join(test_path, 'test03.yaml')
        sh1 = Shifters(filename=test_file1)
        sh2 = Shifters(filename=test_file2)
        self.assert_( sh1.shifters == sh2.shifters )
        self.assert_( sh1.shifters.keys() == sh2.shifters.keys() )
        self.assert_( sh1.shifters.values() == sh2.shifters.values() )
        values = sh2.getall()
        expected = [0, 2, 4, 8, 'fish', 11, 22, 'fish', 3, True, None, False]
        new_values = range(len(values))
        #print values
        self.assert_( values == expected )
        sh2.setall(new_values,filename=test_file3)
        del sh2
        sh3 = Shifters(filename=test_file3)
        self.assert_( sh3.getall() == new_values )
        os.remove(test_file3)

if __name__ == "__main__":
    opus_unittest.main()

    ## values saved to shifters.yaml so they can be easily manipulated
    """
    price_shifters = {
        'price_per_sqft_mf': .35,
        'price_per_sqft_sf':1.2,
        'rent_per_sqft_sf':1.0,
        'rent_per_sqft_mf':2.0,
        'of_rent_sqft':1.85,
        'ret_rent_sqft':1.85,
        'ind_rent_sqft':2.5
    }

    RESLOCALCOST_D = {
        49:115.58*.45, # sonoma
        41:114.6*1.05, # san mateo
        1:116.2*.95, # alameda
        43:117.15, # santa clara
        28:115.58*1.7, # napa
        38:123.8*.8, # san fran
        7:112.9*.95, # contra costa
        48:110.5*.7, # solano
        21:115.58*1.45 # marin 
    }

    NONRESLOCALCOST_D = {
        49:115.58*.8, # sonoma
        41:114.6, # san mateo
        1:116.2*.9, # alameda
        43:117.1*1.0, # santa clara
        28:115.58*.8, # napa
        38:123.8*1.1, # san fran
        7:112.9*.9, # contra costa
        48:110.5*.6, # solano
        21:115.58*.9 # marin 
    }
    """
