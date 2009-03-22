# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configurations.household_location_choice_model_configuration_creator import HouseholdLocationChoiceModelConfigurationCreator

class HouseholdLocationChoiceModelByZonesConfigurationCreator(HouseholdLocationChoiceModelConfigurationCreator):
    _model_name = 'household_location_choice_model_by_zones'
    def execute(self):
        result = HouseholdLocationChoiceModelConfigurationCreator.execute(self)
        result['import'] = {
                'psrc_parcel.models.%s' % self._model_name: 'HouseholdLocationChoiceModelByZones'
                }
        result['init']['name'] = 'HouseholdLocationChoiceModelByZones'
        result["run"]["arguments"]["zones"] = 'zone'
        return result