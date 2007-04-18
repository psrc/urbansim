#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.variables.variable import Variable
#from variable_functions import my_attribute_label
from numpy import where

class units_proposed(Variable):
    """total units proposed (residential units, and/or non residential sqft) for the proposed developmentt project,
    depending on whether the proposed projects will be prorated or not, part or all of the
    units will be available
    """
    _return_type = "int32"

    def dependencies(self):
        return ["vacant_land_area = development_project_proposal.disaggregate(psrc_parcel.parcel.vacant_land_area)",
                "land_area_min = development_project_proposal.disaggregate(development_template.land_area_min)",
                "land_area_max = development_project_proposal.disaggregate(development_template.land_area_max)",
                "density = development_project_proposal.disaggregate(psrc_parcel.development_template.density)",
                "density_convertor = development_template.disaggregate(building_type.density_convertor)",
                "density_convertor = development_project_proposal.disaggregate(development_template.density_convertor)",
                "usable_ratio = 1- development_project_proposal.disaggregate(development_template.percent_land_overhead) / 100.0",
                "possible_units = development_project_proposal.vacant_land_area * development_project_proposal.usable_ratio * development_project_proposal.density / development_project_proposal.density_convertor",
                "min_units = development_project_proposal.land_area_min * development_project_proposal.usable_ratio * development_project_proposal.density / development_project_proposal.density_convertor",
                "max_units = development_project_proposal.land_area_max * development_project_proposal.usable_ratio * development_project_proposal.density / development_project_proposal.density_convertor",
                 ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        templates = dataset_pool.get_dataset("development_template")
        #template_index = templates.get_id_index(proposals.get_attribute("template_id"))
        #density = zeros(templates.size(), dtype=Float)

        #for density_name in unique_values(templates.get_attribute("density_name")):
            #templates.compute_variables("%s.%s" % density_name)
            #itemplates_using_this_density_name = where(template.get_attribute("density_name")==density_name)[0]
            #density[itemplates_using_this_density_name]=templates.get_attribute(density_name)[itemplates_using_this_density_name]

        #proposal_density = density[template_index]
        #possbile_units = proposals.get_attribute("vacant_land_area") * proposal_density
        possible_units = proposals.get_attribute("possible_units")

        min_units = proposals.get_attribute("min_units")
        max_units = proposals.get_attribute("max_units")
        results = possible_units
        w_max = where(results>max_units)
        w_min = where(results<min_units)
        results[w_max] = max_units[w_max]
        results[w_min] = 0 #min_units[w_min], there should not be any such cases; filter takes care of them

        return results

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
            package_order=['psrc_parcel', 'urbansim'],
            test_data={
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                'building_type_id': array([1, 1, 2, 3]),
                'density':array([0.6, 2, 10, 5]),
                'percent_land_overhead':array([0, 10, 0, 20]),
                'land_area_min': array([0, 10, 4, 30],dtype=int32) * self.ACRE,
                'land_area_max': array([2, 20, 8, 100],dtype=int32) * self.ACRE
            },
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "vacant_land_area": array([1, 50,  200],dtype=int32)* self.ACRE,
            },
            'building_type':
            {
                "building_type_id":array([1,  2, 3]),
                "density_name":  array(['units_per_acre',  'far',  'units_per_acre']),
                "density_convertor": array([self.ACRE, 1, self.ACRE])
            },
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4])
            }
        })
        should_be = array([0, 0,  0, 0,
                              36, 80*self.ACRE, 200,
                           1, 36, 80*self.ACRE, 400])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
