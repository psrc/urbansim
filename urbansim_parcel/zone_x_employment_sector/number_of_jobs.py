# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 
from opus_core.variables.variable import Variable
from numpy import zeros

class number_of_jobs(Variable):
    """Number of jobs for each zone and sector """
        
    _return_type = 'int32'
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        sector_ids = ds.get_dataset(2).get_id_attribute()
        result = zeros(ds.size()[0], dtype=self._return_type)
        for isector in range(sector_ids.size):
            varname = 'urbansim_parcel.zone.number_of_jobs_of_sector_%s' % sector_ids[isector]
            self.add_and_solve_dependencies([varname], dataset_pool=dataset_pool)
            result[:,isector] = ds.get_attribute_of_dataset(varname)
        return result

    
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import arange, array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
        
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            "zone":{ 
                 "zone_id": arange(1,3)
                    }, 
             "employment_sector":{ 
                 "id":arange(1,6)
                              },
             "job":{
                 "job_id": arange(1,21),
                 "sector_id": array([1, 1,2, 3, 2,4,1,2,6,5, 3,1, 3, 2, 1, 5,5, 6,5, 1]),
                 "zone_id":   array([1, 2,2, 1, 2,1,1,1,1,2, 2,1, 2, 1, 2, 2,1, 1,1, 2])
                       }
             })
        should_be = array([[3,2,1,1, 2],[3, 2, 2, 0, 2]])
                            
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()