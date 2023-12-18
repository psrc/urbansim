# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label

class occupied_sqft_of_typeclass_SSS(Variable):
    """For a given building, how many sqft is occupied?  Includes business and
       residential.
       Calculated as business-occupied-sqft + (household-occupied-units/total-units) x household-sqft
    """

    _return_type="float32"
    def __init__(self, typeclass):
        self.typeclass = typeclass.lower()
        Variable.__init__(self)
    
    def dependencies(self):
        return ["_occupied_sqft_of_typeclass_%s = where(sanfrancisco.building.building_typeclass_name=='%s'," \
                 "building.aggregate(business.sqft) + numpy.minimum(1.0,safe_array_divide(sanfrancisco.building.number_of_households,building.residential_units))*building.residential_sqft" \
                 ",0)" % (self.typeclass, self.typeclass)]
#        return ["_occupied_sqft_of_typeclass_%s = where(sanfrancisco.building.building_typeclass_name=='%s',"\
#                "numpy.minimum(1.0,safe_array_divide(sanfrancisco.building.number_of_households,building.residential_units)),0)" % (self.typeclass, self.typeclass)]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_occupied_sqft_of_typeclass_%s" % self.typeclass)

    def post_check(self,  values, dataset_pool=None):
        building_sqft = self.get_dataset().get_attribute("building_sqft")
        self.do_check("x >= 0 and x <= " + str(building_sqft), values)
        
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array, alltrue
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['sanfrancisco','urbansim'],
            test_data={
                "building_type_classification":{
                    "class_id":array([1,2,3]),
                    "name":array(['apartment','industrial','mixed']),
                    },
                "building_type":{
                    "building_type_id":array([1,2,3,4,5,6]),
                    "class_id":array([1,1,2,2,3,3])
                    },
                 "building":{
                     "building_id":array([11,12, 13,14, 15,16,
                                          21,22, 23,24, 25,26,
                                          31,32, 33,34, 35,36]),
                     "building_type_id":array([1,2, 3,4, 5,6,
                                               6,5, 4,3, 2,1,
                                               1,2, 3,4, 5,6]),
                      # so type_class is: 1,1,2,2,3,3, = a,a,i,i,m,m
                      #                   3,3,2,2,1,1  = m,m,i,i,a,a
                      #                   1,1,2,2,3,3  = a,a,i,i,m,m
                     "building_sqft":array([101,102, 103,104, 105,106,
                                            201,202, 203,204, 205,206,
                                            301,302, 303,304, 305,306]),
                     "residential_sqft":array([101,102, 0,0,  51, 52,
                                               101,102, 0,0, 205,206,
                                               301,302, 0,0, 101,102]),
                     "non_residential_sqft":array([  0,  0, 103,104,  54, 54,
                                                   100,100, 203,204,   0,  0,
                                                     0,  0, 303,304, 204,204]),
                     "residential_units":array([4,4, 0,0, 2,2,
                                                1,1, 0,0, 3,3,
                                                2,2, 0,0, 1,1])
                 },
                 "business":{
                      "business_id":array([ 1,2,   3, 4,  5, 6,
                                            7,8,   9,10, 11,12,
                                           13,14, 15]),
                      "building_id":array([13,13, 14,14, 15,16,
                                           21,22, 23,23, 24,24,
                                           33,34, 35]),
                      "sqft":       array([23,24, 25,26, 54,55,
                                           27,28, 29,30, 31,32,
                                           33,34, 35])
                      
                 },
                 "household":{
                      "household_id":array([1,2,3,4,5,6,
                                            7,8,9,
                                            10,11,12,13,
                                            14,    # in industrial
                                            15]),  # too many in blg 35
                      "building_id":array([11,11,11,12,12, 15,
                                           21, 26,26,
                                           31,31,32, 35,
                                           13,
                                           35]),
                 }
           }
        )
        
        varname = "sanfrancisco.building.occupied_sqft_of_typeclass_apartment"
        print(tester._get_attribute(given_variable_name=varname))
        # [ (3/4)*101, (2/4)*102, 0,0, 0,0,
        #   0,0,                  0,0, (0/3)*205, (2/3)*206,
        #   (2/2)*301, (1/2)*302, 0,0, 0,0 ]
        expected = [75.75, 51, 0, 0, 0,   0, 
                    0,  0, 0, 0, 0, 137.333,
                    301, 151,0, 0, 0, 0 ]
        tester.test_is_close_for_family_variable(self, expected, varname, 0.001)

        varname = "sanfrancisco.building.occupied_sqft_of_typeclass_industrial"
        print(tester._get_attribute(given_variable_name=varname))
        # [ 0,0, 23+24, 25+26, 0,0,
        #   0,0, 29+30, 31+32, 0,0,
        #   0,0, 33,    34,    0,0]
        expected = [0,0, 47,51, 0,0,
                    0,0, 59,63, 0,0,
                    0,0, 33,34, 0,0]
        tester.test_is_close_for_family_variable(self, expected, varname, 0.001)

        varname = "sanfrancisco.building.occupied_sqft_of_typeclass_mixed"
        print(tester._get_attribute(given_variable_name=varname))
        # [ 0,0, 0,0, 54+(1/2)*51, 55+(0/2)*52,
        #   27+(1/1)*101, 28+(0/1)*102, 0,0, 0,0,
        #   0,0, 0,0, 35+(2/1)*101, 0+(0/1)*102]
        expected = [0,0, 0,0, 79.5, 55,
                    128, 28, 0,0, 0,0,
                    0,0, 0,0, 136, 0]
        tester.test_is_close_for_family_variable(self, expected, varname, 0.001)

if __name__=='__main__':
    opus_unittest.main()
