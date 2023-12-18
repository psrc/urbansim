# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.development_event.is_transition_from_development_type_group_SSS import \
    is_transition_from_development_type_group_SSS as from_var
    

class is_transition_to_development_type_group_SSS(from_var):

    devtype_id = "ending_development_type_id"
        

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.variables.attribute_box import AttributeBox
from numpy import array
from numpy import ma

#emulates the development_type resource and implements the method we're interested in (are_in_group)
class mock_developmenttype(object):
    def __init__(self):
        pass

    def are_in_group(self, ids, group):
        groups = {}
        groups[1] = array([1,2]) #define devtype 1 to be in group 1 and group 2
        groups[2] = array([2])
        groups[3] = array([3])
        def func(idx):
            try:
                return group in groups[idx]
            except:
                return False
        return array([func(x) for x in ids])

    def compute_variables_return_versions_and_final_value(self, name, *args, **kwargs):
        return ([0], array([1,2,3]))
    
    def _get_attribute_box(self, name):
        return AttributeBox(self, None, name.get_alias())


class Tests(opus_unittest.OpusTestCase):
    variable_name1 = "urbansim.development_event.is_transition_to_development_type_group_vacant_developable"
    variable_name2 = "urbansim.development_event.is_transition_to_development_type_group_developed"
    
    def test_my_inputs( self ):
        storage = StorageFactory().get_storage('dict_storage')
        
        #declare an array of four gridcells, each with the specified sector ID below
        storage.write_table(
            table_name='development_events',
            table_data={
                'grid_id': array([100,100,101,102]),
                'scheduled_year': array([1999,1998,1999,1999]),
                'starting_development_type_id': array([1, 3, 2, 3]),
                'ending_development_type_id': array([1, 1, 2, 3]),
            }
        )
        storage.write_table(
            table_name='development_type_groups',
            table_data={
                'name': array(["vacant_developable", "developed"]),
                'group_id': array([1,2]),
            }
        )
        
        dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
                                   storage=storage)
        dataset_pool._add_dataset('development_type', mock_developmenttype())
        
        development_event = dataset_pool.get_dataset('development_event')
        
        # Test variable 1
        development_event.compute_variables(self.variable_name1, 
                                            dataset_pool=dataset_pool)
        values = development_event.get_attribute(self.variable_name1)
        
        should_be = array( [True, True, False, False] )
        self.assertTrue(ma.allequal( values, should_be), 
                     msg = "Error in " + self.variable_name1 )
                          
        # Test variable 2
        development_event.compute_variables(self.variable_name2, 
                                            dataset_pool=dataset_pool)
        values = development_event.get_attribute(self.variable_name2)
        
        should_be = array( [True, True, True, False] )
        self.assertTrue(ma.allequal( values, should_be), 
                     msg = "Error in " + self.variable_name2 )

if __name__=='__main__':
    opus_unittest.main()        