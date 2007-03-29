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
from numpy import bool8, zeros, bool8, logical_and, where

class is_allowed_by_constraint(Variable):
    """whether the proposed development template is viable for a given parcel and its constraints,
    compare if parcel.min_constraint <= development_template.density <=  parcel.min_constraint
    """
    template_opus_path = "psrc_parcel.development_template"
    
    def dependencies(self):
        return ["desnity_name=development_template.disaggregate(building_type.density_name)",
                "constraint_name=development_template.disaggregate(building_type.constraint_name)",
                "development_constraint.building_type_id",
                "parcel.parcel_id",
                 ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        templates = dataset_pool.get_dataset("development_template")
        building_types = dataset_pool.get_dataset("building_type")
        parcels = dataset_pool.get_dataset("parcel")
        constraints = dataset_pool.get_dataset("development_constraint")        
        parcels.get_development_constraints(constraints, dataset_pool)
        #for name in templates.get_attribute("density_name"):  # or "constraint_name", unit_per_acre or FAR, these two should be the same or comparable
            
        #template_index = templates.get_id_index(proposals.get_attribute("template_id"))
        parcel_index = parcels.get_id_index(proposals.get_attribute("parcel_id"))

        results = zeros(proposals.size(), type=bool8)
        for i_template in range(templates.size()):
            this_template_id = templates.get_attribute("template_id")[i_template]
            building_type_id = templates.get_attribute("building_type_id")[i_template]
            constraint_name = templates.get_attribute("constraint_name")[i_template]
            #assert constraint_name == templates.get_attribute("density_name_name")[i_template]
            templates.compute_variables("%s.%s" % (self.template_opus_path, constraint_name), dataset_pool)
            template_density = templates.get_attribute(constraint_name)[i_template]  #density converted to constraint variable name
            
            #get the constraint for each parcel for given building_type_id
            min_constraint = parcels.development_constraints[building_type_id][:, 0][parcel_index] 
            max_constraint = parcels.development_constraints[building_type_id][:, 1][parcel_index]

            indicator = (template_density >= min_constraint) * \
                          (template_density <= max_constraint) * \
                          (proposals.get_attribute("template_id")==this_template_id)
            results[where(indicator)] = True
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    
from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel','urbansim'],
            test_data={
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                "building_type_id":array([1, 1, 2, 2]),
                'density_name':   array(['units_per_acre', 'units_per_acre', 'far', 'far']),
                'constraint_name':array(['units_per_acre', 'units_per_acre', 'far', 'far']),
                'units_per_acre': array([0.2, 2, 0, 0]),
                'far':array([0, 0, 25, 7])
            },
            'building_type':
            {
                "building_type_id":array([1, 2]),
                'density_name':   array(['units_per_acre','far']),
                'constraint_name':array(['units_per_acre','far']),
            },
            'development_constraint':
            {
                'constraint_id': array([1,2,3,4]),
                'is_constrained': array([0, 1, 1, 0]),
                'building_type_id': array([1, 1, 2, 2]),
                'min_constraint': array([0,  0,   0,  0]),
                'max_constraint': array([3, 0.2, 10, 100]),                
            },
            'parcel':
            {
                "parcel_id":        array([1,   2,    3]),
                "is_constrained":   array([1,   0,    1]),
            },
            'development_project_proposal':
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4])
            }
            }
        )
        
        should_be = array([1, 0,  0, 1,  
                             1, 1, 1, 
                             1, 0, 0, 1])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    