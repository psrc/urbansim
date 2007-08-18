#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

#from urbansim.estimation.config import config
from opus_core.configurations.database_configuration import DatabaseConfiguration
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configs.general_configuration import GeneralConfiguration
from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from psrc_parcel.configs.household_location_choice_model_by_zones_configuration_creator import HouseholdLocationChoiceModelByZonesConfigurationCreator
from urbansim.configurations.household_relocation_model_configuration_creator import HouseholdRelocationModelConfigurationCreator
from opus_core.resources import merge_resources_with_defaults
from numpy import array
import os

class ConfigBuildingsNonResidential(UrbansimParcelConfiguration):
    def __init__(self):
        config = UrbansimParcelConfiguration()

        config_changes = {
            'description':'data preparation for PSRC parcel (buildings)',
            'cache_directory': None,
            'creating_baseyear_cache_configuration': CreatingBaseyearCacheConfiguration(
                #cache_directory_root = r'/Users/hana/urbansim_cache/psrc/parcel',
                cache_directory_root = r'/urbansim_cache/psrc_parcel',
                #cache_directory_root = r'/workspace/urbansim_cache/psrc_parcel',
                cache_from_mysql = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    #existing_cache_to_copy = r'/Users/hana/urbansim_cache/psrc/cache_source_parcel',
                    existing_cache_to_copy = r'/urbansim_cache/psrc_parcel/cache_source',
                    #existing_cache_to_copy = r'/workspace/urbansim_cache/psrc_parcel/estimation',
                    years_to_cache = [2000]
                    ),
                cache_mysql_data = 'urbansim.model_coordinators.cache_mysql_data',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                package_order_exceptions={},
                ),
            'base_year':2000,
            'years':(2000, 2000),
            'models':[ # models are executed in the same order as in this list
                 "expected_sale_price_model",
                 "development_proposal_choice_model",
                 "building_construction_model",
                ],
            "datasets_to_preload":{
                    'zone':{},
                    'household':{},
                    'building': {},
                   #'development_project_proposal': {}
                },
            "datasets_to_cache_after_each_model": [
                     'parcel', 'building', 'development_project_proposal', 'household', 'job'
                     ]
        }
        #use configuration in config as defaults and merge with config_changes
        config.replace(config_changes)
        self.merge(config)
        self['models_configuration']['development_proposal_choice_model']['controller']["import"] =  {
                       "psrc_parcel.models.development_proposal_sampling_model_by_zones":
                       "DevelopmentProposalSamplingModelByZones"
                       }
        self['models_configuration']['development_proposal_choice_model']['controller']["init"]["name"] =\
                        "DevelopmentProposalSamplingModelByZones"
        self['models_configuration']['development_proposal_choice_model']['controller']['run']['arguments']["zones"] = 'zone'
        self['models_configuration']['development_proposal_choice_model']['controller']['run']['arguments']["type"] = "'non_residential'"
        self['models_configuration']['expected_sale_price_model']['controller']["prepare_for_run"]['arguments']["parcel_filter"] = \
            "'numpy.logical_and(numpy.logical_or(numpy.logical_not(urbansim_parcel.parcel.is_residential_land_use_type), numpy.logical_and(parcel.land_use_type_id==26, urbansim_parcel.parcel.is_non_residential_plan_type)), urbansim_parcel.parcel.vacant_land_area > 0)'"
                #"'numpy.logical_or(parcel.land_use_type_id==26, numpy.logical_and(urbansim_parcel.parcel.is_residential_land_use_type, urbansim_parcel.parcel.vacant_land_area > 0))'"
                