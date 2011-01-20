# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.zone.number_of_jobs import number_of_jobs as urbansim_number_of_jobs

class number_of_jobs(urbansim_number_of_jobs):
    """Number of jobs in zones """

    def dependencies(self):
        return ["urbansim_parcel.job.zone_id"]