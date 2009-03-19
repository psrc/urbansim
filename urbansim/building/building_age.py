# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import ma, maximum, logical_not
from opus_core.simulation_state import SimulationState

class building_age(Variable):
    """The age of buildings, computed by subtracting the year built
    from the current simulation year. All values that have year_built < urbansim_constant["absolute_min_year"]
    are masked.
    """
    _return_type = "int32"

    year_built = "year_built"
    is_valid_year_built = "is_valid_year_built"

    def dependencies(self):
        return [my_attribute_label(self.year_built), my_attribute_label(self.is_valid_year_built)]

    def compute(self, dataset_pool):
        current_year = SimulationState().get_current_time()

        if current_year == None:
            raise StandardError, "'SimulationState().get_current_time()' returns None."
        building_age = maximum(0, current_year - self.get_dataset().get_attribute(self.year_built))
        return ma.masked_where(logical_not(self.get_dataset().get_attribute(self.is_valid_year_built)),
                             building_age)

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.building.building_age"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='buildings',
            table_data={
                'building_id': array([1,2,3,4]),
                'year_built': array([1995, 2000, 2006, 0])
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "absolute_min_year": array([1800]),
            }
        )

        SimulationState().set_current_time(2005)
        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        buildings = dataset_pool.get_dataset('building')
        buildings.compute_variables(self.variable_name,
                                   dataset_pool=dataset_pool)
        values = buildings.get_attribute(self.variable_name)

        should_be = array([10, 5, 0, -99])

        self.assert_(ma.allequal( values, should_be),
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()