# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import arange, array

class same_household_age_in_faz(Variable):
    """Number of households in the FAZ (of this gridcell) of same age as this household.
    Uses five categories: <30, 30-39, 40-49, 50-64, and 65+."""

    hh_age = "age_of_head"
    gc_faz_id = "faz_id"

    def dependencies(self):
        return [attribute_label("household", self.hh_age),
                attribute_label("gridcell", self.gc_faz_id),
                attribute_label("faz", "same_household_age")]

    def compute(self, dataset_pool):
        fazes = dataset_pool.get_dataset('faz')
        gc_fazes = self.get_dataset().get_2d_dataset_attribute(self.gc_faz_id)
        return fazes.get_value_from_same_age_table(self.get_dataset().get_attribute_of_dataset(self.hh_age),
                                                      gc_fazes)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.household_x_gridcell.same_household_age_in_faz"
    #EXAMPLE FOR TUTORIAL
    def test_full_tree(self):
        """This is an "interaction variable", i.e. it depends on both the gridcell and household
        datasets, and thus, it is in the household_x_gridcell "category"."""

        #declare five households, three of which whose age of head is 40, 4th is 50, 5th is 35
        age_of_head = array([40, 40, 40, 50, 35])
        #declare four gridcells, two of which are in Forecast Analysis Zone #1, and others in FAZ #2, #3
        gridcell_faz_id = array([1, 3, 2, 1])
        #assign gridcell id's to the five households. here, households #1 and #3 are in the same gridcell
        household_grid_id = array([2, 1, 2, 4, 4])

        #Imagine a 5x4 grid, where the origin is at the upper left. on the vertical axis are the five households,
        #and on the horizontal axis are the four gridcells, numbered 1-4 (grid id).
        #fill in each square by answering the question:
        #for the age of this row's household, how many other households in that column's gridcell faz are
        #have the same age? if the row's household lives in that faz, include it in the count.


        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"gridcell":{
                "faz_id":gridcell_faz_id},
             "household":{
                "age_of_head":age_of_head,
                "grid_id":household_grid_id},
             "faz":{
                 "faz_id":array([1,2,3]) } },
            dataset = "household_x_gridcell")

        #what the result says here is that for household #1 (age = 20), there is 1 household of the same age
        #in gridcelll #1's FAZ. there are 2 households of the same age in gridcell #2's FAZ...
        should_be = array([[1, 2, 0, 1],
                           [1, 2, 0, 1],
                           [1, 2, 0, 1],
                           [1, 0, 0, 1],
                           [1, 0, 0, 1]])

        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()