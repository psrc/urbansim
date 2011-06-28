# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array
from opus_core.variables.variable import Variable

class fraction_of_SSS_jobs_of_sector_DDD_combined(Variable):
    """ Combines fraction_of_jobs_of_sector_DDD (urbansim_parcel) with its static version (applied to new buildings, i.e. without jobs).
        Then buildings without any available job space of the given type are filtered out.
    """
    _return_type="float32"
    
    def __init__(self, type, sector_id):
        self.sector_id = sector_id
        self.type = type
        Variable.__init__(self)
        
    def dependencies(self):
        return ["urbansim_parcel.building.fraction_of_jobs_of_sector_%s" % self.sector_id,
                "urbansim_parcel.building.number_of_jobs",
                "psrc_parcel.building.fraction_of_jobs_of_sector_%s_static" % self.sector_id,
                "psrc_parcel.building.vacant_%s_job_space" % self.type]
        
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return (ds["fraction_of_jobs_of_sector_%s" % self.sector_id] + 
                ((ds["number_of_jobs"] == 0)*ds["fraction_of_jobs_of_sector_%s_static" % self.sector_id]))*ds["building.vacant_%s_job_space" % self.type]

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
