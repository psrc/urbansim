# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import bool8, zeros, bool8, logical_and, where
from opus_core.misc import unique_values

class is_allowed_by_constraint(Variable):
    """whether the proposed development template is viable for a given parcel and its constraints,
    compare if parcel.min_constraint <= development_template.density <=  parcel.min_constraint
    """
    template_opus_path = "urbansim_parcel.development_template"
    
    def dependencies(self):
        return ["generic_land_use_type_id = development_template.disaggregate(land_use_type.generic_land_use_type_id)",
                "development_template.density_type",
                "development_constraint.constraint_type",
                "development_project_proposal.parcel_id",
                "development_project_proposal.template_id",
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
        constraint_types = unique_values(constraints.get_attribute("constraint_type"))
        templates.compute_variables(map(lambda x: "%s.%s" % (self.template_opus_path, x), constraint_types), dataset_pool)
        template_ids = templates.get_id_attribute()
        generic_land_use_type_ids = templates.get_attribute("generic_land_use_type_id")
        proposal_template_ids = proposals.get_attribute("template_id")
        results = zeros(proposals.size(), dtype=bool8)
        unique_templates = unique_values(proposal_template_ids)
        for this_template_id in unique_templates:
            i_template = templates.get_id_index(this_template_id)
            fit_indicator = (proposal_template_ids == this_template_id )
            building_type_id = generic_land_use_type_ids[i_template]
            for constraint_type, constraint in parcels.development_constraints[building_type_id].iteritems():                
                template_attribute = templates.get_attribute(constraint_type)[i_template]  #density converted to constraint variable name           
                min_constraint = constraint[:, 0][parcel_index].copy() 
                max_constraint = constraint[:, 1][parcel_index].copy()
                ## treat -1 as a constant for unconstrainted
                w_unconstr = min_constraint == -1
                if w_unconstr.any():
                    min_constraint[w_unconstr] = template_attribute.min()

                w_unconstr = max_constraint == -1
                if w_unconstr.any():
                    max_constraint[w_unconstr] = template_attribute.max()
                
                fit_indicator = logical_and(fit_indicator,
                                            logical_and(template_attribute >= min_constraint,
                                                        template_attribute <= max_constraint)
                                            )
            results[fit_indicator] = True
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            'development_template':
            {
                'template_id': array([1,2,3,4]),
                "land_use_type_id":array([1, 1, 2, 2]),
                'density_type':   array(['units_per_acre', 'units_per_acre', 'far', 'far']),
#                'constraint_name':array(['units_per_acre', 'units_per_acre', 'far', 'far']),
                'units_per_acre': array([0.2, 2, 0, 0]),
                'far':array([0, 0, 25, 7])
            },
            'land_use_type':
            {
                "land_use_type_id":array([1, 2]),
                "generic_land_use_type_id":array([1, 2]),
#                'density_type':   array(['units_per_acre','far']),

            },
            'development_constraint':
            {
                'constraint_id': array([1,2,3,4]),
                'is_constrained': array([0, 1, 1, 0]),
                'generic_land_use_type_id': array([1, 1, 2, 2]),
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
    
