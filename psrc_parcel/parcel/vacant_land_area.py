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

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label

class vacant_land_area(Variable):
    """parcel lot size minus land area of all buildings in the parcel;
    it's land area that is available for future development
    """

    _return_type="Int32"
    
    def dependencies(self):
        return ["used_land_area = parcel.aggregate(building.land_area_sqft, function=sum)",
                my_attribute_label("lot_size_sqft")]

    def compute(self,  dataset_pool):
        parcels = self.get_dataset()
        return parcels.get_attribute("lot_size_sqft") - parcels.get_attribute("used_land_area")

    def post_check(self,  values, dataset_pool=None):
        size = self.get_dataset().get_attribute("lot_size_sqft").max()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numpy import array
    from numpy import ma
    from opus_core.resources import Resources
    from psrc_parcel.datasets.parcel_dataset import ParcelDataset
    from psrc_parcel.datasets.building_dataset import BuildingDataset
    from opus_core.storage_factory import StorageFactory    
    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.parcel.vacant_land_area"
        def test_my_inputs(self):
            storage1 = StorageFactory().get_storage('dict_storage')
            parcels_table_name = 'parcels'            
            storage1.write_dataset(
                Resources({
                    'out_table_name':parcels_table_name,
                    'values':{
                        'parcel_id':array([1,2,3]),
                        "lot_size_sqft":array([1000,200,1300]),
                        },
                    })
                )
    
            parcels = ParcelDataset(in_storage=storage1, in_table_name=parcels_table_name)

            
            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"parcel":parcels, \
                 "building":{
                        'building_id':     array([1,   2,   3,   4,   5,   6,   7]),
                        'parcel_id':       array([1,   1,   2,   3,   3,   3,   3]),
                        "land_area_sqft":  array([600, 400, 100, 300, 150, 400, 400]),
                        },}, \
                dataset = "parcel")
            should_be = array([0,100,50])
            
            self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()