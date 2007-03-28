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

from numpy import where, zeros
import re
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class building_size(Variable):
    """Return size of the building, either sqft, or residential units, depending on the building type. 
    If the value in column 'units' of the building_types table contains a substring 'sqft', it will take 
    the 'sqft' of the buildings table as a measure of size, otherwise 'residential_units'.
    """
    _return_type="Int32"
    
    def dependencies(self):
        return [attribute_label("building_type", "name"), attribute_label("building_type", "units"),
                my_attribute_label("building_type_id"), my_attribute_label("sqft"), my_attribute_label("residential_units")]
        
    def compute(self, dataset_pool):
        bt = dataset_pool.get_dataset('building_type')
        types = bt.get_id_attribute()
        units = bt.get_attribute("units")
        my_type = self.get_dataset().get_attribute("building_type_id")
        result = zeros(self.get_dataset().size(), type = self._return_type)
        for itype in range(bt.size()):
            idx = where(my_type == types[itype])[0]
            units_name = units[itype]
            if re.search("sqft", units_name):
                attr_name = "sqft"
            else:
                attr_name = "residential_units"
            result[idx] = self.get_dataset().get_attribute_by_index(attr_name,idx)
        return result

from opus_core.tests import opus_unittest
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from urbansim.datasets.building_dataset import BuildingDataset
from opus_core.resources import Resources
from numpy import array, strings, arange
from numpy.ma import allequal
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.building.building_size"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        building_types_table_name = 'building_types'        
        storage.write_dataset(
            Resources({
                'out_table_name':building_types_table_name,
                'values':{
                    'building_type_id':array([1,2]), 
                    'name': strings.array(['residential', 'commercial']),
                    'units': strings.array(['residential_units', 'commercial_sqft'])
                    }
                })
            )

        buildings_table_name = 'buildings'        
        storage.write_dataset(
            Resources({
                'out_table_name':buildings_table_name,
                'values':{
                     'building_id': arange(6)+1,
                     'building_type_id': array([1,2,1,2,1,1]),
                     'sqft': array([100, 350, 1000, 0, 430, 95]),
                     'residential_units': array([300, 0, 100, 0, 1000, 600])
                     }
                })
            )

        building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)
        buildings = BuildingDataset(in_storage=storage, in_table_name=buildings_table_name)
        
        buildings.compute_variables(self.variable_name, resources=Resources({'building_type': building_types}))

        should_be = array([300, 350, 100, 0, 1000, 600])
        values = buildings.get_attribute(self.variable_name)
        
        self.assert_(allequal(values, should_be),
            'Error in ' + self.variable_name)

if __name__=='__main__':
    opus_unittest.main()