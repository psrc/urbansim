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
from variable_functions import my_attribute_label

class occupied_building_sqft_by_jobs(Variable):
    """sum of jobs sqft per building"""

    _return_type="int32"

    def dependencies(self):
        return ["urbansim_parcel.job.building_id",
                "urbansim_parcel.job.sqft"]

    def compute(self,  dataset_pool):
        jobs = dataset_pool.get_dataset("job")
        return self.get_dataset().sum_dataset_over_ids(jobs, "sqft")

    def post_check(self,  values, dataset_pool=None):
        size = dataset_pool.get_dataset("job").get_attribute("sqft").sum()
        self.do_check("x >= 0 and x <= " + str(size), values)

if __name__=='__main__':
    import unittest
    from numpy import array
    from numpy import ma
    from opus_core.resources import Resources
    from urbansim_parcel.datasets.building_dataset import BuildingDataset
    from urbansim.datasets.job_dataset import JobDataset
    from opus_core.storage_factory import StorageFactory

    class Tests(unittest.TestCase):
        variable_name = "urbansim_parcel.building.occupied_building_sqft_by_jobs"
        def test(self):
            storage = StorageFactory().get_storage('dict_storage')
            bs_table_name = 'job'

            storage.write_table(
                    table_name=bs_table_name,
                    table_data={"job_id": array([1,2,3,4,5,6]),
                               "sqft":        array([0,1,4,0,2,5]),
                               "building_id": array([2,1,3,2,1,2])
                               },
                )

            bs = JobDataset(in_storage=storage,
                                          in_table_name=bs_table_name)

            storage = StorageFactory().get_storage('dict_storage')
            building_table_name='building'
            storage.write_table(
                    table_name=building_table_name,
                    table_data={"building_id": array([1,2,3]),},
            )

            buildings = BuildingDataset(in_storage=storage,
                                        in_table_name=building_table_name)

            buildings.compute_variables(self.variable_name,
                                        resources=Resources({'job':bs}))
            values = buildings.get_attribute(self.variable_name)
            should_be = array([3,5,4])

            self.assertEqual(ma.allclose(values, should_be, rtol=1e-20), \
                             True, msg = "Error in " + self.variable_name)
    unittest.main()