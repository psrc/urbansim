# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import isnan
from opus_core.variables.variable import Variable
from opus_core.ndimage import mean

class average_school_district_SSS(Variable):
    """Computes the average of the school measure given by SSS per school district disaggregated to parcels, 
        where missing values are removed from the computation. The measure must be a primary attribute of schools. 
        Missing values are those that are less or equal zero."""
        
    def __init__(self, name):
        self.varname = name
        Variable.__init__(self)
        
    def dependencies(self):
        return ["school.%s" % self.varname, "school.school_district_id", "parcel.school_district_id"]
    
    def compute(self,  dataset_pool):
        ds = self.get_dataset()
        schools = dataset_pool.get_dataset("school")
        values = schools[self.varname]
        valid_idx = values > 0
        pcl_school_district = ds['school_district_id']
        result = mean(values[valid_idx], labels=schools["school_district_id"][valid_idx], index=pcl_school_district)
        is_nan = isnan(result)
        result[is_nan] = 0
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
                    "total_score":        array([1,    2,  0,  3, -1, 0, 1.5, 5.5])
                    },
                "parcel":{
                     "parcel_id":          array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                     "school_district_id": array([1, 1, 1, 2, 2, 4, 2, 4, 3, 3])
                 }             
                 
           }
        )
        
        #should_be = array([1.5, 3, 3, 0, 3])
        should_be = array([1.5, 1.5, 1.5, 3, 3, 3.5, 3, 3.5, 0, 0])

        tester.test_is_equal_for_family_variable(self, should_be, 'psrc_parcel.parcel.average_school_district_total_score')
if __name__=='__main__':
    opus_unittest.main()
