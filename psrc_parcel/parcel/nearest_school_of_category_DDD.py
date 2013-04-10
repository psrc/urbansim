# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.abstract_variables.abstract_nearest_id_of_SSS_dataset import abstract_nearest_id_of_SSS_dataset

class nearest_school_of_category_DDD(abstract_nearest_id_of_SSS_dataset):
    """id of the nearest school"""

    _return_type = "int32"
    dataset_x_coord = "school.disaggregate(parcel.x_coord_sp)"
    dataset_y_coord = "school.disaggregate(parcel.y_coord_sp)"
    my_x_coord = "x_coord_sp"
    my_y_coord = "y_coord_sp"
    package = "urbansim_parcel"
    from_dataset = "parcel"
    to_dataset = "school"
   
    def __init__(self, category):
        if category < 6:
            self.filter = 'psrc_parcel.school.is_in_category_%s' % category
        else:
            cats = list(str(category))
            self.filter = 'psrc_parcel.school.is_in_category_%s' % cats[0]
            for cat in cats[1:len(cats)]:
                self.filter = '%s + psrc_parcel.school.is_in_category_%s' % (self.filter, cat)
        Variable.__init__(self)
        
from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":  array([1,   2,    3,  4, 5, 6, 7, 8]),
                "x_coord_sp": array([1,   2,    3,  3, 1, 5, 2, 3]),
                "y_coord_sp": array([1,   1,    1,  2, 4, 4, 2, 3]),
            },
            'school':
            {
             "school_id":array([1,2,3,4, 5, 6, 7]),
             "parcel_id":array([1,2,3,7, 7, 1, 8]),
             #"sxcoord":array([1,2,3,2,2,1,3]),
             #"sycoord":array([1,1,1,2,2,1,3]),
             "category": array(['K', 'E', 'EMH', 'M', 'EM', 'E', 'E'])
             },
        })
        should_be = array([6, 2, 3, 3, 5, 7, 5, 7])

        instance_name = 'psrc_parcel.parcel.nearest_school_of_category_2'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        
        instance_name = 'psrc_parcel.parcel.nearest_school_of_category_12'
        should_be = array([1, 2, 3, 3, 5, 7, 5, 7])
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()
