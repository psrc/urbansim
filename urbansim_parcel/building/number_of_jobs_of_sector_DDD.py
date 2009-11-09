# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.gridcell.number_of_jobs_of_sector_DDD import number_of_jobs_of_sector_DDD as us_number_of_jobs_of_sector_DDD
from urbansim.functions import attribute_label

class number_of_jobs_of_sector_DDD(us_number_of_jobs_of_sector_DDD):
    """Sum the number of jobs for a given building that are in the employment sector specified by DDD.
       (see code in the parent's class) 
    """
    def dependencies(self):
        return [attribute_label("job", self.job_is_in_employment_sector),
                'job.building_id']
