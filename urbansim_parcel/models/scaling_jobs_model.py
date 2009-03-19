# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.models.scaling_jobs_model import ScalingJobsModel as UrbansimScalingJobsModel

class ScalingJobsModel(UrbansimScalingJobsModel):
    """
    This model works exactly as its parent. It uses different variable_package.
    It is used for locating scalable jobs into buildings.  
    """
    variable_package = "urbansim_parcel"
