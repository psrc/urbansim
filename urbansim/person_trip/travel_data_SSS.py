# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class travel_data_SSS(Variable):
    """get travel data primary attribute SSS"""

    def __init__(self, name):
        self.var_name = name
        Variable.__init__(self)
        
    def dependencies(self):
        return ["travel_data." + self.var_name,
                "person_trip.from_zone_id",
                "person_trip.to_zone_id"
                ]

    def compute(self, dataset_pool):
        travel_data = dataset_pool.get_dataset('travel_data')
        var_matrix = travel_data.get_attribute_as_matrix(self.var_name)
        
        person_trips = self.get_dataset()
        
        return var_matrix[person_trips.get_attribute('from_zone_id'), 
                          person_trips.get_attribute('to_zone_id')]
