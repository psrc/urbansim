# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import copy

from sets import Set
from shutil import rmtree, copytree

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.simulation_state import SimulationState
from opus_core.variables.attribute_type import AttributeType
from opus_core.cache.cache_scenario_database import CacheScenarioDatabase as CoreCacheScenarioDatabase
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from urbansim.model_coordinators.unroll_gridcells import UnrollGridcells
from opus_core.session_configuration import SessionConfiguration


class CacheScenarioDatabase(Model):
    """Get data from MySQL into urbansim cache.  This includes
    the large database tables and lag data.
    """
    def run(self, 
            config = None, ### TODO: Get rid of this parameter!
            unroll_gridcells = None, ### TODO: Get rid of this parameter!
            cache_directory = None, 
            base_year = None,
            creating_baseyear_cache_configuration = None,
            debuglevel = None,
            ):
        """
        Copy large baseyear datasets from MySQL into cache.
        """
        
        config = Resources(config)
        
        if unroll_gridcells is None:
            unroll_gridcells = config['creating_baseyear_cache_configuration'].unroll_gridcells
            
        if cache_directory is None:
            cache_directory = config['cache_directory']
            
        if base_year is None:
            base_year = config['base_year']
            
        if creating_baseyear_cache_configuration is None:
            creating_baseyear_cache_configuration = copy.deepcopy(config['creating_baseyear_cache_configuration'])
        
        if debuglevel is None:
            debuglevel = config.get('debuglevel', 3)

        CoreCacheScenarioDatabase().run(config)
        
        self.prepare_data_before_baseyear(
            cache_directory,
            base_year,
            creating_baseyear_cache_configuration
            )
        
    def prepare_data_before_baseyear(self, 
                                     cache_directory, 
                                     base_year,
                                     creating_baseyear_cache_configuration):
        if creating_baseyear_cache_configuration.unroll_gridcells:
            sc = SessionConfiguration()
            gridcells = sc.get_dataset_from_pool('gridcell')
            development_event_history = sc.get_dataset_from_pool('development_event_history')
        
            UnrollGridcells().unroll_gridcells_to_cache(gridcells, development_event_history,
                                                        cache_directory, base_year)
            # If you want to unroll the gridcells using your buildings table, exchange the 
            # previous two calls by the two following ones.
            #buildings = sc.get_dataset_from_pool('building')
            #UnrollGridcells().unroll_gridcells_to_cache_from_buildings(gridcells, buildings,
            #                                            cache_directory, base_year)
   
        attribute_cache = AttributeCache()
        self._initialize_previous_years(attribute_cache, base_year,
                                        creating_baseyear_cache_configuration)
   
    def _initialize_previous_years(self, attribute_cache, 
                                   base_year,
                                   creating_baseyear_cache_configuration):
        simulation_state = SimulationState()
        cache_directory = simulation_state.get_cache_directory()

        baseyear_cache_path = os.path.join(cache_directory, str(base_year))
        for table_name, year in creating_baseyear_cache_configuration.tables_to_copy_to_previous_years.iteritems():
            year_cache_path = os.path.join(cache_directory, str(year))
            dest_file_path = os.path.join(year_cache_path, table_name)
            if os.path.exists(dest_file_path):
                rmtree(dest_file_path)
            copytree(os.path.join(baseyear_cache_path, table_name),
                     dest_file_path)
        
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    from opus_core.store.attribute_cache import AttributeCache
    
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

#    logger.enable_memory_logging()
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,
                         in_storage=AttributeCache())
    CacheScenarioDatabase().run(resources)