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
from numarray import Bool, zeros, Bool, logical_and, where

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

        results = zeros(proposals.size(), type=Bool)
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
from numarray import array
import numarray.strings as strarray
from numarray.ma import allequal

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.development_project_proposal.is_allowed_by_constraint"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage._write_dataset(
            'development_templates',
            {
                'template_id': array([1,2,3,4]),
                "building_type_id":array([1, 1, 2, 2]),
                'density_name':   strarray.array(['units_per_acre', 'units_per_acre', 'far', 'far']),
                'constraint_name':strarray.array(['units_per_acre', 'units_per_acre', 'far', 'far']),
                'units_per_acre': array([0.2, 2, 0, 0]),
                'far':array([0, 0, 25, 7])
            }
        )
        storage._write_dataset(
            'building_types',
            {
                "building_type_id":array([1, 2]),
                'density_name':   strarray.array(['units_per_acre','far']),
                'constraint_name':strarray.array(['units_per_acre','far']),
            }
        )
        
        storage._write_dataset(
            'development_constraints',
            {
                'constraint_id': array([1,2,3,4]),
                'is_constrained': array([0, 1, 1, 0]),
                'building_type_id': array([1, 1, 2, 2]),
                'min_constraint': array([0,  0,   0,  0]),
                'max_constraint': array([3, 0.2, 10, 100]),                
            }
        )
        storage._write_dataset(
            'parcels',
            {
                "parcel_id":        array([1,   2,    3]),
                "is_constrained":   array([1,   0,    1]),
            }
        )
        storage._write_dataset(
            'development_project_proposals',
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['psrc_parcel','urbansim'],
                                   storage=storage)

        proposals = dataset_pool.get_dataset('development_project_proposal')
        proposals.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = proposals.get_attribute(self.variable_name)
        
        should_be = array([1, 0,  0, 1,  
                             1, 1, 1, 
                             1, 0, 0, 1])
        
        self.assert_(allequal( values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()