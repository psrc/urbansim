# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.logger import logger
from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from numpy import zeros, float32
from variable_functions import my_attribute_label

class travel_time_hbw_am_drive_alone_from_home_to_work(Variable):
    """Travel time frome home zone to work zone.
    The travel time used is for the home-based-work am trips by auto with 
    drive-alone.
    """

    def dependencies(self):
        return [my_attribute_label("home_zone_id"),
                my_attribute_label("work_place_zone_id"),
                attribute_label("travel_data", 'am_single_vehicle_to_work_travel_time'),
                ]
    
    def compute(self, dataset_pool):
        persons = self.get_dataset()
        homes = persons.get_attribute("home_zone_id")
        workplaces = persons.get_attribute("work_place_zone_id")
        
        keys = map(lambda x, y: (x, y), homes, workplaces)
        travel_data = dataset_pool.get_dataset('travel_data')
        try:
            time = travel_data.get_attribute_by_id("am_single_vehicle_to_work_travel_time", keys)
        except:
            logger.log_warning("Variable %s returns zeros, since zone number %d is not in zoneset." % (self.variable_name, self.tnumber))
            time = zeros(self.get_dataset().size(), dtype=float32)
        return time


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
        
        self.assert_(ma.allclose(values, should_be, rtol=1e-2),
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()