# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.configs.employment_location_choice_model_by_zones_configuration_creator import EmploymentLocationChoiceModelByZonesConfigurationCreator

class EmploymentLocationChoiceModelByZipcodesConfigurationCreator(EmploymentLocationChoiceModelByZonesConfigurationCreator):
    def execute(self):
        result = EmploymentLocationChoiceModelByZonesConfigurationCreator.execute(self)
        result["init"]["arguments"]["geography_dataset"] = 'zipcode'
        return result