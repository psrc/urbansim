# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.scaling_jobs_model import ScalingJobsModel as UrbansimScalingJobsModel

class ScalingJobsModel(UrbansimScalingJobsModel):
    """
    This model works exactly as its parent. It uses different variable_package.
    It is used for locating scalable jobs into buildings.  
    """
    variable_package = "urbansim_parcel"
