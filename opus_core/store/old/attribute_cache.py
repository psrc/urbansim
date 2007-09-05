#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

import os

from sets import Set

from numpy import float32

from opus_core.store.old.storage import Storage
from opus_core.resources import Resources
from opus_core.opus_error import OpusError
from opus_core.store.flt_storage import flt_storage
from opus_core.simulation_state import SimulationState


class AttributeCache(Storage):
    """This Storage class caches data via the file system, which is faster
    than running directly from a database, and allows the simulation to 
    unload computed values from memory when they are no longer needed.
    
    The cached data are stored in a 'cache directory', whose name contains the 
    datetime in which it was created.  In this directory there is a separate
    sub-directory for each year with cached data.  Inside each year directory 
    is a dataset directory for any dataset with cached directory.  
    Inside the dataset directory
    are a set of files, one per attribute of this dataset.  Each attribute 
    file has a suffix indicating the type of data stored in it.
    
    For instance, the file:
    
        'D:\cache\2005_12_14__21_14\2000\gridcells\grid_id.li4 
    
    contains an array of int32 values that are the grid_id attribute for 
    the gridcells dataset as it was last computed in year 2000 of the 
    simulation begun on December 14, 2005 at 21:14 hours.
    
    Delegates as much work as possible to flt_storage objects created
    for a year directory.
    
    It currently uses flt_storage.
    """
    def __init__(self, cache_directory=None):
        """cache_directory is the directory containing the year directories."""
        self.simulation_state = SimulationState()
        self._flt_storage_per_year = {}
        self.cache_directory = cache_directory
        
    def write_dataset(self, write_resources):
        values = write_resources['values']
        attrtype = write_resources['attrtype']
        out_table_name = write_resources['in_table_name']

        return self._write_dataset(out_table_name=out_table_name, values=values,
            attrtype=attrtype) 
        
    def _write_dataset(self, out_table_name, values, attrtype):
        """Will write to the SimulationState's current year.
        """
        time = SimulationState().get_current_time()
        self._write_dataset_to_cache(values, attrtype, time, out_table_name)
    
    def _write_dataset_to_cache(self, values, attribute_types, time, table_name):
        """ writes the values given in values to the cache"""
        write_resources = Resources({"values":values, 
                                     "attrtype":attribute_types, 
                                     "out_table_name":table_name})
        self.get_flt_storage_for_year(time).write_dataset(write_resources)
    
    
from opus_core.tests import opus_unittest
import tempfile

from shutil import rmtree
from numpy import array
from numpy import ma

from opus_core.misc import write_to_file
from opus_core.variables.attribute_type import AttributeType
from opus_core.session_configuration import SessionConfiguration

class AttributeCacheTests(opus_unittest.OpusTestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='opus_tmp')
        self.start_year = 2001
        self.dataset_name = "my_dataset"
        self.table_name = "my_dataset"
        self.flt_test_file_path = os.path.join(self.temp_dir, "2001", self.dataset_name, "attr1.lf4")
        self.flt_index_file_path = os.path.join(self.temp_dir, "2001", self.dataset_name, "my_id.lf4")
        self.flt_industrial_file_path = os.path.join(self.temp_dir, "2001", self.dataset_name, "attr2.lf8")
        self.attr1_data = array([3.5,6.7,8.9,-1.2,6])
        self.index_data = array([1,2,3,4,5])
        self.attr2_data = array([5.2,7.4,1.2,4,98])
        self.simulation_state = SimulationState(new_instance=True, base_cache_dir=self.temp_dir)
        self.simulation_state.set_current_time(self.start_year)
        SessionConfiguration(new_instance=True,
                             in_storage=AttributeCache())
        os.makedirs(os.path.join(self.temp_dir, str(self.start_year), self.table_name))
        self.create_flt_file(self.flt_test_file_path, self.attr1_data)
        self.create_flt_file(self.flt_index_file_path, self.index_data)
    
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)




if __name__ == '__main__':
    opus_unittest.main()