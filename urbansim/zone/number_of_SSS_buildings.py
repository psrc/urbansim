# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.gridcell.number_of_SSS_buildings import number_of_SSS_buildings as gridcell_number_of_SSS_buildings
from urbansim.functions import attribute_label

class number_of_SSS_buildings(gridcell_number_of_SSS_buildings):
    """Computes the number of buildings of the given type for a zone. It inherits
        most of the code from the gridcell variable of the same name.
    """

    def dependencies(self):
        return [attribute_label("building", "zone_id"), 
                attribute_label("building", self.is_building_type)]

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.number_of_single_family_buildings"

    def test_my_inputs(self):
        grid_id = array([1, 2, 3])
        #specify an array of 4 buildings, 1st buildings's grid_id = 2 (it's in gridcell 2), etc.
        b_grid_id = array([2, 1, 3, 1])
        #corresponds to above building array, specifies which buildings in which locations are in the group of interest
        single_family = array([0, 1, 1, 1]) 

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            { "zone":{ 
                  "zone_id":grid_id }, 
              "building":{ 
                  "zone_id":b_grid_id, 
                  "is_building_type_single_family":single_family} }, 
              dataset = "zone" )
        should_be = array([2, 0, 1])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()