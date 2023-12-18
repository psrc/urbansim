# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.buildings_SSS_space import buildings_SSS_space as gridcell_buildings_SSS_space

class buildings_SSS_space(gridcell_buildings_SSS_space):
    """Sum of building space of given type across zones."""
        
    id_name = "zone_id"

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.buildings_residential_space"

    def test_my_inputs(self):
        """Total number of residential of buildings.
        """
        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'zone':{
                    'zone_id':array([1,2,3]),
                    },
                'building': {
                    'is_building_type_residential':array([1,0,1,0,1,1]),
                    'zone_id':array([2,3,1,1,2,1]),
                    'building_size':array([100, 350, 1000, 0, 430, 95])
                    },
                }, 
            dataset = 'zone'
            )
            
        should_be = array([1095, 530, 0])

        self.assertTrue(ma.allequal(values, should_be),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()