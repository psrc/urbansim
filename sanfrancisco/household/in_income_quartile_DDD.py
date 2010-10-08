# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
import scipy.stats
from numpy import where,logical_and

class in_income_quartile_DDD(Variable):
    """1 if a household in in the given income quartile, 0 otherwise.  
       Quartile should be 1,2,3, or 4.
    """

    def __init__(self, quartile):
        self.quartile = quartile
        Variable.__init__(self)
        
    # def dependencies(self):
    #    return ["_has_%s_workers = household.nfulltime==%s" % (self.nworkers, self.nworkers)
    #            ]
            
    def compute(self,  dataset_pool):
        income = self.get_dataset().get_attribute("income")
        if self.quartile==1:
            perc25 = scipy.stats.scoreatpercentile(income,25)
            return where(income<perc25,1,0)
        elif self.quartile==2:
            perc25 = scipy.stats.scoreatpercentile(income,25)
            perc50 = scipy.stats.scoreatpercentile(income,50)
            return where(logical_and(income>=perc25,income<perc50),1,0)
        elif self.quartile==3:
            perc50 = scipy.stats.scoreatpercentile(income,50)
            perc75 = scipy.stats.scoreatpercentile(income,75)            
            return where(logical_and(income>=perc50,income<perc75),1,0)
        else:
            perc75 = scipy.stats.scoreatpercentile(income,75)
            return where(income>=perc75,1,0)

from numpy import array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
            'household':
            {"household_id":array([1,2,3,4,5,6,7,8,9]),
             "income":array      ([1.5,9.4,2.6,5.3,8.8,3.3,4.6,10.4,3.4]),
             },         
           }
        )
        
        should_be = array([1,0,1,0,0,0,0,0,0])
        instance_name = 'sanfrancisco.household.in_income_quartile_1'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

        should_be = array([0,0,0,0,0,1,0,0,1])
        instance_name = 'sanfrancisco.household.in_income_quartile_2'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

        should_be = array([0,0,0,1,0,0,1,0,0])
        instance_name = 'sanfrancisco.household.in_income_quartile_3'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

        should_be = array([0,1,0,0,1,0,0,1,0])
        instance_name = 'sanfrancisco.household.in_income_quartile_4'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()