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

import os
from sets import Set
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import Dataset
from opus_core.store.scenario_database import ScenarioDatabase
from opus_core.storage_factory import StorageFactory
from opus_core.variables.attribute_type import AttributeType
from shutil import rmtree

class CacheMysqlData(Model):
    """Get data from MySQL into a cache.  This includes
    the large database tables and lag data.
    """
    def run(self, config):
        """
        Copy large baseyear datasets from MySQL into cache.
        """
        
        logger.log_status("Caching large MySQL tables to: " + config['cache_directory'])
        debuglevel = config.get('debuglevel', 3)
        input_db = ScenarioDatabase(hostname = config['input_configuration'].host_name,
                                    username = config['input_configuration'].user_name,
                                    password = config['input_configuration'].password,
                                    database_name = config['input_configuration'].database_name)

        simulation_state = SimulationState()
        if 'low_memory_run' in config:
            simulation_state.set_low_memory_run(config['low_memory_run'])
        simulation_state.set_cache_directory(config['cache_directory'])
        simulation_state.set_current_time(config['base_year'])
        
        self.cache_database_tables(config, input_db)

    def cache_database_tables(self, config, input_db):
        """Loads cache with all tables from this database.
        """
        tables_cached = Set()
        for table_name, database_name in input_db.get_table_mapping().iteritems():
            if table_name not in config['creating_baseyear_cache_configuration'].tables_to_cache:
                continue
            try:
                self.cache_database_table(table_name, input_db, config['base_year'], config)
            except:
                logger.log_error("Problem caching table %s from database %s.%s" % 
                                 (table_name, input_db.hostname, database_name))
                raise
            tables_cached.add(table_name)
        
        # Were all these tables cached?
        un_cached_tables = Set(config['creating_baseyear_cache_configuration'].tables_to_cache) - tables_cached
        if un_cached_tables:
            logger.log_warning('The following requested tables were NOT cached:')
            for table_name in un_cached_tables:
                logger.log_warning('    %s' % table_name)
                
    def cache_database_table(self, table_name, input_db, year, config):
        """Copy this table from input database into attribute cache.
        """
        logger.start_block('Caching table %s' % table_name)
        try:
            in_storage = StorageFactory().build_storage_for_dataset(type='mysql_storage', 
                storage_location=input_db)
            config['storage_location'] = os.path.join(config['cache_directory'], str(year), table_name)
            
            if not os.path.exists(config['storage_location']):
                flt_storage = StorageFactory().get_storage(type='flt_storage', subdir='store', 
                    storage_location=config['storage_location'])
                if table_name == 'gridcells':  # TODO: Remove this evil hack once we can determine the primary keys for tables.
                    id_name = ['grid_id']
                elif table_name == 'buildings':
                    id_name = ['building_id']
                elif table_name == 'parcels':
                    id_name = ['parcel_id']
                else:
                    id_name = []
                dataset = Dataset(resources=config, 
                                  in_storage=in_storage,
                                  out_storage=flt_storage,
                                  in_table_name=table_name,
                                  id_name = id_name)
                nchunks = config['creating_baseyear_cache_configuration'].tables_to_cache_nchunks.get(table_name, 1)
                current_time = SimulationState().get_current_time()
                SimulationState().set_current_time(year)
                dataset.load_dataset(nchunks=nchunks, flush_after_each_chunk=True)
                SimulationState().set_current_time(current_time)
            else:
                logger.log_status(config['storage_location'] + " already exits; skip caching " + table_name)
            
        finally:
            logger.end_block()
