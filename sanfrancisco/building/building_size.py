#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from numarray import where, zeros
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
        return [attribute_label("building_use_classification", "name"), 
                attribute_label("building_use_classification", "units"),
                my_attribute_label("building_class_id"), 
                my_attribute_label("building_sqft"), 
                my_attribute_label("residential_units")]
        
    def compute(self,  dataset_pool):
        bt = dataset_pool.get_dataset("building_use_classification")
        types = bt.get_id_attribute()
        units = bt.get_attribute("units")
        my_type = self.get_dataset().get_attribute("building_class_id")
        result = zeros(self.get_dataset().size(), type = self._return_type)
        for itype in range(bt.size()):
            idx = where(my_type == types[itype])[0]
            units_name = units[itype]
            if re.search("building_sqft", units_name):
                attr_name = "building_sqft"
            else:
                attr_name = "residential_units"
            result[idx] = self.get_dataset().get_attribute_by_index(attr_name,idx)
        return result

import unittest
from sanfrancisco.datasets.building_use_classification_dataset import BuildingUseClassificationDataset
from urbansim.datasets.building_dataset import BuildingDataset
from opus_core.resources import Resources
from numarray import array, strings, arange
from opus_core.storage_factory import StorageFactory
from numarray.ma import allequal
class Tests(unittest.TestCase):
    variable_name = "sanfrancisco.building.building_size"

    def test_my_inputs(self):
        storage1 = StorageFactory().get_storage('dict_storage')
        bu_table_name = 'building_use_classification'
        
        storage1.write_dataset(
            Resources({
                'out_table_name':bu_table_name,
                'values': {"class_id":array([1,2]), 
                           "name": strings.array(["residential", "nonresidential"]),
                           "units": strings.array(["residential_units", "building_sqft"])
                           },
                })
            )

        building_use_classification = BuildingUseClassificationDataset(in_storage=storage1, 
                                                                       in_table_name=bu_table_name)

        storage2 = StorageFactory().get_storage('dict_storage')
        builing_table_name='building'
        storage2.write_dataset(
            Resources({
                'out_table_name':builing_table_name,
                'values': {
                    "building_id": arange(6)+1,
                    "building_class_id": array([1,2,1,2,1,1]),
                    "building_sqft": array([100, 350, 1000, 0, 430, 95]),
                    "residential_units": array([300, 0, 100, 0, 1000, 600])
                             },
                })
            )
        
        buildings = BuildingDataset(in_storage=storage2, 
                                    in_table_name=builing_table_name)
        
        buildings.compute_variables(self.variable_name, resources=Resources({"building_use_classification": building_use_classification}))

        should_be = array([300, 350, 100, 0, 1000, 600])
        values = buildings.get_attribute(self.variable_name)
        self.assertEqual(allequal(values, should_be), \
                         True, msg = "Error in " + self.variable_name)

if __name__=='__main__':
    unittest.main()