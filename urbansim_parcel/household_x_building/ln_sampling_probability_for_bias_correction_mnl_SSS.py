# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.abstract_variables.ln_sampling_probability_for_bias_correction_mnl import ln_sampling_probability_for_bias_correction_mnl

class ln_sampling_probability_for_bias_correction_mnl_SSS(ln_sampling_probability_for_bias_correction_mnl):
    def __init__(self, attribute):
        ln_sampling_probability_for_bias_correction_mnl.__init__(self, attribute)
        
    def dependencies_to_add(self, dataset_name, package=None):
        return ln_sampling_probability_for_bias_correction_mnl.dependencies_to_add(self, dataset_name, 
                                                                                   package="urbansim_parcel")
        
        
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array, arange
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim_parcel.household_x_building.ln_sampling_probability_for_bias_correction_mnl_residential_units"
        
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')        
        
        storage.write_table(
            table_name='buildings',
            table_data={
                'building_id': arange(50),
                'residential_units': array(5*[0]+10*[20]+5*[15]+10*[50]+15*[3]+5*[45]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'],
                                   storage=storage)        
        household_x_building = dataset_pool.get_dataset('household_x_building', 
                 dataset_arguments={"index2": array([[13, 15, 23, 49],
                                                     [5, 9, 17, 43],
                                                     [17, 18, 40, 47]], dtype="int32")})
        household_x_building.compute_variables(self.variable_name)
        values = household_x_building.get_attribute(self.variable_name)

        # The values are computed using formula from Ben-Akiva book (Chapter of correcting for sampling bias)
        should_be = array([[-11.3207881 , -11.03310603, -12.23707884, -12.13171832],
                           [-15.01597613, -15.01597613, -14.72829406, -13.11885615],
                           [-14.18521949, -14.18521949, -12.57578158, -15.28383178]]) + 11.03310603
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-4), 
                     msg="Error in " + self.variable_name)
        

if __name__=='__main__':
    opus_unittest.main()