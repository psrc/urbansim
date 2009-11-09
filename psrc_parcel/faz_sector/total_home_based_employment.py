# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, logical_and

class total_home_based_employment(Variable):
    """
    """
            
    def dependencies(self):
        return ["urbansim_parcel.job.dummy_id",
                "_total_home_based_employment = faz_sector.aggregate(job.building_type==1)", 
               ]

    def compute(self,  dataset_pool):
        faz_sectors = self.get_dataset()
        return faz_sectors.get_attribute("_total_home_based_employment")
