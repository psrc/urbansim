# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from collections import OrderedDict
from numpy import concatenate
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

class Shifters(object):

    def __init__(self):
        try:
            dataset_pool = SessionConfiguration().get_dataset_pool()
        except:
            logger.log_warning("SessionConfiguration is not initialized; return {}")
            self.shifters = OrderedDict()
            return
        self.price_shifters = dataset_pool['price_shifter']
        self.cost_shifters = dataset_pool['cost_shifter']
        self.load()

    def __getitem__(self, key):
        return self.shifters[key]

    def getall(self):
        """concatenate all values"""
        values = concatenate((self.price_shifters['estimate'], 
                              self.cost_shifters['residential_shifter'], 
                              self.cost_shifters['non_residential_shifter']))
        return values

    def setall(self, values):
        assert len(values) == len(self.getall())
        size1 = self.price_shifters.size()
        size2 = self.cost_shifters.size()
        i = 0
        self.price_shifters['estimate'] = values[i:(i+size1)]
        self.price_shifters.touch_attribute('estimate')
        i += size1
        self.cost_shifters['residential_shifter'] = values[i:(i+size2)]
        self.cost_shifters.touch_attribute('residential_shifter')
        i += size2
        self.cost_shifters['non_residential_shifter'] = values[i:(i+size2)]
        self.cost_shifters.touch_attribute('non_residential_shifter')
        self.flush()
        self.load()  ##reload to update values

    def load(self):
        self.shifters = OrderedDict()
        self.shifters['price_shifters'] = OrderedDict([(name, shifter) for name, shifter in
                                zip(self.price_shifters['name'], self.price_shifters['estimate'])])
        res_cost = self.cost_shifters.compute_variables('cost_shifter.cost_estimate * cost_shifter.residential_shifter')
        nonres_cost = self.cost_shifters.compute_variables('cost_shifter.cost_estimate * cost_shifter.non_residential_shifter')
        RESLOCALCOST_D = OrderedDict([(cnty_id, cost) for cnty_id, cost in
                               zip(self.cost_shifters['county_id'], res_cost)])
        NONRESLOCALCOST_D = OrderedDict([(cnty_id, cost) for cnty_id, cost in
                               zip(self.cost_shifters['county_id'], nonres_cost)])
        self.shifters['RESLOCALCOST_D'] = RESLOCALCOST_D
        self.shifters['NONRESLOCALCOST_D'] = NONRESLOCALCOST_D

    def flush(self):
        self.price_shifters.flush_dataset()
        self.cost_shifters.flush_dataset()

vars = locals()
_shifters = Shifters().shifters
for k, v in _shifters.iteritems():
    vars[k]=eval('{}'.format(v))

from opus_core.tests import opus_unittest
from numpy import array, arange, allclose
import tempfile, os, shutil, sys
from glob import glob
import urbansim.tools.do_refinement

class TestShifters(opus_unittest.OpusTestCase):
    def setUp(self):
        self.urbansim_tmp = tempfile.mkdtemp(prefix='urbansim_tmp')
        self.datasets = {
                'price_shifter' : {
                    'price_shifter_id': arange(1, 8),
                    'name':             array(["price_per_sqft_mf", "price_per_sqft_sf", "rent_per_sqft_sf", 
                                               "rent_per_sqft_mf", "of_rent_sqft", "ret_rent_sqft", "ind_rent_sqft"]),
                    'estimate':         array([.35, 1.2, 1.0, 2.0, 1.85, 1.85, 2.5]),
                 },
                'cost_shifter': {
                    'cost_shifter_id': arange(1, 10),
                    'county_id': array([49, 41, 1, 43, 28, 38, 7, 48, 21]),
                    'cost_estimate': array([115.58, 114.6, 116.2, 117.15, 115.58, 123.8, 112.9, 110.5, 115.58]),
                    'residential_shifter': array([ .45, 1.05, .95, 1.0, 1.7, .8, .95, .7, 1.45]),
                    'non_residential_shifter': array([.8, 1.0, .9, 1.0, .8, 1.1, .9, .6, .9]),
                }
              }
        cache_dir = os.path.join(self.urbansim_tmp, 'urbansim_cache')
        SimulationState().set_cache_directory(cache_dir)
        year = 2010
        SimulationState().set_current_time(year)
        attribute_cache = AttributeCache()
        self.dataset_pool = SessionConfiguration(new_instance=True,
                                                 package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
                                                 in_storage=attribute_cache).get_dataset_pool()
        for table_name, table_data in self.datasets.iteritems():
            attribute_cache.write_table(table_name=table_name, table_data=table_data)

    def tearDown(self):
        shutil.rmtree(self.urbansim_tmp)

    def test_shifters(self):
        sh1 = Shifters()
        self.assert_( sh1.shifters.keys() == ['price_shifters', 'RESLOCALCOST_D', 'NONRESLOCALCOST_D'] )
        self.assert_(allclose(sh1.shifters['price_shifters'].values(), self.datasets['price_shifter']['estimate']))
        cost_shifters = self.datasets['cost_shifter']
        self.assert_(allclose( sh1.shifters['RESLOCALCOST_D'].values(), 
                               cost_shifters['residential_shifter']*cost_shifters['cost_estimate'] ))
        self.assert_(allclose( sh1.shifters['NONRESLOCALCOST_D'].values(), 
                               cost_shifters['non_residential_shifter']*cost_shifters['cost_estimate'] ))

    def test_get(self):
        sh1 = Shifters()
        expected = concatenate((self.datasets['price_shifter']['estimate'], 
                                 self.datasets['cost_shifter']['residential_shifter'],
                                 self.datasets['cost_shifter']['non_residential_shifter']))
        self.assertArraysEqual( sh1.getall(), expected )

    def test_set(self):
        sh1 = Shifters()
        original_values = sh1.getall()
        new_values = original_values * 1.09
        sh1.setall(new_values)
        self.assert_(allclose( sh1.getall(), new_values ))
        i = 0
        self.dataset_pool.remove_all_datasets()
        price_shifters = self.dataset_pool['price_shifter']
        size1 = price_shifters.size()
        self.assertArraysEqual(price_shifters['estimate'],  new_values[i:(i+size1)])
        i += size1
        cost_shifters = self.dataset_pool['cost_shifter']
        size2 = cost_shifters.size()
        self.assertArraysEqual(cost_shifters['residential_shifter'],  new_values[i:(i+size2)])
        i += size2
        self.assertArraysEqual(cost_shifters['non_residential_shifter'],  new_values[i:(i+size2)])

if __name__ == "__main__":
    opus_unittest.main()

