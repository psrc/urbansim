# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import newaxis, concatenate

class max_network_cost_from_home_to_work(Variable):
    """max_network_cost_from_home_to_work between worker1 & worker2"""
    
    def dependencies(self):
        return [ 
                "psrc_parcel.household_x_building.worker1_network_cost_from_home_to_work",
                "psrc_parcel.household_x_building.worker2_network_cost_from_home_to_work",
             ]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        data1 = interaction_dataset.get_attribute("worker1_network_cost_from_home_to_work")
        data2 = interaction_dataset.get_attribute("worker2_network_cost_from_home_to_work")

        return concatenate((data1[...,newaxis], data2[...,newaxis]), axis=2).max(axis=2)