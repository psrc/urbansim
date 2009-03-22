# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, logical_and

class commute_trips(Variable):
    """
    """
            
    def dependencies(self):
        return ["home_district_id = person.disaggregate(zone.district_id, intermediates=[parcel, building, household])",
                "workplace_district_id = person.disaggregate(zone.district_id, intermediates=[parcel, building, job])", 
               ]

    def compute(self,  dataset_pool):
        dc = self.get_dataset()
        results = zeros(dc.size(), dtype='int32')
        
        persons = dataset_pool.get_dataset("person")
        home_district_id = persons.get_attribute("home_district_id")
        workplace_district_id = persons.get_attribute("workplace_district_id")
        origin_array = dc.get_attribute("origin_district_id")
        distination_array = dc.get_attribute("destination_district_id")
        
        for i in range(dc.size()):
            results[i] = logical_and(home_district_id==origin_array[i], 
                                     workplace_district_id==distination_array[i]).sum()
        return results

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel','urbansim_parcel', 'urbansim'],
            test_data={
                'district_commute':
                    { 'commute_id':arange(1, 10),
                      'origin_district_id':     array([1, 1, 1, 3, 3, 3, 4, 4, 4]),
                      'destination_district_id':array([1, 3, 4, 1, 3, 4, 1, 3, 4])
                     },
                'zone':
                    {
                     'zone_id':     array([1, 2, 3, 4, 5, 6]),
                     'district_id': array([1, 1, 3, 4, 4, 4])
                     },
                'parcel':
                    {
                     'parcel_id': array([1, 2, 3, 4, 5, 6, 7, 8]),
                     'zone_id':   array([1, 2, 3, 3, 4, 1, 4, 4])
                     },
                'building':
                    {
                     'building_id': array([1, 2, 3, 4, 5, 6, 7, 8, 9]),
                     'parcel_id':   array([1, 2, 2, 3, 4, 5, 7, 7, 8])
                     },
                'household':
                    {
                     'household_id': array([1, 2, 3, 4, 5, 6, 7]),
                     'building_id':  array([1, 1, 2, 3, 8, 4, 7])
                     },
                'job':
                    {
                     'job_id':      array([1, 2, 3, 4, 5, 6]),
                     'building_id': array([2, 8, 7, 3, 1, 2])
                     },
                'person':
                    {
                     'person_id':    array([1, 2, 3, 4, 5, 6, 7, 8]),
                     'household_id': array([1, 1, 7, 3, 4, 4, 5, 6]),  #home_district_id: 1, 1, 4, 1, 1, 1, 4, 3 
                     'job_id':       array([-1,2,-1, 3, 1, 4,-1, 5])   #work_district_id:-1, 4,-1, 4, 1, 1,-1, 1 
                     },
                     
                    }
        )
        
        should_be = array([2, 0, 2, 1, 0, 0, 0, 0, 0])

        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()