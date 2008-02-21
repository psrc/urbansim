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

from numpy import array, arange
from opus_core.configuration import Configuration
from psrc_parcel.configs.baseline import Baseline
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.database_management.database_configuration import DatabaseConfiguration
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.storage_factory import StorageFactory
from opus_core.store.attribute_cache import AttributeCache
from psrc.datasets.person_dataset import PersonDataset
from urbansim.model_coordinators.cache_scenario_database import CacheScenarioDatabase
import os

class ExpandPersons(object):
    """This class creates a persons table from households by inserting 1 record for each worker in a household"""
    ## TODO: Is this class in use?
    def __init__(self, config):
        if 'output_configuration' in config:
#            config = Baseline()
            db_config = DatabaseServerConfiguration(
                host_name=config['output_configuration'].host_name,
                user_name=config['output_configuration'].user_name,
                password=config['output_configuration'].password                                                    
            )
            db_server = DatabaseServer(db_config)
            db = db_server.get_database(config['output_configuration'].database_name)
        
            out_storage = StorageFactory().build_storage_for_dataset(
                type='sql_storage', storage_location=db)
        else:
            out_storage = StorageFactory().get_storage(type='flt_storage',
                storage_location=os.path.join(config['cache_directory'], str(config['base_year']+1)))

        simulation_state = SimulationState()
        simulation_state.set_cache_directory(config['cache_directory'])
        simulation_state.set_current_time(config['base_year'])
        attribute_cache = AttributeCache()
        
        SessionConfiguration(new_instance=True,
                             package_order=config['dataset_pool_configuration'].package_order,
                             package_order_exceptions=config['dataset_pool_configuration'].package_order_exceptions,
                             in_storage=attribute_cache)
        
        if not os.path.exists(os.path.join(config['cache_directory'], str(config['base_year']))):
            #raise RuntimeError, "datasets uncached; run prepare_estimation_data.py first"
            CacheScenarioDatabase().run(config, unroll_gridcells=False)

        for dataset_name in config['datasets_to_preload']:
            SessionConfiguration().get_dataset_from_pool(dataset_name)

        households = SessionConfiguration().get_dataset_from_pool("household")
        household_ids = households.get_id_attribute()
        workers = households.get_attribute("workers")
        
        hh_ids = []
        member_ids = []
        is_worker = []
        job_ids = []

        for i in range(households.size()):  
            if workers[i] > 0:
                hh_ids += [household_ids[i]] * workers[i]
                member_ids += range(1, workers[i]+1)
                is_worker += [1] * workers[i]
                job_ids += [-1] * workers[i]

        in_storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        in_storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':arange(len(hh_ids))+1,
                    'household_id':array(hh_ids),
                    'member_id':array(member_ids),
                    'is_worker':array(is_worker),                    
                    'job_id':array(job_ids),
                    },
            )

        persons = PersonDataset(in_storage=in_storage, in_table_name=persons_table_name)
        persons.write_dataset(out_storage=out_storage, out_table_name=persons_table_name)

if __name__ == '__main__':
    config = Baseline()
    config.replace({
        'input_configuration': DatabaseConfiguration(
            database_name = 'psrc_2005_parcel_baseyear',
            ),
        'output_configuration': DatabaseConfiguration(
            database_name = 'psrc_2005_parcel_baseyear_change_20080219',
            ),
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['urbansim_parcel','urbansim', 'opus_core'],
            package_order_exceptions={},
            ),
        'low_memory_mode': False,
        'cache_directory': '/urbansim_cache/psrc_parcel/persons',
        'debuglevel':7,
        'base_year': 2000,
        'years': (2000,2000),
        },
    )

#    del config['output_configuration']['db_output_database']
    ExpandPersons(config)