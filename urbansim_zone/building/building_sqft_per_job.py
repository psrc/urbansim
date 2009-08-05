# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim_parcel.building.building_sqft_per_job import building_sqft_per_job as parcel_building_sqft_per_job

class building_sqft_per_job(parcel_building_sqft_per_job):
    """ building sqft per job disaggregated from the zonal-building_type averages"""
        
    def dependencies(self):
        return ["building_sqft_per_job.building_sqft_per_job",
                "building.zone_id",
                "building.building_type_id",
                ]
