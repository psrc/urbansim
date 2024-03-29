# Opus/UrbanSim urban simulation software./Applications/opus/src/urbansim/zone/number_of_jobs_of_sector_DDD.py
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_access_within_threshold_variable import abstract_access_within_threshold_variable

class SSS_within_DDD_SSS_threshold(abstract_access_within_threshold_variable):
    """sum zone attribute SSS (e.g. number of jobs) within DDD minutes SSS (primary attribute of travel_data, e.g. travel time by mode),
    e.g. urbansim_zone.zone.number_of_jobs_within_30_hbw_am_drive_alone_threshold
    """
    
    _return_type = "int32"
    function = "sum"

    def __init__(self, zone_attribute, number, mode):
        self.zone_attribute_to_access =  "urbansim_zone.zone.%s" % zone_attribute
        self.threshold = number
        self.travel_data_attribute  = "travel_data.%s" % mode
        abstract_access_within_threshold_variable.__init__(self)

## abstract variable tested elsewhere
from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester
class Tests(opus_unittest.OpusTestCase):
    def do(self, ddd, sss, should_be):
        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                 "zone":{
                    "zone_id":array([1,3]),
                    "employment":array([10, 1])},
                 "travel_data":{
                     "from_zone_id":array([3,3,1,1,4]),
                     "to_zone_id":array([1,3,1,3,4]),
                     sss:array([1.1, 2.2, 3.3, 4.4,99])}
            }
        )
        instance_name = "urbansim_zone.zone.employment_within_%s_%s_threshold" % (ddd, sss) 
        tester.test_is_close_for_family_variable(self, should_be, instance_name)

    def test_to_2(self):
        should_be = array([0, 10])
        self.do(2, 'hwy', should_be)

    def test_to_4(self):
        should_be = array([10, 11])
        self.do(4, 'bart', should_be)

if __name__=='__main__':
    opus_unittest.main()