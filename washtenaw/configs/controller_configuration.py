# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.configuration import Configuration
from washtenaw.configurations.regional_development_project_transition_model_configuration_creator import RegionalDevelopmentProjectTransitionModelConfigurationCreator
from washtenaw.configurations.regional_development_project_location_choice_model_configuration_creator import RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator
from washtenaw.configurations.home_based_regional_employment_location_choice_model_configuration_creator import HomeBasedRegionalEmploymentLocationChoiceModelConfigurationCreator
from washtenaw.configurations.regional_household_location_choice_model_configuration_creator import RegionalHouseholdLocationChoiceModelConfigurationCreator
from washtenaw.configurations.regional_employment_location_choice_model_configuration_creator import RegionalEmploymentLocationChoiceModelConfigurationCreator
from washtenaw.configurations.governmental_regional_employment_location_choice_model_configuration_creator import GovernmentalRegionalEmploymentLocationChoiceModelConfigurationCreator
from washtenaw.configurations.regional_employment_transition_model_configuration_creator import RegionalEmploymentTransitionModelConfigurationCreator
from washtenaw.configurations.regional_household_transition_model_configuration_creator import RegionalHouseholdTransitionModelConfigurationCreator
from washtenaw.configurations.jobs_event_model_configuration_creator import JobsEventModelConfigurationCreator
from washtenaw.configurations.households_event_model_configuration_creator import HouseholdsEventModelConfigurationCreator
from washtenaw.configurations.regional_household_relocation_model_configuration_creator import RegionalHouseholdRelocationModelConfigurationCreator
from washtenaw.configurations.regional_employment_relocation_model_configuration_creator import RegionalEmploymentRelocationModelConfigurationCreator
from washtenaw.configurations.regional_distribute_unplaced_jobs_model_configuration_creator import RegionalDistributeUnplacedJobsModelConfigurationCreator

class ControllerConfiguration(Configuration):
    """ Contains controller entries that differ from the urbansim controllers.
    """
    def __init__(self):
        Configuration.__init__(self)
        self['residential_regional_development_project_location_choice_model'] = {
                    'controller': RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'residential',
                        coefficients_table = 'residential_development_location_choice_model_coefficients',
                        specification_table = 'residential_development_location_choice_model_specification',
                        #submodel_string = None
                        ).execute(),
                    }
        self['commercial_regional_development_project_location_choice_model'] = {
                    'controller': RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'commercial',
                        coefficients_table = 'commercial_development_location_choice_model_coefficients',
                        specification_table = 'commercial_development_location_choice_model_specification',
                        #submodel_string = None
                        ).execute(),
                    }
        self['industrial_regional_development_project_location_choice_model'] = {
                    'controller': RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'industrial',
                        coefficients_table = 'industrial_development_location_choice_model_coefficients',
                        specification_table = 'industrial_development_location_choice_model_specification',
                        #submodel_string = None
                        ).execute(),
                    }
        self['regional_development_project_transition_model'] =  {
                    'controller': RegionalDevelopmentProjectTransitionModelConfigurationCreator(
                        output_results = 'dptm_results',
                        ).execute(),
                    }
        self['regional_household_transition_model'] = {
                    'controller': RegionalHouseholdTransitionModelConfigurationCreator().execute(),
                    }
        self['regional_employment_transition_model'] = {
                    'controller': RegionalEmploymentTransitionModelConfigurationCreator().execute(),
                    }
        self['regional_employment_location_choice_model'] = {
                    'controller': RegionalEmploymentLocationChoiceModelConfigurationCreator(
                        ).execute(),
                    }
        self['home_based_regional_employment_location_choice_model'] = {
                    'controller': HomeBasedRegionalEmploymentLocationChoiceModelConfigurationCreator(
                        ).execute(),
                    }
        self['governmental_regional_employment_location_choice_model'] = {
                    'controller': GovernmentalRegionalEmploymentLocationChoiceModelConfigurationCreator(
                        ).execute(),
                    }
        self['regional_household_location_choice_model'] = {
                    'controller': RegionalHouseholdLocationChoiceModelConfigurationCreator(
                        ).execute(),
                                                            }
        self['regional_household_relocation_model'] = {
                    'controller': RegionalHouseholdRelocationModelConfigurationCreator(
                        ).execute(),
                    }
        self['regional_employment_relocation_model'] = {
                    'controller': RegionalEmploymentRelocationModelConfigurationCreator(
                        ).execute(),
                    }
        self['regional_distribute_unplaced_jobs_model'] = {
                    'controller': RegionalDistributeUnplacedJobsModelConfigurationCreator(
                        ).execute(),
                    }
        self['jobs_event_model'] = {
                    'controller': JobsEventModelConfigurationCreator(
                        ).execute(),
                    }
        self['households_event_model'] = {
                    'controller': HouseholdsEventModelConfigurationCreator(
                        ).execute(),
                    }

#if __name__ == '__main__':
#    ControllerConfiguration()