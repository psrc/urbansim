# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label

class occupation(Variable):
    """The parcel_id of a person's work place."""

    def dependencies(self):
        return [
                attribute_label("work_place","occup"),
                attribute_label("work_place","person_id"),
                ]
        
    def compute(self, dataset_pool):
        work_places = dataset_pool.get_dataset('work_place')
        return self.get_dataset().get_join_data(work_places, name="occup")
    

from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset
from psrc.datasets.work_place_dataset import WorkPlaceDataset
from opus_core.storage_factory import StorageFactory


class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.person.occupation"
    
    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':array([1, 2, 3, 4, 5]),
                    'household_id':array([1, 1, 3, 3, 3]),
                    'member_id':array([1,2,1,2,3]),
                    'work_place_id':array([1, 2, 3, 4, -1]),                                    
                    },
            )

        work_places_table_name = 'jobs'
        storage.write_table(
                table_name=work_places_table_name,
                table_data={
                    'work_place_id':array([1, 2, 3, 4]),
                    'person_id':array([1,2,3,4]),
                    'occup':  array([5,6,7,6])
                    },
            )

        persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)
        work_places = WorkPlaceDataset(in_storage=storage, in_table_name=work_places_table_name)
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            data_dictionary = {
                'work_place':work_places,
                'person':persons
                },
            dataset = 'person'
            )
            
        should_be = array([5, 6, 7, 6, -1])

        self.assert_(ma.allclose(values, should_be, rtol=1e-7), 
            'Error in ' + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()