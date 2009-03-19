# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, round_

class units_proposed(Variable):
    """total units proposed (residential units, and/or non residential sqft) for the proposed developmentt project,
    depending on whether the proposed projects will be prorated or not, part or all of the
    units will be available
    """
    _return_type = "int32"

    def dependencies(self):
        return [
                "urbansim_parcel.development_project_proposal.land_area_taken",
                "density = development_project_proposal.disaggregate(urbansim_parcel.development_template.density)",
                "density_convertor = development_project_proposal.disaggregate(urbansim_parcel.development_template.density_converter)",  # land area is in sqft
                "usable_ratio = (1- development_project_proposal.disaggregate(development_template.percent_land_overhead) / 100.0).astype(float32)",
                 ]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return round_(ds.get_attribute("land_area_taken") * ds.get_attribute("usable_ratio") * 
                            ds.get_attribute("density") * ds.get_attribute("density_convertor"))

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from numpy import array, int32
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    ACRE = 43560
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'building_type_id': array([1, 1, 2, 3]),
                "density_type":  array(['units_per_acre', 'units_per_acre', 'far',  'units_per_acre']),                
                'density':array([0.6, 2.0, 10, 5]),
                'percent_land_overhead':array([0, 10, 0, 20]),
                'land_sqft_min': array([0, 10, 4, 30],dtype=int32) * self.ACRE,
                'land_sqft_max': array([2, 20, 8, 100],dtype=int32) * self.ACRE
            },
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "vacant_land_area": array([1, 50,  200],dtype=int32)* self.ACRE,
            },
            'development_project_proposal':
            {
                "proposal_id":array([1,  2,  3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3,  3 ]),
                "template_id":array([1,  2,  3,  4, 2,  3, 4, 1, 2, 3,  4])
            }
        })
        should_be = array([1, 0,  0,            0,
                              36, 80*self.ACRE, 200,  
                           1, 36, 80*self.ACRE, 400]) 

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
