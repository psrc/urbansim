# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
from urbansim.configs.general_configuration import GeneralConfiguration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from psrc.configs.create_travel_model_configuration import create_travel_model_configuration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration

class ModelConfig(GeneralConfiguration):
    """PSRC's baseline configuration.
    """
    def __init__(self, cache_directory, year, 
                 travel_model_data_directory='baseline_travel_model_psrc_baseline'):
        
        config = AbstractUrbansimConfiguration()
        
        config_changes = {
            'description':'baseline with travel model',

            'cache_directory':cache_directory,
            'creating_baseyear_cache_configuration':CreatingBaseyearCacheConfiguration(
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                unroll_gridcells = False,
                tables_to_cache = [],
                tables_to_copy_to_previous_years = {},
                ),
            'models':[],  # run no urbansim models
            'scenario_database_configuration': ScenarioDatabaseConfiguration(
                database_name = 'PSRC_2000_baseyear',
                ),
            'base_year':year,
            'years':(year, year),
            }
        config.merge(config_changes)
        
        years_to_run = {
            2005:'2000_06',
            2010:'2010_06',
            2015:'2010_06',
            2020:'2020_06',
            2025:'2020_06',
            2030:'2030_06',
            }
        year_to_run = {year:years_to_run[year]}
        travel_model_config = create_travel_model_configuration(travel_model_data_directory, 
                                                                mode='get_emme2_data_after_run',
                                                                years_to_run = year_to_run,
                                                                emme2_batch_file='QUICKRUN.BAT')
        config['travel_model_configuration'] = travel_model_config
        self.merge(config)


if __name__ == "__main__":
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file 
    from opus_core.file_utilities import write_resources_to_file
    from opus_core.store.attribute_cache import AttributeCache
    from opus_core.fork_process import ForkProcess
    
    parser = OptionParser()
    parser.add_option("-d", "--cache-directory", dest="cache_directory", action="store", type="string",
                      help="Year in which to 'run' the travel model")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    parser.add_option("-t", "--travel-model", dest="travel_model", default="baseline", 
                      help="which travel model data to use")
    
    (options, args) = parser.parse_args()
    travel_models = {"baseline":"baseline_travel_model_psrc",
                     "no_build":"baseline_travel_model_psrc_no_build",
                     "one_half_highway":"baseline_travel_model_psrc_highway_x_1.5",
                     }
    travel_model_path = travel_models[options.travel_model]
    config = ModelConfig(options.cache_directory, options.year, travel_model_path)

    ForkProcess().fork_new_process('opus_core.tools.start_run', resources=config,
                                   optional_args=["--hostname", "None"])
    