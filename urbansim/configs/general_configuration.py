# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
from opus_core.configuration import Configuration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration

from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange

from urbansim.configurations.land_price_model_configuration_creator import LandPriceModelConfigurationCreator
from urbansim.configurations.events_coordinator_configuration_creator import EventsCoordinatorConfigurationCreator
from urbansim.configurations.prescheduled_events_configuration_creator import PrescheduledEventsConfigurationCreator
from urbansim.configurations.home_based_choice_model_configuration_creator import HomeBasedChoiceModelConfigurationCreator
from urbansim.configurations.real_estate_price_model_configuration_creator import RealEstatePriceModelConfigurationCreator
from urbansim.configurations.development_project_type_configuration_creator import DevelopmentProjectTypeConfigurationCreator
from urbansim.configurations.building_transition_model_configuration_creator import BuildingTransitionModelConfigurationCreator
from urbansim.configurations.building_relocation_model_configuration_creator import BuildingRelocationModelConfigurationCreator
from urbansim.configurations.development_project_types_configuration_creator import DevelopmentProjectTypesConfigurationCreator
from urbansim.configurations.household_transition_model_configuration_creator import HouseholdTransitionModelConfigurationCreator
from urbansim.configurations.household_relocation_model_configuration_creator import HouseholdRelocationModelConfigurationCreator
from urbansim.configurations.auto_ownership_choice_model_configuration_creator import AutoOwnershipChoiceModelConfigurationCreator
from urbansim.configurations.employment_transition_model_configuration_creator import EmploymentTransitionModelConfigurationCreator
from urbansim.configurations.employment_relocation_model_configuration_creator import EmploymentRelocationModelConfigurationCreator
from urbansim.configurations.residential_land_share_model_configuration_creator import ResidentialLandShareModelConfigurationCreator
from urbansim.configurations.building_location_choice_model_configuration_creator import BuildingLocationChoiceModelConfigurationCreator
from urbansim.configurations.distribute_unplaced_jobs_model_configuration_creator import DistributeUnplacedJobsModelConfigurationCreator
from urbansim.configurations.household_location_choice_model_configuration_creator import HouseholdLocationChoiceModelConfigurationCreator
from urbansim.configurations.employment_location_choice_model_configuration_creator import EmploymentLocationChoiceModelConfigurationCreator
from urbansim.configurations.development_event_transition_model_configuration_creator import DevelopmentEventTransitionModelConfigurationCreator
from urbansim.configurations.development_project_transition_model_configuration_creator import DevelopmentProjectTransitionModelConfigurationCreator
from urbansim.configurations.development_project_location_choice_model_configuration_creator import DevelopmentProjectLocationChoiceModelConfigurationCreator
from urbansim.configurations.home_based_employment_location_choice_model_configuration_creator import HomeBasedEmploymentLocationChoiceModelConfigurationCreator
from urbansim.configurations.governmental_employment_location_choice_model_configuration_creator import GovernmentalEmploymentLocationChoiceModelConfigurationCreator


# This configuration contains all of the informaiton needed for the code
# to know how to process the desired range of development projects.
# This should be globally accessible, so that models and datasets
# can know what flavors of development projects exist.

class GeneralConfiguration(Configuration):
    """Specifies the common set of configuration values for use by an UrbanSim model system.

    Additional configuration information must be provided before running,
    such as which database name to use for the inputs.
    Typically these are specified by a CachingConfiguration,
    SimulatingConfiguration, or EstimatingConfiguration that merges
    values into this configuration."""
    def __init__(self):
        config_changes = self._get_initial_config()
        self.merge(config_changes)

    def _get_initial_config(self):
        """Encapsulate dirty inner workings"""
        debuglevel = 4
        
        config = {
            'models_configuration': {
                'development_project_types': DevelopmentProjectTypesConfigurationCreator(
                    commercial = DevelopmentProjectTypeConfigurationCreator(
                        categories = [1000, 2000, 5000, 10000],
                        #categories = [],
                        developable_maximum_unit_variable_full_name = 'urbansim.gridcell.developable_maximum_commercial_sqft',
                        developable_minimum_unit_variable_full_name = 'urbansim.gridcell.developable_minimum_commercial_sqft',
                        residential = False,
                        units = 'commercial_sqft',
                        ),
                    industrial = DevelopmentProjectTypeConfigurationCreator(
                        categories = [1000,2000,5000,10000],
                        #categories = [],
                        developable_maximum_unit_variable_full_name = 'urbansim.gridcell.developable_maximum_industrial_sqft',
                        developable_minimum_unit_variable_full_name = 'urbansim.gridcell.developable_minimum_industrial_sqft',
                        residential = False,
                        units = 'industrial_sqft',
                        ),
                    residential = DevelopmentProjectTypeConfigurationCreator(
                        categories = [1,2,3,5,10,20],
                        #categories = [],
                        developable_maximum_unit_variable_full_name = 'urbansim.gridcell.developable_maximum_residential_units',
                        developable_minimum_unit_variable_full_name = 'urbansim.gridcell.developable_minimum_residential_units',
                        residential = True,
                        units = 'residential_units',
                        )
                    ).execute(),
                'residential_development_project_location_choice_model':{
                    'controller': DevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'residential',
                        coefficients_table = 'residential_development_location_choice_model_coefficients',
                        specification_table = 'residential_development_location_choice_model_specification',
                        #submodel_string = None
                        ).execute(),
                    },
                'commercial_development_project_location_choice_model':{
                    'controller': DevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'commercial',
                        coefficients_table = 'commercial_development_location_choice_model_coefficients',
                        specification_table = 'commercial_development_location_choice_model_specification',
                        #submodel_string = None
                        ).execute(),
                    },
                'industrial_development_project_location_choice_model':{
                    'controller': DevelopmentProjectLocationChoiceModelConfigurationCreator(
                        project_type = 'industrial',
                        coefficients_table = 'industrial_development_location_choice_model_coefficients',
                        specification_table = 'industrial_development_location_choice_model_specification',
                        #submodel_string = None
                        ).execute(),
                    },
                'prescheduled_events': {
                    'controller': PrescheduledEventsConfigurationCreator(
                        output_events = 'development_events',
                        ).execute(),
                    },
                'events_coordinator': {
                    'controller': EventsCoordinatorConfigurationCreator(
                        input_events = 'development_events',
                        output_changed_indices = 'changed_indices',
                        ).execute(),
                    'default_type_of_change':DevelopmentEventTypeOfChange.ADD,
                    },
                'home_based_choice_model': {
                    'controller': HomeBasedChoiceModelConfigurationCreator().execute(),
                    },
                'auto_ownership_choice_model': {
                    'controller': AutoOwnershipChoiceModelConfigurationCreator().execute(),
                    },
                'residential_land_share_model': {
                    'controller': ResidentialLandShareModelConfigurationCreator(
                        debuglevel = debuglevel,
                        input_changed_indices = 'changed_indices',
                        ).execute(),
                    },
                'land_price_model': {
                    'controller': LandPriceModelConfigurationCreator(
                        debuglevel = debuglevel,
                        ).execute(),
                    },
                'development_project_transition_model': {
                    'controller': DevelopmentProjectTransitionModelConfigurationCreator(
                        debuglevel = debuglevel,
                        output_results = 'dptm_results',
                        ).execute(),
                    },
                'development_event_transition_model': {
                    'controller': DevelopmentEventTransitionModelConfigurationCreator(
                        input_projects = 'dptm_results',
                        output_events = 'development_events',
                        ).execute(),
                    },
                'household_transition_model': {
                    'controller': HouseholdTransitionModelConfigurationCreator().execute(),
                    },
                'employment_transition_model': {
                    'controller': EmploymentTransitionModelConfigurationCreator().execute(),
                    },
                'household_relocation_model': {
                    'controller': HouseholdRelocationModelConfigurationCreator(
                        output_index = 'hrm_index',
                        ).execute(),
                    },
                'household_location_choice_model': {
                    'controller': HouseholdLocationChoiceModelConfigurationCreator(
                        input_index = 'hrm_index',
                        ).execute(),
                    },
                'employment_relocation_model': {
                    'controller': EmploymentRelocationModelConfigurationCreator(
                        output_index = 'erm_index',
                        ).execute(),
                    },
                'employment_location_choice_model': {
                    'controller': EmploymentLocationChoiceModelConfigurationCreator(
                        input_index = 'erm_index',
                        ).execute(),
                    },
                # These are deviations from the general ELCM for the two home_based ELCMs (sfh, mfh)
                'home_based_employment_location_choice_model': {
                    'controller': HomeBasedEmploymentLocationChoiceModelConfigurationCreator(
                        input_index = 'erm_index',
                        ).execute(),
                    },
                'governmental_employment_location_choice_model': {
                    'controller': GovernmentalEmploymentLocationChoiceModelConfigurationCreator(
                        input_index = 'erm_index',
                        ).execute(),
                    },
                'distribute_unplaced_jobs_model': {
                    'controller': DistributeUnplacedJobsModelConfigurationCreator().execute(),
                    },
                'real_estate_price_model': {
                    'controller': RealEstatePriceModelConfigurationCreator().execute(),
                    },
                'building_transition_model': {
                    'controller': BuildingTransitionModelConfigurationCreator().execute(),
                    },
                'building_relocation_model': {
                    'controller': BuildingRelocationModelConfigurationCreator(
                        output_index = 'brm_index',
                        ).execute(),
                    },
                'building_location_choice_model': {
                    'controller': BuildingLocationChoiceModelConfigurationCreator(
                        input_index = 'brm_index',
                        ).execute(),
                    },
                },
            'model_system':'urbansim.model_coordinators.model_system',
            'models':[ # models are executed in the same order as in this list
                "prescheduled_events",
                "events_coordinator",
                "residential_land_share_model",
                'land_price_model',
                'development_project_transition_model',
                'residential_development_project_location_choice_model',
                'commercial_development_project_location_choice_model',
                'industrial_development_project_location_choice_model',
                "development_event_transition_model",
                "events_coordinator",
                "residential_land_share_model",
                "household_transition_model",
                "employment_transition_model",
                "household_relocation_model",
                "household_location_choice_model",
                "employment_relocation_model",
                {"employment_location_choice_model": {"group_members": "_all_"}},
                "distribute_unplaced_jobs_model"
                ],
            'years':(2001, 2030),
            'debuglevel':debuglevel,
            'flush_variables':False,
            'seed':0,#(0,0),
            'chunk_specification':{ # Default value
                'nchunks':1,
                },
            'datasets_to_cache_after_each_model':[ # datasets to be cached after each model,
                'gridcell',
                'household',
                'job'],
            'datasets_to_preload': { # Datasets that should be loaded before each year, e.g. in order to pass them as model arguments.
                'gridcell':{         # All remaining datasets are used via SessionConfiguration
                    'nchunks':2
                    },               # linked to the cache.
                'household':{
                    },
                'job':{
                    },
                'zone':{
                    },
                'development_type':{},
                'target_vacancy':{},
                'development_event_history':{},
                'development_constraint':{},
                'job_building_type':{},
#                'building_type':{},
#                'building':{},
                'vacant_land_and_building_type':{},
                'urbansim_constant':{},
                },
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['urbansim', 'opus_core'],
                ),
            'services_database_configuration':ServicesDatabaseConfiguration(),
            }

        return config
        

from opus_core.tests import opus_unittest


class Tests(opus_unittest.OpusTestCase):
    def test(self):
        config = GeneralConfiguration()
        self.assert_('models' in config)
        self.assert_('scenario_database_configuration' not in config)
        self.assert_('estimation_database_configuration' not in config)
        
        
if __name__ == '__main__':
    opus_unittest.main()