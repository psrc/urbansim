# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from scipy.stats import scoreatpercentile
from numpy import logical_and, zeros

class income_quintiles(Variable):
    """
       Returns 1,2,3,4 or 5 depending on household income.
       Modeled after sanfrancisco.household.in_income_quartile_DDD,
       thanks Bay Area folks!
    """

    def compute(self, dataset_pool):
        # get income attribute
        income = self.get_dataset().get_attribute("income")
        # set up array, same size as households to hold quintile values
        quintiles = zeros(self.get_dataset().n).astype('int')
        # Get quintiles
        perc20 = scoreatpercentile(income,20)
        perc40 = scoreatpercentile(income,40)
        perc60 = scoreatpercentile(income,60)
        perc80 = scoreatpercentile(income,80)
        
        q1 = income<perc20
        q2 = logical_and(income>=perc20,income<perc40)
        q3 = logical_and(income>=perc40,income<perc60)
        q4 = logical_and(income>=perc60,income<perc80)
        q5 = income>=perc80
        
        quintiles[q1] = 1
        quintiles[q2] = 2
        quintiles[q3] = 3
        quintiles[q4] = 4
        quintiles[q5] = 5
        
        return quintiles


from numpy import array
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['mag_zone','urbansim_zone'],
            test_data={
            'household':
            {"household_id":array([1,2,3,4,5,6,7,8,9,10]),
             "income":array      ([1.5,9.4,2.6,5.3,8.8,3.3,4.6,10.4,3.4,6.2]),
             },         
           }
        )
        
        should_be = array([1,5,1,3,4,2,3,5,2,4])
        instance_name = 'mag_zone.household.income_quintiles'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()