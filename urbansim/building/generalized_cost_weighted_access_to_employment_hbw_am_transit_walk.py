# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class generalized_cost_weighted_access_to_employment_hbw_am_transit_walk(Variable):
    """
    """
    _return_type="float32"
    
    def dependencies(self):
        return ["_generalized_cost_weighted_access_to_employment_hbw_am_transit_walk=building.disaggregate(psrc.zone.generalized_cost_weighted_access_to_employment_hbw_am_transit_walk)"]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("_generalized_cost_weighted_access_to_employment_hbw_am_transit_walk")
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
