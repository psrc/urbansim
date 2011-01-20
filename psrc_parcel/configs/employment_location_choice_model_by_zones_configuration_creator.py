# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator

class EmploymentLocationChoiceModelByZonesConfigurationCreator(EmploymentLocationChoiceModelConfigurationCreator):
    _model_name = 'employment_location_choice_model_by_geography'
    def execute(self):
        result = EmploymentLocationChoiceModelConfigurationCreator.execute(self)
        result['import'] = {
                'psrc_parcel.models.%s' % self._model_name: 'EmploymentLocationChoiceModelByGeography'
                }
        result['init']['name'] = 'EmploymentLocationChoiceModelByGeography'
        result["init"]["arguments"]["geography_dataset"] = 'zone'
        return result