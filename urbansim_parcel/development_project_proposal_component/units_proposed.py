# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numpy import logical_and

class units_proposed(Variable):
    _return_type = "float32"

    def dependencies(self):
        return [
                "_units_proposed_in_proposal = development_project_proposal_component.disaggregate(urbansim_parcel.development_project_proposal.units_proposed)",
                "_is_far_unit = development_project_proposal_component.disaggregate(urbansim_parcel.development_template.is_far)",
                 my_attribute_label("percent_building_sqft"),
                 my_attribute_label("building_sqft_per_unit"),
                 my_attribute_label("is_residential")
                ]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        amount = ds.get_attribute("_units_proposed_in_proposal")/100.0 * ds.get_attribute("percent_building_sqft")
        is_res_and_far = logical_and(ds.get_attribute("is_residential"), ds.get_attribute("_is_far_unit"))
        # transform units for residential components into residential_units
        amount[is_res_and_far] = amount[is_res_and_far] / \
                            ds.get_attribute("building_sqft_per_unit")[is_res_and_far].astype("float32")
        return amount

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0 and x <= 100 ", values)

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'development_project_proposal':
            {
                "proposal_id":    array([1,  2,    3,  4, 5]),
                "units_proposed": array([34, 250, 130, 0, 52])
            },
            'development_project_proposal_component':
            {
                "proposal_component_id": arange(8)+1,
                 "proposal_id":           array([3,   3, 5,  2,   5,   1, 3, 1]),
                 "percent_building_sqft": array([30, 25, 1, 100, 99, 100, 45, 0]),
                 "template_id":           array([4,   2, 1,  3,   2,   2,  4, 1]),
                 "is_residential":        array([True,False, True, True,False,True,False, True]),
                 "building_sqft_per_unit": array([3.5, 1, 20, 0, 1, 0.1, 10, 50])
             },
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'density_type': array(['units_per_acre', 'far', 'units_per_acre', 'far']),
            },
        })
        should_be = array([130/100.0*30/3.5, 130/100.0*25,  52/100.0,  250, 52/100.0 * 99, 34/0.1, 130/100.0*45, 0])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
