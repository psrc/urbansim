# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import ma, maximum, zeros, column_stack
from opus_core.simulation_state import SimulationState


class abstract_growth_rate(Variable):
    """The rate of growth for the total column (SSS) between the year before current year and current year
    e.g. mag_zone.control_total.population_growth_rate (the control totals table must have population column) 
    """
    
    GROWTH_RATE_FOR_NO_MATCH = 1.0
    #attr_names = ['subarea_id']
    #target_attribute_name = 'total_number_of_households'
    _return_type = "float32"
    target_attribute_name = 'population'
    attr_names = ['subarea_id', 'male']
    
    def dependencies(self):
        return ['control_total.year',
                'control_total.%s' % self.target_attribute_name
                ] + ['control_total.' + name for name in self.attr_names]

    def compute(self, dataset_pool):
        ct = self.get_dataset()
        results = zeros(ct.size(), dtype=self._return_type)
        for i in range(ct.size()):
            year = ct['year'][i]
            same_attrs = column_stack([ ct[name] == ct[name][i] for name in self.attr_names ]
                                     ).prod(axis=-1).astype('bool')
            
            curr_val = ct[self.target_attribute_name][(ct['year']==year) * same_attrs]
            prev_val = ct[self.target_attribute_name][(ct['year'] == year - 1) * same_attrs]
            
            if prev_val.size == 0:
                results[i] = self.GROWTH_RATE_FOR_NO_MATCH
            else:
                results[i] = ( curr_val.sum() - prev_val.sum()) / float(prev_val.sum()) 
            
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
                        'year':                array([2000, 2000, 2000,  2000, 2001, 2001, 2001,  2001, 2001]),
                        'subarea_id':          array([   1,    1,    2,     2,    1,    1,    2,     2,    3]),
                        'male':                array([   0,    1,    0,     1,    0,    1,    1,     0,   -1]),
                        'sampling_threshold':  array([   '',  '',    '','1==1',   '',  '',   '',    '',    '']),
                        'population':          array([  48,   49,    58,   54,   44,   49,   62,    58,    1]),
                        }
                       }
            )
        defval = abstract_growth_rate.GROWTH_RATE_FOR_NO_MATCH
        should_be = array([defval, defval, defval, defval,
                           (44-48)/48.0, (49-49)/49.0, (62-54)/54.0, (58-58)/58.0, defval])
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
