# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from psrc_parcel.configs.scaling_jobs_model_by_zones_configuration_creator import ScalingJobsModelByZonesConfigurationCreator

class ScalingJobsModelByZipcodesConfigurationCreator(ScalingJobsModelByZonesConfigurationCreator):

    def execute(self):
        result = ScalingJobsModelByZonesConfigurationCreator.execute(self)
        result["run"]["arguments"]["geography_set"] = 'zipcode'
        return result
