# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from .variable_functions import my_attribute_label
from numpy import arange, array

class sector_DDD_jobs_in_faz(Variable):
    """number of jobs in sector in the same fazes as this gridcell. """
    
    jobs_sector_id = "sector_id"
    gc_faz_id = "faz_id"

    def __init__(self, number):
        self.tnumber = number
        self.number_of_jobs_of_sector = "number_of_jobs_of_sector_"+str(int(self.tnumber))
        Variable.__init__(self)

    def dependencies(self):
        return [attribute_label("faz", self.number_of_jobs_of_sector), 
                my_attribute_label(self.gc_faz_id)]
        
    def compute(self, dataset_pool):
        fazes = dataset_pool.get_dataset('faz')
        gc_fazes = self.get_dataset().get_attribute(self.gc_faz_id)
        values = [fazes.get_attribute_by_id(self.number_of_jobs_of_sector, [x])[0] for x in gc_fazes]
        return array(values)
        

from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        faz_id = array([1, 2, 3, 4])
        number_of_jobs_of_sector_2 = array([1,4,2,1])
        
        grid_id = array([101,103,105,107])
        gc_faz_id = array([1, 2, 1, 3])
        
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "faz":{ 
                    "faz_id":faz_id,
                    "number_of_jobs_of_sector_2":number_of_jobs_of_sector_2
                    }, 
                "gridcell":{ 
                    "grid_id":grid_id,
                    "faz_id":gc_faz_id
                }
            }
        )
        
        should_be = array([1, 4, 1, 2])
        instance_name = "urbansim.gridcell.sector_2_jobs_in_faz"
        tester.test_is_close_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()