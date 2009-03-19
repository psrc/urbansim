# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from psrc.abstract_variables.abstract_logsum_variable import abstract_logsum_variable
from opus_core.variables.variable import Variable
from numpy import newaxis, concatenate

class max_logsum_hbw_am_from_home_to_work(Variable):
    """max_logsum_hbw_am_from_home_to_work between worker1 & worker2"""
    
    def dependencies(self):
        return [ 
                "psrc_parcel.household_x_building.worker1_logsum_hbw_am_from_home_to_work",
                "psrc_parcel.household_x_building.worker2_logsum_hbw_am_from_home_to_work",
             ]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        data1 = interaction_dataset.get_attribute("worker1_logsum_hbw_am_from_home_to_work")
        data2 = interaction_dataset.get_attribute("worker2_logsum_hbw_am_from_home_to_work")

        return concatenate((data1[...,newaxis], data2[...,newaxis]), axis=2).max(axis=2)