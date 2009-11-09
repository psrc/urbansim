# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label

class is_in_employment_sector_group_SSS(Variable):
    """Is this job in a sector that is a part of group SSS. """

    sector_id = "sector_id"
    gr_name = "name"

    def __init__(self, group):
        self.group = group
        Variable.__init__(self)


    def dependencies(self):
        return [attribute_label("employment_sector_group", "group_id"),
                attribute_label("employment_sector_group", self.gr_name),
                my_attribute_label(self.sector_id),
                attribute_label("employment_sector", "sector_id")]

    def compute(self, dataset_pool):
        groups = dataset_pool.get_dataset('employment_sector_group')
        group_id = groups.get_id_attribute()[groups.get_attribute(self.gr_name)==self.group][0]
        return dataset_pool.get_dataset('employment_sector').are_in_group(self.get_dataset().get_attribute(self.sector_id), group_id)

    def post_check(self, values, dataset_pool):
        self.do_check("x == 0 or x==1", values)


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.variables.attribute_box import AttributeBox
from numpy import array
from numpy import ma

#emulates the employmentsector resource and implements the method we're interested in (are_in_group)
class mock_employmentsector(object):
    def __init__(self):
        pass

    def are_in_group(self, ids, group):
        groups = {}
        groups[1] = array([1,2]) #"sector 1 is in group 1 and group 2"
        groups[2] = array([2])
        groups[3] = array([3])
        def func(idx):
            try:
                return group in groups[idx]
            except:
                return False
        return array(map(lambda x: func(x), ids))

    def compute_variables_return_versions_and_final_value(self, name, *args, **kwargs):
        return ([0], array([1,2,3]))

    def _get_attribute_box(self, name):
        return AttributeBox(self, None, name.get_alias())

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.job.is_in_employment_sector_group_basic"

    def test_my_inputs( self ):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='jobs',
            table_data={
                'job_id': array([1,2,3,4]),
                'sector_id': array([1, 3, 2, 3]),
            }
        )
        storage.write_table(
            table_name='employment_sectors',
            table_data={
                'sector_id': array([1,2]),
                'name': array(["basic", "retail"]),
            }
        )
        storage.write_table(
            table_name='employment_adhoc_sector_groups',
            table_data={
                'group_id': array([1,2]),
                'name': array(["basic", "retail"]),
            }
        )
        storage.write_table(
            table_name='employment_adhoc_sector_group_definitions',
            table_data={
                'sector_id': array([1,2]),
                'group_id': array([1,2]),
            }
        )

        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)
        dataset_pool._add_dataset('employment_sector',
                                 mock_employmentsector())

        job = dataset_pool.get_dataset('job')
        job.compute_variables(self.variable_name,
                              dataset_pool=dataset_pool)
        values = job.get_attribute(self.variable_name)

        should_be = array( [True, False, False, False] )

        self.assert_(ma.allequal(values, should_be),
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()