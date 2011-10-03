# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import isnan
from opus_core.variables.variable import Variable
from opus_core.ndimage import mean

class average_school_SSS(Variable):
    """Computes the average of the school measure given by DDD per zone, where missing values are removed 
        from the computation. The measure must be a primary attribute of schools. 
        Missing values are those that are less or equal zero."""
        
    def __init__(self, name):
        self.varname = name
        Variable.__init__(self)
        
    def dependencies(self):
        return ["school.%s" % self.varname, "psrc_parcel.school.zone_id", 
                "_school_faz_measure = zone.disaggregate(psrc_parcel.faz.average_school_%s)" % self.varname]
    
    def compute(self,  dataset_pool):
        ds = self.get_dataset()
        schools = dataset_pool.get_dataset("school")
        values = schools[self.varname]
        valid_idx = values > 0
        result = mean(values[valid_idx], labels=schools[ds.get_id_name()[0]][valid_idx], 
                        index=ds.get_id_attribute())
        is_nan = isnan(result)
        result[is_nan] = ds["_school_faz_measure"]
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
                    "total_score": array([200, 300, 0, 50, -1, 0, 10, 60]),
                    "zone_id": array([1,1,1,2,2,4,3,3]),
                    "faz_id": array([1,1,1,1,1,2,2,2])
                    },
                "zone":{
                     "zone_id":array([1,2,3,4]),
                     "faz_id": array([1,1,2,2])
                 },
                 "faz":{
                    "faz_id" : array([1,2]) 
                    }           
                 
           }
        )
        
        should_be = array([250, 50, 35, 0])

        tester.test_is_equal_for_family_variable(self, should_be, 'psrc_parcel.zone.average_school_total_score')
if __name__=='__main__':
    opus_unittest.main()
