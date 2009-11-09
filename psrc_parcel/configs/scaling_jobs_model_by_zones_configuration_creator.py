# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configurations.governmental_employment_location_choice_model_configuration_creator import GovernmentalEmploymentLocationChoiceModelConfigurationCreator

class ScalingJobsModelByZonesConfigurationCreator(GovernmentalEmploymentLocationChoiceModelConfigurationCreator):
    _model_name = 'scaling_jobs_model_by_geography'
    def execute(self):
        result = GovernmentalEmploymentLocationChoiceModelConfigurationCreator.execute(self)
        result['import'] = {
                'psrc_parcel.models.%s' % self._model_name: 'ScalingJobsModelByGeography'
                }
        result['init']['name'] = 'ScalingJobsModelByGeography'
        result["run"]["arguments"]["geography_set"] = 'zone'
        return result
