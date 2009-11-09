# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from opus_core.logger import logger

class customized_filter(Variable):
    """return True or False for a customized set of filter"""
    
    _return_type="float32"

    def dependencies(self):
        return ["psrc.household.county_id",
                "household.in_control",
                "psrc.household.is_worker1_work_place_in_county_033_if_has_the_worker",
                "psrc.household.is_worker2_work_place_in_county_033_if_has_the_worker",
                ]

    def compute(self, dataset_pool):
        hhs = self.get_dataset()
        indicator=(hhs.get_attribute("county_id") == 33) * \
                  (hhs.get_attribute("in_control") == 1) * \
                   hhs.get_attribute("is_worker1_work_place_in_county_033_if_has_the_worker") *\
                   hhs.get_attribute("is_worker2_work_place_in_county_033_if_has_the_worker")
#                   hhs.get_attribute("is_worker1_work_place_in_county_033") *\
#                   hhs.get_attribute("is_worker2_work_place_in_county_033")
        return indicator


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
from psrc.datasets.person_dataset import PersonDataset

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc.household.customized_filter"

    def test_my_inputs(self):
        
        values = VariableTestToolbox().compute_variable(self.variable_name, \
            {
              "household":{ 
                                "household_id":array([1,      2,      3,      4,      5,      6]),
                                "county_id":   array([33,     31,     33,     31,     33,     33]),
                                "in_control":  array([0,      0,      1,      1,      1,      1]),
                                "is_worker1_work_place_in_county_033_if_has_the_worker":     \
                                               array([1,      1,      1,      1,      1,      0]),
                                "is_worker2_work_place_in_county_033_if_has_the_worker":     \
                                               array([1,      0,      1,      1,      1,      0]),
                               }},
              dataset = "household" )
        should_be = array([0, 0, 1, 0, 1, 0])
        
        self.assertEqual(ma.allclose(values, should_be, rtol=1e-7), \
                         True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()