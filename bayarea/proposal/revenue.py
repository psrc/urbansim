# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
import numpy as np
from numpy import ma, zeros, arange, array
from numpy import float32, column_stack, asscalar

periods_per_year = 4

class revenue(Variable):
    """
    revenue calculation for the new real estate model
    """ 
    _return_type = "float32"
    
    def dependencies(self):
        return ["total_units = proposal_component.disaggregate(proposal.total_units)",
        "affordable_units = proposal_component.total_units * proposal_component.disaggregate(proposal.affordable_ratio)",
                "sales_units = proposal_component.total_units - proposal_component.affordable_units",
                "rentable_sqft = proposal_component.sqft * ( 1 - proposal_component.common_area)",
                "sales_revenue = proposal_component.sales_units * proposal_component.price_per_unit",
                "rent_revenue = proposal_component.affordable_units * proposal_component.rent_per_unit",
                "lease_revenue = proposal_component.rentable_sqft * proposal_component.lease_per_sqft",
                "total_revenue = proposal.aggregate(proposal_component.sales_revenue + proposal_component.rent_revenue + proposal_component.lease_revenue)",
                "revenue_per_period = proposal.total_revenue / %s" % periods_per_year
                ]

    def compute(self, dataset_pool):
        p = self.get_dataset()
        return p['total_revenue']
    
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_visitacion(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            
            'proposal_component':
            {
                "proposal_component_id": array([1,  2,  3,  4]),
                "proposal_id":           array([1,  1,  1,  1]),
           "building_type_id":           array([2,  3,  5,  9]), 
                                           #mf, mf-affordable, retail, cultural
               "sqft":               array([0,  0,  105, 15]) * 1000,
              "price_per_unit":      array([400,0,  0,  0]) * 1000,
          "rent_per_unit":       array([0,  15, 0,  0]) * 1000,
          "lease_per_sqft":      array([0,  0,  21, 0]),
                  "parking_ratio":       array([4/3.0,4/3.0,500,500]),
                  "common_area":         array([.2, .2, .15, .15]),
             },

            'proposal':{
                'proposal_id': array([1]),
                'total_units': array([1250]),
                'affordable_ratio': array([.25]),
            },
            
            }
        )
        
        should_be = array([381369250.00])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-2)
        
if __name__=='__main__':
    opus_unittest.main()
    
