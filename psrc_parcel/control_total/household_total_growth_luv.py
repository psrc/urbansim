# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, column_stack


class household_total_growth_luv(Variable):
    """The total growth for the total column between the 5-years LUV totals.
    """
    
    GROWTH_FOR_NO_MATCH = 0.0
    _return_type = "float32"
    target_attribute_name = 'total_number_of_households'
    attr_names = ['city_id']
    geo_name = attr_names[0]
    
    def dependencies(self):
        return ['control_total.year',
                'control_total.%s' % self.target_attribute_name
                ] + ['control_total.' + name for name in self.attr_names]

    def compute(self, dataset_pool):
        ct = self.get_dataset()
        results = zeros(ct.size(), dtype=self._return_type)
        for i in range(ct.size()):
            if ct[self.geo_name][i] <= 0:
                results[i] = self.GROWTH_FOR_NO_MATCH
                continue
            year = ct['year'][i]
            same_attrs = column_stack([ ct[name] == ct[name][i] for name in self.attr_names ]
                                     ).prod(axis=-1).astype('bool')
            curr_val = ct[self.target_attribute_name][(ct['year']==year) * same_attrs]
            next_val = ct[self.target_attribute_name][(ct['year'] == year + 5) * same_attrs]
            
            
            if curr_val.size == 0 or next_val.size == 0:
                results[i] = self.GROWTH_FOR_NO_MATCH
            else:
                results[i] = next_val.sum() - curr_val.sum()
            
        return results
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['opus_core'],
            test_data={ 'control_total': 
                       {
                        'control_total_id':    array([   1,    2,    3,     4,    5,    6,    7,     8,    9]),
                        'year':                array([2014, 2014, 2015,  2015, 2016, 2020, 2020,  2021, 2021]),
                        'city_id':             array([  -1,   -1,    1,     2,   -1,    2,    1,    -1,   -1]),
                'total_number_of_households':  array([  10,   20,    5,     6,   35,   11,    7,    17,   25]),
                        "income":              array([ 100,  200,   -1,    -1,   -1,   -1,   -1,   100,  200]),
                        }
                       }
            )
        defval = household_absolute_growth_luv.GROWTH_FOR_NO_MATCH
        should_be = array([defval, defval, 7-5, 11-6, defval, defval, defval, defval, defval])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
