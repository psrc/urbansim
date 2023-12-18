# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from numpy import logical_and

class is_transition_to_developed(Variable):
    """Returns a boolean indicating whether this development_event is a transition 
    to developed"""

    def dependencies(self):
        return [my_attribute_label("is_transition_from_development_type_group_vacant_developable"),
                my_attribute_label("is_transition_to_development_type_group_developed")]

    def compute(self, dataset_pool):
        development_events = self.get_dataset()
        return logical_and(
                 development_events.get_attribute("is_transition_from_development_type_group_vacant_developable"),
                 development_events.get_attribute("is_transition_to_development_type_group_developed")
                 )                                     

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)
        

from opus_core.tests import opus_unittest
from opus_core.variables.attribute_box import AttributeBox
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from numpy import ma

#emulates the employmentsector resource and implements the method we're interested in (are_in_group)
class mock_developmenttype(object):
    def __init__(self):
        pass

    def are_in_group(self, ids, group):
        groups = {}
        groups[1] = array([1,2]) #define sector 1 to be in group 1 and group 2
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
    variable_name = "urbansim.development_event.is_transition_to_developed"

    def test_my_tree( self ):
        storage = StorageFactory().get_storage('dict_storage')
        
        #declare an array of four gridcells, each with the specified sector ID below
        storage.write_table(
            table_name='development_events',
            table_data={
                'grid_id': array([100,100,101,102]),
                'scheduled_year': array([1999,1998,1999,1999]),
                'starting_development_type_id': array([1, 3, 1, 3]),
                'ending_development_type_id': array([1, 2, 2, 3]),
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
        development_event.compute_variables(self.variable_name, 
                                            dataset_pool=dataset_pool)
        values = development_event.get_attribute(self.variable_name)
        
        should_be = array( [True, False, True, False] )
        self.assertTrue(ma.allequal( values, should_be), 
                     msg = "Error in " + self.variable_name )

if __name__=='__main__':
    opus_unittest.main()