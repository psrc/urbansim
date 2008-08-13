#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.datasets.dataset import Dataset
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.resources import Resources
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger

from urbansim.constants import Constants
from urbansim.data.test_cache_configuration import TestCacheConfiguration

class UrbansimConstantDataset(Constants):

    def __init__(self, **kwargs):
        Constants.__init__(self, **kwargs)
        
    def get_attribute(self, x):
        # look up the attribute and return it in a list of length 1
        return [self[x]]

    def summary(self, output=logger):
        output.write("UrbanSim constant dataset")


import os
from opus_core.tests import opus_unittest

from opus_core.opus_package_info import package

class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.config = TestCacheConfiguration()

        opus_core_path = package().get_opus_core_path()
        cache_dir = os.path.join(opus_core_path, 'data', 'test_cache')

        SimulationState(new_instance=True).set_current_time(
            self.config['base_year'])
        SimulationState().set_cache_directory(cache_dir)
        SessionConfiguration(self.config, new_instance=True,
                             package_order=['urbansim', 'opus_core'],
                             in_storage=AttributeCache())

    def test(self):
        urbansim_constant = UrbansimConstantDataset(in_storage=AttributeCache())
        self.assertEqual(urbansim_constant['absolute_max_year'], 3000)
        self.assertAlmostEqual(urbansim_constant['acres'], 150*150*0.0002471, 6)

if __name__ == '__main__':
    opus_unittest.main()
