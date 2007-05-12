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
        return ["generic_building_type_id = development_template.disaggregate(building_type.generic_building_type_id)",
                "development_template.density_type",
                "development_constraint.constraint_type",
                "parcel.parcel_id",
                 ]

    def compute(self, dataset_pool):
        proposals = self.get_dataset()
        templates = dataset_pool.get_dataset("development_template")
        parcels = dataset_pool.get_dataset("parcel")
        constraints = dataset_pool.get_dataset("development_constraint")        
        try:
            index1 = proposals.index1
        except:
            index1 = None
        parcels.get_development_constraints(constraints, dataset_pool, 
                                            index= index1)

        parcel_index = parcels.get_id_index(proposals.get_attribute("parcel_id"))
        # transform parcel_index to be relative to index of parcels.development_constraints
        i_sort = parcels.development_constraints['index'].argsort()
        #i_sort_sort = i_sort.argsort()
        parcel_index = parcels.development_constraints['index'][i_sort].searchsorted(parcel_index)
        results = zeros(proposals.size(), dtype=bool8)
        for i_template in range(templates.size()):
            this_template_id = templates.get_attribute("template_id")[i_template]
            building_type_id = templates.get_attribute("generic_building_type_id")[i_template]

            fit_indicator = ( proposals.get_attribute("template_id")==this_template_id )
            for constraint_type, constraints in parcels.development_constraints[building_type_id].iteritems():
                templates.compute_variables("%s.%s" % (self.template_opus_path, constraint_type), dataset_pool)
                template_attribute = templates.get_attribute(constraint_type)[i_template]  #density converted to constraint variable name
            
                #get the constraint for each parcel for given building_type_id
                min_constraint = constraints[:, 0][parcel_index] 
                max_constraint = constraints[:, 1][parcel_index]
                
                fit_indicator = logical_and(fit_indicator,
                                            logical_and(template_attribute >= min_constraint,
                                                        template_attribute <= max_constraint)
                                            )
            results[where(fit_indicator)] = True
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
                'density_type':   array(['units_per_acre', 'units_per_acre', 'far', 'far']),
#                'constraint_name':array(['units_per_acre', 'units_per_acre', 'far', 'far']),
                'units_per_acre': array([0.2, 2, 0, 0]),
                'far':array([0, 0, 25, 7])
            },
            'building_type':
            {
                "building_type_id":array([1, 2]),
                "generic_building_type_id":array([1, 2]),
#                'density_type':   array(['units_per_acre','far']),

            },
            'development_constraint':
            {
                'constraint_id': array([1,2,3,4]),
                'is_constrained': array([0, 1, 1, 0]),
                'generic_building_type_id': array([1, 1, 2, 2]),
                'constraint_type':array(['units_per_acre','units_per_acre', 'far', 'far']),                
                'minimum': array([0,  0,   0,  0]),
                'maximum': array([3, 0.2, 10, 100]),                
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
    