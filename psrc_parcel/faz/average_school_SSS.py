# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import isnan, logical_and
from opus_core.variables.variable import Variable
from opus_core.ndimage import mean

class average_school_SSS(Variable):
    """Computes the average of the school measure given by DDD per faz, where missing values are removed 
        from the computation. The measure must be a primary attribute of schools. 
        Missing values are those that are less or equal zero."""
        
    def __init__(self, name):
        self.varname = name
        Variable.__init__(self)
        
    def dependencies(self):
        return ["school.%s" % self.varname, "psrc_parcel.school.faz_id", 
#                "psrc_parcel.school.school_district_id",
#                "has_%s = school.%s > 0" % (self.varname, self.varname), 
                #"school_district_id = faz.disaggregate(school.school_district_id, intermediates=[parcel])"
                ]
    
    def compute(self,  dataset_pool):
        ds = self.get_dataset()
        schools = dataset_pool.get_dataset("school")
        values = schools[self.varname]
        valid_idx = values > 0
        result = mean(values[valid_idx], labels=schools[ds.get_id_name()[0]][valid_idx], 
                        index=ds.get_id_attribute())
        is_nan = isnan(result)
        result[is_nan] = 0
#        if any(is_nan):
#            result_district = mean(values[valid_idx], labels=schools['school_district_id'][valid_idx], 
#                        index=ds['school_district_id'])
#            not_is_nan_district = logical_and(isnan(result_district) == 0,is_nan)
#            result[not_is_nan_district] = result_district[not_is_nan_district]
        return result
    
from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel','urbansim_parcel','urbansim'],
            test_data={
                "school":{
                    "school_id":array([1, 2, 3, 4, 5, 6, 7, 8]),
                    "school_district_id": array([1,    1,  1,  2,  2, 3, 4,   4]),
                    "total_score":        array([1,    2,  0,  3, -1, 0, 1.5, 4.5]),
                    "faz_id":             array([1,    1,  1,  2,  5, 4,  3,  3])
                    },
                "faz":{
                     "faz_id":array([1,2,3,4,5]),
                     "school_district_id": array([1,2,4,3,2])
                 }             
                 
           }
        )
        
        #should_be = array([1.5, 3, 3, 0, 3])
        should_be = array([1.5, 3, 3, 0, 0])

        tester.test_is_equal_for_family_variable(self, should_be, 'psrc_parcel.faz.average_school_total_score')
if __name__=='__main__':
    opus_unittest.main()
