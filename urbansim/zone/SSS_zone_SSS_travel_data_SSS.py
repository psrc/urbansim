# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.logger import logger

class SSS_zone_SSS_travel_data_SSS(Variable):
    """by SSS [origin | destination] zone do function SSS [sum | mean] for travel_data attribute SSS"""

    def __init__(self, target, function, name):
        if target.strip().lower() == "origin":
            self.join_attribute = "from_zone_id"
        elif target.strip().lower() == "destination":
            self.join_attribute = "to_zone_id"
        else:
            logger.log_warning("the first wild card is incorrectly specified; should be either 'origin' or 'destination'.")
            logger.log_warning("Default to 'destination'.")
            self.join_attribute = "to_zone_id"
            
        self.function = function
        
        self.var_name = name
        Variable.__init__(self)
        
    def dependencies(self):
        return ["zone.zone_id",
                "travel_data." + self.var_name,
                "zone_id=travel_data." + self.join_attribute
                ]

    def compute(self, dataset_pool):
        travel_data = dataset_pool.get_dataset('travel_data')
        
        zones = self.get_dataset()
        results = zones.aggregate_dataset_over_ids(travel_data, function=self.function, attribute_name=self.var_name)
        
        return results