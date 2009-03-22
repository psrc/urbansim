# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import array, arange
from psrc_parcel.configs.baseline import Baseline
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration
from opus_core.database_management.configurations.estimation_database_configuration import EstimationDatabaseConfiguration
from opus_core.database_management.database_server import DatabaseServer
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
        if 'estimation_database_configuration' in config:
            db_server = DatabaseServer(config['estimation_database_configuration'])
            db = db_server.get_database(config['estimation_database_configuration'].database_name)
        
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
        'scenario_database_configuration': ScenarioDatabaseConfiguration(
            database_name = 'psrc_2005_parcel_baseyear',
            ),
        'estimation_database_configuration': EstimationDatabaseConfiguration(
            database_name = 'psrc_2005_parcel_baseyear_change_20080219',
            ),
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['urbansim_parcel','urbansim', 'opus_core'],
            ),
        'low_memory_mode': False,
        'cache_directory': '/urbansim_cache/psrc_parcel/persons',
        'debuglevel':7,
        'base_year': 2000,
        'years': (2000,2000),
        },
    )

#    del config['estimation_database_configuration']['db_output_database']
    ExpandPersons(config)