# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk(Variable):
    """
    """
    _return_type="float32"
    
    def dependencies(self):
        return ["_ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk=building.disaggregate(psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk)"]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("_ln_employment_within_30_minutes_travel_time_hbw_am_transit_walk")
        
    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
