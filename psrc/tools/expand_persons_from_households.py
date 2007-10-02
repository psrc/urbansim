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

from opus_core.configuration import Configuration
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration

from numpy import array, arange

from urbansim.model_coordinators.cache_scenario_database import CacheScenarioDatabase

from psrc.datasets.person_dataset import PersonDataset

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration


class ExpandPersons(object):
    """This class creates a persons table from households by inserting 1 record for each worker in a household"""
    ## TODO: Is this class in use?
    def __init__(self, config):
        if 'output_configuration' in config:
            config = AbstractUrbansimConfiguration()
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

        household_ids = SessionConfiguration().get_dataset_from_pool("household").get_id_attribute()
        workers = SessionConfiguration().get_dataset_from_pool("household").get_attribute("workers")
        
        hh_ids = []
        member_ids = []
        job_ids = []

        i = 0
        for household_id in household_ids:
            if workers[i] > 0:
                hh_ids += [household_id] * workers[i]
                member_ids += range(1, workers[i]+1)
                job_ids += [-1] * workers[i]
            i = i+1

        in_storage = StorageFactory().get_storage('dict_storage')
        
        persons_table_name = 'persons'
        in_storage.write_table(
                table_name=persons_table_name,
                table_data={
                    'person_id':arange(len(hh_ids))+1,
                    'household_id':array(hh_ids),
                    'member_id':array(member_ids),
                    'job_id':array(job_ids),
                    },
            )

        persons = PersonDataset(in_storage=in_storage, in_table_name=persons_table_name)

        persons.write_dataset(out_storage=out_storage, out_table_name=persons_table_name)


from opus_core.configurations.database_configuration import DatabaseConfiguration



if __name__ == '__main__':
    config = Configuration({
        'input_configuration': DatabaseConfiguration(
            host_name     = "trondheim.cs.washington.edu",
            user_name     = os.environ['MYSQLUSERNAME'],
            password      = os.environ['MYSQLPASSWORD'],
            database_name = 'PSRC_2000_baseyear',
            ),
        'output_configuration': DatabaseConfiguration(
            host_name     = 'trondheim.cs.washington.edu', #os.environ['MYSQLHOSTNAME'],
            user_name     = os.environ['MYSQLUSERNAME'],
            password      = os.environ['MYSQLPASSWORD'],
            database_name = 'GSPSRC_2000_baseyear_change_20060902',
            ),
        'dataset_pool_configuration': DatasetPoolConfiguration(
            package_order=['urbansim', 'opus_core'],
            package_order_exceptions={},
            ),
        'low_memory_mode': False,
        'cache_directory': '/urbansim_cache/psrc',
        'debuglevel':7,
        'base_year': 2000,
        'years': (2000,2000),
        },
    )

#    del config['output_configuration']['db_output_database']
    ExpandPersons(config)