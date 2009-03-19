# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros, logical_and

class total_non_home_based_employment(Variable):
    """
    """
            
    def dependencies(self):
        return ["urbansim_parcel.job.dummy_id",
                "_total_non_home_based_employment = faz_sector.aggregate(job.building_type==2)", 
               ]

    def compute(self,  dataset_pool):
        faz_sectors = self.get_dataset()
        return faz_sectors.get_attribute("_total_non_home_based_employment")
