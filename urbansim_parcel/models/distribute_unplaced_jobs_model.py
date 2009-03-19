# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.models.distribute_unplaced_jobs_model import DistributeUnplacedJobsModel as UrbansimDistributeUnplacedJobsModel

class DistributeUnplacedJobsModel(UrbansimDistributeUnplacedJobsModel):
    """
    This model works exactly as its parent. It uses different variable_package.
    It is used for locating scalable jobs into buildings.  
    """
    variable_package = "urbansim_parcel"
