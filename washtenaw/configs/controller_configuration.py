#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.configuration import Configuration
from washtenaw.configurations.regional_development_project_transition_model_configuration_creator import RegionalDevelopmentProjectTransitionModelConfigurationCreator
from washtenaw.configurations.regional_development_project_location_choice_model_configuration_creator import RegionalDevelopmentProjectLocationChoiceModelConfigurationCreator
from washtenaw.configurations.home_based_regional_employment_location_choice_model_configuration_creator import HomeBasedRegionalEmploymentLocationChoiceModelConfigurationCreator
from washtenaw.configurations.regional_household_location_choice_model_configuration_creator import RegionalHouseholdLocationChoiceModelConfigurationCreator
from washtenaw.configurations.regional_employment_location_choice_model_configuration_creator import RegionalEmploymentLocationChoiceModelConfigurationCreator
from washtenaw.configurations.regional_employment_transition_model_configuration_creator import RegionalEmploymentTransitionModelConfigurationCreator
from washtenaw.configurations.regional_household_transition_model_configuration_creator import RegionalHouseholdTransitionModelConfigurationCreator
from washtenaw.configurations.deletion_event_model_configuration_creator import DeletionEventModelConfigurationCreator
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
        self['deletion_event_model'] = {
                    'controller': DeletionEventModelConfigurationCreator(
                        ).execute(),
                    }

#if __name__ == '__main__':
#    ControllerConfiguration()