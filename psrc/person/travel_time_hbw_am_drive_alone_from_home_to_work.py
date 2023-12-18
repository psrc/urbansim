# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_travel_time_variable_for_non_interaction_dataset import abstract_travel_time_variable_for_non_interaction_dataset

class travel_time_hbw_am_drive_alone_from_home_to_work(abstract_travel_time_variable_for_non_interaction_dataset):
    """Travel time frome home zone to work zone.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """
    
    default_value = 999
    origin_zone_id = 'psrc.person.home_zone_id'
    destination_zone_id = 'psrc.person.work_place_zone_id'
    travel_data_attribute = 'travel_data.am_single_vehicle_to_work_travel_time'

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person.travel_time_hbw_am_drive_alone_from_home_to_work"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5]),
                    'household_id':array([1, 1, 3, 3, 3]),
                    'member_id':array([1,2,1,2,3]),
                    'home_zone_id':      array([3, 1, 1, 2, 3]),
                    'work_place_zone_id':array([1, 3, 3, 1, 2])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)        

        values = VariableTestToolbox().compute_variable(self.variable_name,
            data_dictionary = {
                'person':persons,
                'travel_data':{
                    'from_zone_id':array([3,3,1,1,1,2,2,3,2]),
                    'to_zone_id':  array([1,3,1,3,2,1,3,2,2]),
                    'am_single_vehicle_to_work_travel_time':array([1.1, 2.2, 3.3, 4.4, 0.5, 0.7, 8.7, 7.8, 1.0])
                    }
                },
            dataset = 'person'
            )
            
        should_be = array([1.1, 4.4, 4.4, 0.7, 7.8])
        
        self.assertTrue(ma.allclose(values, should_be, rtol=1e-2),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()