# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from urbansim.abstract_variables.abstract_nearest_id_of_SSS_dataset import abstract_nearest_id_of_SSS_dataset

class nearest_public_school_of_category_DDD_with_enrollment(abstract_nearest_id_of_SSS_dataset):
    """id of the nearest school. Filter out schools with zero enrollment."""

    _return_type = "int32"
    dataset_x_coord = "school.disaggregate(parcel.x_coord_sp)"
    dataset_y_coord = "school.disaggregate(parcel.y_coord_sp)"
    my_x_coord = "x_coord_sp"
    my_y_coord = "y_coord_sp"
    package = "urbansim_parcel"
    from_dataset = "parcel"
    to_dataset = "school"
    enrollment_attribute = "student_count2014"
   
    def __init__(self, category):
        if category < 6:
            self.filter = '(school.public == 1) * (school.%s > 0) * psrc_parcel.school.is_in_category_%s' % (
                self.enrollment_attribute, category)
        else:
            cats = list(str(category))
            self.filter = 'psrc_parcel.school.is_in_category_%s' % cats[0]
            for cat in cats[1:len(cats)]:
                self.filter = '%s + psrc_parcel.school.is_in_category_%s' % (self.filter, cat)
            self.filter = "(school.public == 1) * (school.%s > 0) * (%s)" % (self.enrollment_attribute, self.filter)
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
             "category": array(['K', 'E', 'EMH', 'M', 'EM', 'E', 'E']),
             "public":  array([1, 1, 0, 1, 1, 0, 1]), 
             "student_count2014": array([0, 10, 20, 10, 10, 10, 0]), 
             
             },
        })
        should_be = array([2, 2, 2, 5, 5, 5, 5, 5])

        instance_name = 'psrc_parcel.parcel.nearest_public_school_of_category_2_with_enrollment'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)
        
        instance_name = 'psrc_parcel.parcel.nearest_public_school_of_category_12_with_enrollment'
        should_be = array([2, 2, 2, 5, 5, 5, 5, 5])
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()
