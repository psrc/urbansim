# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import ones, zeros, column_stack, logical_and, all
from opus_core.misc import ndsum

class number_of_workers(Variable):
    """"""
    
    def dependencies(self):
        return ["zone_id=person.work_zone",
                "workers=zone.number_of_agents(person)"
                ]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        results = ds['workers']
        #dataset_pool.get_dataset('person').delete_one_attribute('zone_id')
        return results
