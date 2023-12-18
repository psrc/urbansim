# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where
from opus_core.datasets.dataset import DatasetSubset

class SSS_control_total_DDD(Variable):
    """City-level control totals for given year.
    """
    
    _return_type = "int32"
    attr_names = ['city_id']
    geo_name = attr_names[0]
    
    def __init__(self, what, year):
        if what != 'household' and what != 'employment':
            raise Exception('Variable must start with either "household" or "employment". It starts with %s' % what)
        self.year = year
        self.what = what
        Variable.__init__(self)    
    
    def dependencies(self):
        if self.what == 'household':
            self.target_attribute_name = 'total_number_of_households'
        else:
            self.target_attribute_name = 'total_number_of_jobs'
        return ['%s_control_total.year' % self.what,
                '%s_control_total.%s' % (self.what, self.target_attribute_name)
                ] + ['%s_control_total.' % self.what + name for name in self.attr_names]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        ct = dataset_pool.get_dataset('%s_control_total' % self.what)
        ct_year_index = where((ct['year']==self.year)*(ct[self.geo_name]>0))[0]
        cty = DatasetSubset(ct, ct_year_index)     
        return ds.aggregate_dataset_over_ids(cty, attribute_name=self.target_attribute_name)

        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.city.household_control_total_2015"
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim','opus_core'],
            test_data={ 'household_control_total': 
                       {
                        #'control_total_id':    array([   1,    2,    3,     4,    5,    6,    7,     8,    9, 10, 11]),
                        'year':                array([2014, 2014, 2015,  2015, 2016, 2020, 2020,  2021, 2021, 2015, 2015]),
                        'city_id':             array([  -1,   -1,    1,     2,   -1,    2,    1,    -1,   -1, 2, 1]),
                'total_number_of_households':  array([  10,   20,    5,     6,   35,   11,    7,    17,   25, 10, 15]),
                        "income":              array([ 100,  200,   -1,    -1,   -1,   -1,   -1,   100,  200, 100, 100]),
                        },
                       'city' :
                       { 'city_id': array([1,2])
                       }
                    }
            )
        should_be = array([20,16])
        tester.test_is_equal_for_family_variable(self, should_be, self.variable_name)

if __name__=='__main__':
    opus_unittest.main()
