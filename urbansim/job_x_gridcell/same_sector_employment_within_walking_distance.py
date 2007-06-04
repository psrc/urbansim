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

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label, create_dependency_name_with_number
from numpy import array, arange

class same_sector_employment_within_walking_distance(Variable):
    """Sum over c in cell.walking_radius, count of j in c.placed_jobs where j.sector = job.sector."""
        
    jobs_sector_id = "sector_id"
    
    def dependencies(self):
        return [attribute_label("job", self.jobs_sector_id)] + \
            create_dependency_name_with_number("sector_DDD_employment_within_walking_distance", "gridcell", range(1,19))
        
    def compute(self, dataset_pool):
        index = self.get_dataset().get_index(2)
        if index == None:
            index = arange(self.get_dataset().get_m())
        values = map(lambda x,y: self.get_dataset().get_dataset(2).get_attribute_by_index("sector_"+str(int(x))+"_employment_within_walking_distance",y), 
            self.get_dataset().get_attribute_of_dataset(self.jobs_sector_id), index)
        return array(values)
        

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job_x_gridcell.same_sector_employment_within_walking_distance"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage._write_dataset(
            'jobs',
            {
                'job_id': array([1,2,3,4]),
                'sector_id': array([2,1,2,3]),
                'grid_id': array([1,2, 3, 4]),
            }
        )
        storage._write_dataset(
            'gridcells',
            {
                'grid_id': array([1,2,3,4]),
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
            }
        )
        storage._write_dataset(
            'urbansim_constants',
            {
                "walking_distance_circle_radius": array([150]),
                'cell_size': array([150]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)
        job_x_gridcell = dataset_pool.get_dataset('job_x_gridcell')
        job_x_gridcell.compute_variables(self.variable_name, 
                                         dataset_pool=dataset_pool)
        values = job_x_gridcell.get_attribute(self.variable_name)
        
        should_be = array([4,3,4,3])
        
        self.assert_(ma.allequal(values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()