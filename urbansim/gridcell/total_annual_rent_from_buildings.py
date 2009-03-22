# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class total_annual_rent_from_buildings(Variable):
    """Total annual rent computed by dividing the total residential value of the gridcell
    by the number of residential units (quantities derived from buildings), and then dividing that figure by the 
    property value to annual cost ratio."""
    _return_type="float32"
    avg_val_per_unit = "avg_val_per_unit_residential"

    def dependencies(self):
        return [my_attribute_label(self.avg_val_per_unit)]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute(self.avg_val_per_unit) / \
               float(dataset_pool.get_dataset('urbansim_constant')["property_value_to_annual_cost_ratio"])



from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.gridcell.total_annual_rent_from_buildings"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'avg_val_per_unit_residential': array([25, 50, 75]),
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                'property_value_to_annual_cost_ratio': array([50]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        gridcell = dataset_pool.get_dataset('gridcell')
        gridcell.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = gridcell.get_attribute(self.variable_name)
        
        should_be = array([25/50.0, 1, 75/50.0])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()