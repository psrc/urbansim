# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class population_per_acre(Variable):
    """The population of the faz / land acres in the faz, rounded to the nearest integer. """
    _return_type = "int32"
    gc_population = "population"
    acres_of_land = "acres_of_land"

    def dependencies(self):
        return [attribute_label("gridcell", self.gc_population),
                attribute_label("gridcell", self.acres_of_land),
                attribute_label("gridcell", "faz_id")]

    def compute(self, dataset_pool):
        population_per_faz = self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('gridcell'),
                                                                      self.gc_population)
        acres_per_faz = self.get_dataset().sum_dataset_over_ids(dataset_pool.get_dataset('gridcell'),
                                                                 self.acres_of_land)
        result = (population_per_faz / acres_per_faz.astype("float32")).round()
        result[population_per_faz == 0] = 0
        return result

    def post_check(self, values, dataset_pool):
        """Check for where there is population on fully-water fazs (e.g. on no land).
        """
        from numpy import isinf, isnan
        if isinf(values).sum():
            logger.log_error("Variable %s has %d Infinity values" %
                             (self.__class__.__module__, isinf(values).sum()))
        if isnan(values).sum():
            logger.log_error("Variable %s has %d NaN values" %
                             (self.__class__.__module__, isnan(values).sum()))


from numpy import array, inf, ma, int32

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.faz.population_per_acre"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='fazes',
            table_data={
                "faz_id":array([1,2, 3, 4, 5]),
            }
        )
        storage.write_table(
            table_name='gridcells',
            table_data={
                "population": array([100,200,300,400,500,0]),
                "percent_water": array([0,30,0,0,100,100]),
                "faz_id": array([1,2,1,3,4,5]),
                "grid_id": array([1,2,3,4,5,6]),
            }
        )
        storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "acres": array([105.0]),
            }
        )

        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        faz = dataset_pool.get_dataset('faz')
        faz.compute_variables(self.variable_name,
                               dataset_pool=dataset_pool)
        values = faz.get_attribute(self.variable_name)

        inf_as_int32 = array([inf]).astype(int32)[0]
        should_be = array([400/(2*105.0), 200/(105.0*0.7), 400/105.0, inf_as_int32, 0.0]).round()

        self.assert_(ma.allclose(values, should_be, rtol=1e-7),
                     msg="Error in " + self.variable_name)



if __name__=='__main__':
    opus_unittest.main()