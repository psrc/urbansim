# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class percent_minority_households_within_walking_distance_if_minority(Variable):
    """Percent of households' heads within the walking radius that are in a minority race,
    given that the decision-making household's head is in a minority race.
    [percent_minority_households_within_walking_distance if hh.is_minority is true else 0]"""

    gc_percent_minority_households_within_walking_distance = \
      "percent_minority_households_within_walking_distance"
    hh_is_minority = "is_minority"

    def dependencies(self):
        return [attribute_label("gridcell", self.gc_percent_minority_households_within_walking_distance),
                attribute_label("household", self.hh_is_minority)]

    def compute(self, dataset_pool):
        return self.get_dataset().interact_attribute_with_condition(
                                            self.gc_percent_minority_households_within_walking_distance,
                                            self.hh_is_minority)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.percent_minority_households_within_walking_distance_if_minority"

    def test_full_tree(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3,4]),
                'relative_x': array([1,2,1,2]),
                'relative_y': array([1,1,2,2]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4, 5, 6]),
                'grid_id': array([1, 2, 3, 4, 2, 2]),
                'is_minority': array([1, 0, 1, 0, 0, 1]),
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "walking_distance_circle_radius": array([150]),
                'cell_size': array([150]),
            }
        )

        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name,
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)

        should_be = array([[100*(5.0/7.0), 100*(4.0/11.0), 80.0, 100*(2.0/7.0)],
                           [0,0,0,0],
                           [100*(5.0/7.0), 100*(4.0/11.0), 80.0, 100*(2.0/7.0)],
                           [0,0,0,0],
                           [0,0,0,0],
                           [100*(5.0/7.0), 100*(4.0/11.0), 80.0, 100*(2.0/7.0)]])

        self.assert_(ma.allclose(values, should_be, rtol=1e-7),
                     msg="Error in " + self.variable_name)

    def test_my_inputs(self):
        """Percent of households within walking distance that are minority.
        """
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='gridcells',
            table_data={
                'grid_id': array([1,2,3]),
                'percent_minority_households_within_walking_distance': array([50, 0, 15]),
            }
        )
        storage.write_table(
            table_name='households',
            table_data={
                'household_id': array([1, 2, 3, 4]),
                'grid_id': array([1, 2, 3, 4]),
                'is_minority': array([1, 0, 1, 1]),
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "walking_distance_circle_radius": array([150]),
                'cell_size': array([150]),
            }
        )

        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        household_x_gridcell = dataset_pool.get_dataset('household_x_gridcell')
        household_x_gridcell.compute_variables(self.variable_name,
                                               dataset_pool=dataset_pool)
        values = household_x_gridcell.get_attribute(self.variable_name)

        should_be = array([[50, 0, 15],
                           [0, 0, 0],
                           [50, 0, 15],
                           [50, 0, 15]])

        self.assert_(ma.allclose(values, should_be, rtol=1e-7),
                     msg="Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()