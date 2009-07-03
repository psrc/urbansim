# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, re
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory

from opus_core.database_management.scenario_database_manager import ScenarioDatabaseManager
from opus_core.database_management.database_server import DatabaseServer

class CacheScenarioDatabase(Model):
    """Extract a flattened scenario database to the cache.
    """
    def run(self, config, show_output = False):
        logger.log_status("Caching large SQL tables to: " + config['cache_directory'])
        self.show_output = show_output
        
        #import pydevd;pydevd.settrace()
        
        server_configuration = config['scenario_database_configuration']
        
        scenario_database_manager = ScenarioDatabaseManager(
            server_configuration = server_configuration, 
            base_scenario_database_name = server_configuration.database_name                                                         
        )
        
        self.database_server = DatabaseServer(server_configuration)
        
        database_to_table_mapping = scenario_database_manager.get_database_to_table_mapping()
        
        self.tables_to_cache = config['creating_baseyear_cache_configuration'].tables_to_cache
                
        simulation_state = SimulationState()
        if 'low_memory_run' in config:
            simulation_state.set_low_memory_run(config['low_memory_run'])
        simulation_state.set_cache_directory(config['cache_directory'])
        simulation_state.set_current_time(config['base_year'])
                  
        self.tables_cached = set()      
        for database_name, tables in database_to_table_mapping.items():
            self.cache_database_tables(config, database_name, tables)

        un_cached_tables = set(self.tables_to_cache) - self.tables_cached
        if un_cached_tables:
            logger.log_warning('The following requested tables were NOT cached:')
            for table_name in un_cached_tables:
                logger.log_warning('\t%s' % table_name)
                
    def cache_database_tables(self, config, database_name, tables):
        """Loads cache with all tables from this database.
        """
        database = self.database_server.get_database(database_name)
        in_storage = StorageFactory().get_storage(
            type='sql_storage',
            storage_location = database)
        
        for table_name in tables:
            if table_name in self.tables_to_cache:
                try:
                    self.cache_database_table(table_name, config['base_year'], database, in_storage, config)
                except:
                    logger.log_error("Problem caching table %s from database %s" % 
                                     (table_name, database_name))
                    raise
                self.tables_cached.add(table_name)
        
    def cache_database_table(self, table_name, base_year, database, in_storage, config):
        """Copy this table from input database into attribute cache.
        """
        logger.start_block('Caching table %s' % table_name)
        try:
            #TODO: why is the config being modified...seems like its kind of useless here...
            config['storage_location'] = os.path.join(config['cache_directory'], str(base_year), table_name)
            
            if not os.path.exists(config['storage_location']):
                flt_storage = StorageFactory().get_storage(
                   type='flt_storage', 
                   subdir='store', 
                   storage_location=config['storage_location'])
                
                table = database.get_table(table_name)
                
                id_name = [primary_key.name for primary_key in table.primary_key]                    

                dataset = Dataset(resources=config, 
                                  in_storage=in_storage,
                                  out_storage=flt_storage,
                                  in_table_name=table_name,
                                  id_name = id_name)

                nchunks = config['creating_baseyear_cache_configuration'].tables_to_cache_nchunks.get(table_name, 1)
                current_time = SimulationState().get_current_time()
                SimulationState().set_current_time(base_year)
                dataset.load_dataset(nchunks=nchunks, flush_after_each_chunk=True)
                SimulationState().set_current_time(current_time)
            else:
                logger.log_status(config['storage_location'] + " already exits; skip caching " + table_name)
            
        finally:
            logger.end_block()