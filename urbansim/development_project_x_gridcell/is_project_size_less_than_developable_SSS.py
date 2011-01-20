# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import ma
from urbansim.functions import attribute_label

class is_project_size_less_than_developable_SSS(Variable):
    """utility_for_transit_walk if persons=1, 0 otherwise"""

    def __init__(self, type):
        Variable.__init__(self)
        self.type = type

    def dependencies(self):
        return [attribute_label("gridcell", "developable_" + self.type),
                attribute_label("development_project", self.type)]

    def compute(self, dataset_pool):
        return self.get_dataset().is_less_or_equal(self.type, "developable_" + self.type)


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.development_project_x_gridcell.is_project_size_less_than_developable_residential_units"

    # TODO: this tests most of the tree, but not quite the full tree.  To
    # test the full tree, the grid cells should be given their
    # DEVELOPMENT_TYPE_ID plain, rather than using
    # is_in_development_type_group_mixed_use
    # Fix this (maybe low priority though, since if
    # is_in_development_type_group_mixed_use is working
    # this is OK)
    def test_most_of_tree(self):
        developable_residential_units = array([10, 75, 6])
        project_residential_units = array([30,31,5,7, 0, 100])


        values = VariableTestToolbox().compute_variable(self.variable_name,
            {"gridcell":{
                "developable_residential_units":developable_residential_units},
             "development_project":{
                 "residential_units":project_residential_units}},
            dataset = "development_project_x_gridcell")
        should_be = array([[0,1,0],
                           [0,1,0],
                           [1,1,1],
                           [1,1,0],
                           [1,1,1],
                           [0,0,0]])

        self.assertEqual(ma.allclose(values, should_be, rtol=1e-5), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()