# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc.abstract_variables.abstract_travel_data_h5_income_variable_DDDtoDDD import abstract_travel_data_h5_income_variable_DDDtoDDD

class travel_distance_from_home_to_work_DDDtoDDD(abstract_travel_data_h5_income_variable_DDDtoDDD):
    """Travel distance from home to work obtained from hdf5 skims. Time periods can be 
        given in the variable name, e.g. travel_distance_from_home_to_work_6to8.
        
    """
    default_value = 0
    origin_zone_id = "residence_zone_id = person.disaggregate(urbansim_parcel.household.zone_id)"
    destination_zone_id = "workplace_zone_id = urbansim_parcel.person.workplace_zone_id"
    travel_data_attribute = "svtlINCd"
    income_groups_attribute = "psrc_parcel.person.income_groups_for_tm"
    
    def __init__(self, from_time, to_time):
        abstract_travel_data_h5_income_variable_DDDtoDDD.__init__(self, from_time, to_time)
    
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import ma, array
import h5py
from shutil import rmtree
from tempfile import mkdtemp
import os

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.person.travel_distance_from_home_to_work_5to6"
    def setUp(self):
        self.dist5to6i1 = array([[1, 30.6, 50.3],
                                 [40.9, 1, 108],
                                 [66.4, 121, 1]])
        self.dist5to6i2 = self.dist5to6i1 + 6
        self.temp_dir = mkdtemp(prefix='psrc_parcel_test_travel_data_h5')
        f = h5py.File(os.path.join(self.temp_dir, "5to6.h5"), "w")
        group = f.create_group("Skims")
        group.create_dataset("svtl1d", data=self.dist5to6i1)
        group.create_dataset("svtl2d", data=self.dist5to6i2)
        f.close()
        
    def tearDown(self):
        if os.path.exists(self.temp_dir):
            rmtree(self.temp_dir)  
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'psrc', 'urbansim_parcel', 'urbansim', 'opus_core'],
            test_data={
            "person":{ 
                'person_id':   array([1, 2, 3, 4, 5, 6]),
                'household_id':array([1, 1, 2, 3, 3, 5]),
                #hhzone_id    :array([3, 3, 1, 1, 1, 2]),
                'job_id':      array([1, 2, -1, -1, 2, 3]),
                #jobzone_id:   array([1, 2, -1, -1, 2, 3])
                }, 
             "job":{ 
                'job_id': array([1, 2, 3]),
                'zone_id':array([1, 2, 3]),
                },
             "household":{
                'household_id':array([1, 2, 3, 4, 5]),
                'zone_id':     array([3, 1, 1, 1, 2]),
                'income':      array([10000, 45000, 40000, 5000, 0])
                 },
            'travel_data_link':{
                'travel_data_link_id':  array([1]),
                'data_link':  array([self.temp_dir]),
            },
         })
        should_be = array([66.4, 121, 0, 0, 36.6, 108])
        tester.test_is_close_for_family_variable(self, should_be, self.variable_name)

if __name__=='__main__':
    opus_unittest.main()
