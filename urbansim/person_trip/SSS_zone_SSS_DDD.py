# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.logger import logger

class SSS_zone_SSS_DDD(Variable):
    """get SSS [origin | destination] zone attribute SSS_DDD"""

    def __init__(self, target, name1, name2):
        if target.strip().lower() == "origin":
            self.join_attribute = "from_zone_id"
        elif target.strip().lower() == "destination":
            self.join_attribute = "to_zone_id"
        else:
            logger.log_warning("the first wild card is incorrectly specified; should be either 'origin' or 'destination'.")
            logger.log_warning("Default to 'destination'.")
            self.join_attribute = "to_zone_id"
            
        self.var_name = '_'.join(name1, name2)
        Variable.__init__(self)
        
    def dependencies(self):
        return ["zone.zone_id",
                "person_trip.from_zone_id",
                "person_trip.to_zone_id"
                ]

    def compute(self, dataset_pool):
        zones = dataset_pool.get_dataset('zone')
        # in case SSS is a computed variable
        zones.compute_one_variable_with_unknown_package(self.var_name, dataset_pool=dataset_pool)
        
        person_trips = self.get_dataset()
        
        return person_trips.get_join_data(zones, self.var_name, 
                                          join_attribute=self.join_attribute)
