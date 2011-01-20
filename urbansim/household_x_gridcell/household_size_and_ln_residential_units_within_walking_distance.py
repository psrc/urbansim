# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class household_size_and_ln_residential_units_within_walking_distance(Variable):
    """Interaction term between household size and log of density of housing within 
    the walking distance radius. [hh.people * ln_residential_units_within_walking_distance]"""
    _return_type="float32"
    gc_ln_residential_units_within_walking_distance = "ln_residential_units_within_walking_distance"
    hh_persons = "persons"
    
    def dependencies(self):
        return [attribute_label("gridcell", self.gc_ln_residential_units_within_walking_distance), 
                attribute_label("household", self.hh_persons)]

    def compute(self, dataset_pool):
        return self.get_dataset().multiply(self.hh_persons, 
                                self.gc_ln_residential_units_within_walking_distance)


from math import log
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.household_size_and_ln_residential_units_within_walking_distance"
        
    def test_my_inputs(self):
        # suppose that there are 4 grid cells, and the number of residential units within walking distance in
        # each of the cells is [7, 100, 0, 24]
        # for the ln of the number of residential units, if the number of units is 0 we use the bounded log, so
        # that the corresponding value is also 0
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'ln_residential_units_within_walking_distance': array([log(7), log(100), 0, log(24)]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3]),
                'persons': array([4, 1, 10]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name, 
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([[log(7)*4, log(100)*4, 0, log(24)*4],
                           [log(7), log(100), 0, log(24)],
                           [log(7)*10, log(100)*10, 0, log(24)*10]])
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
                     msg="Error in " + self.variable_name)
        
if __name__=='__main__':
    opus_unittest.main()