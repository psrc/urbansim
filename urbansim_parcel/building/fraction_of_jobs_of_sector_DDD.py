# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.misc import safe_array_divide
from opus_core.variables.variable import Variable

class fraction_of_jobs_of_sector_DDD(Variable):
    """ Fraction of jobs of sector DDD in buildings."""
    
    def __init__(self, sector_id):
        self.sector_id = sector_id
        Variable.__init__(self)
        
    def dependencies(self):
        return ["urbansim_parcel.building.number_of_jobs", 
                "urbansim_parcel.building.number_of_jobs_of_sector_%s" % self.sector_id]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return safe_array_divide(ds["number_of_jobs_of_sector_%s" % self.sector_id], ds["number_of_jobs"])

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim_parcel.building.fraction_of_jobs_of_sector_3"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
  
        storage.write_table(
                 table_name='buildings',
                 table_data={
                    'building_id':      array([1, 2, 3]),
                    }
                )
        storage.write_table(
                 table_name='jobs',
                 table_data={
                    'job_id':      array([1, 2, 3, 4, 5, 6]),
                    'sector_id':   array([1, 1, 3, 2, 3, 3]),
                    'building_id': array([1, 1, 1, 2, 3, 3])
                    }
                )
        dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=storage)
        buildings = dataset_pool.get_dataset('building')
        
        values = buildings.compute_variables(self.variable_name, dataset_pool=dataset_pool)
        
        should_be = array([1/3., 0, 1])
        
        self.assert_(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()