# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.abstract_variables.abstract_commute_trips import abstract_commute_trips

class school_trips(abstract_commute_trips):
    """
    """
    origin_person_variable = "home_district_id = person.disaggregate(zone.district_id, intermediates=[parcel, building, household])"
    destination_person_variable = "school_district_id = person.disaggregate(zone.district_id, intermediates=[parcel, school])"  
 

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
                'school':
                    {
                     'school_id': array([1, 2, 3, 4, 5, 6]),
                     'parcel_id': array([2, 8, 7, 3, 1, 2])
                     },
                'person':
                    {
                     'person_id':    array([1, 2, 3, 4, 5, 6, 7, 8]),
                     'household_id': array([1, 1, 7, 3, 4, 4, 5, 6]), #home_district_id:   1, 1, 4, 1, 1, 1, 4, 3 
                     'school_id':    array([-1,2,-1, 3, 1, 4,-1, 5])  #school_district_id:-1, 4,-1, 4, 1, 3,-1, 1 
                     },
                     
                    }
        )
        
        should_be = array([1, 1, 2, 1, 0, 0, 0, 0, 0])

        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()