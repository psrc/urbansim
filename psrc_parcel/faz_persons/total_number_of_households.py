# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, logical_and

class total_number_of_households(Variable):
    """
    """
            
    def dependencies(self):
        return ["urbansim_parcel.household.dummy_id",
                "_total_number_of_households = faz_persons.number_of_agents(household)", 
               ]

    def compute(self,  dataset_pool):
        faz_sectors = self.get_dataset()
        return faz_sectors.get_attribute("_total_number_of_households")
