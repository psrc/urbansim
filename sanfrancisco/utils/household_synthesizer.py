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

import os
from numpy import float32, float64, searchsorted, array, zeros, where
from numpy.random import random
from opus_core.misc import ncumsum
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
#from opus_core.resources import Resources
#from opus_core.services.run_server.misc import create_datasets_from_flt
#from sandbox.progress import ProgressMeter

class HouseholdSynthesizer(object):
    """This class assign household from zone (taz) to building. It may only work for the purpose of sanfrancisco project"""
    def __init__(self, config):
        ss = SimulationState(new_instance=True)
        ss.set_current_time(config['base_year'])
        ss.set_cache_directory(config['cache_directory'])

        SessionConfiguration(new_instance=True,
                             package_order=config['dataset_pool_configuration'].package_order,
                             package_order_exceptions=config['dataset_pool_configuration'].package_order_exceptions,
                             in_storage=AttributeCache())
        
        db_config = DatabaseServerConfiguration(
               host_name=config['output_configuration'].host_name,
               user_name=config['output_configuration'].user_name,
               password=config['output_configuration'].password                                               
        )
        db_server = DatabaseServer(db_config)
        db = db_server.get_database(config['output_configuration'].database_name)
        if 'output_configuration' in config:
            out_storage = StorageFactory().get_storage(
               'sql_storage', 
               storage_location = db)
        else:
            output_cache = os.path.join(config['cache_directory'], str(config['base_year']+1))
            out_storage = StorageFactory().get_storage('flt_storage', storage_location=output_cache)

#        attribute_cache = AttributeCache()
#        
#        if not os.path.exists(os.path.join(config['cache_directory'], str(config['base_year']))):
#            #raise RuntimeError, "datasets uncached; run prepare_estimation_data.py first"
#            CacheMysqlData().run(config, unroll_gridcells=False)
#
#        datasets = create_datasets_from_flt(config['datasets_to_preload'], 
#                                            "urbansim",
#                                            additional_arguments={'in_storage':attribute_cache})
#        sc.merge(datasets)

        dataset_pool = SessionConfiguration().get_dataset_pool()
        households = dataset_pool.get_dataset("household")
        buildings = dataset_pool.get_dataset("building")
        zones = dataset_pool.get_dataset("zone")
        zone_ids = zones.get_id_attribute()
        capacity_attribute_name = "residential_units"  #_of_use_id_%s" % id
        capacity_variable_name = "%s=sanfrancisco.zone.aggregate_%s_from_building" % \
                                 (capacity_attribute_name, capacity_attribute_name)
        buildings.compute_variables("sanfrancisco.building.zone_id", dataset_pool=dataset_pool)
        zones.compute_variables(capacity_variable_name, dataset_pool=dataset_pool)

        building_zone_id = buildings.get_attribute('zone_id')
        
#        is_household_unplace = datasets['household'].get_attribute("building_id") <= 0
        is_household_unplaced = 1 #all households are unplaced
        household_building_id = zeros(households.size())-1 #datasets['household'].get_attribute("building_id")
        
        for zone_id in zone_ids:
            capacity = zones.get_attribute_by_id(capacity_attribute_name, zone_id)
            is_household_in_this_zone = (households.get_attribute('zone_id') == zone_id)
            is_unplaced_household_in_this_zone = is_household_in_this_zone * is_household_unplaced
            is_building_in_this_zone = (building_zone_id == zone_id)
#            if not is_household_in_this_zone.sum() <= capacity:
            if capacity == 0 or is_household_in_this_zone.sum()==0:
                print "WARNING: zone %s has %s households but only %s units" % (zone_id, is_household_in_this_zone.sum(), capacity)
                continue
                        
            prob = buildings.get_attribute(capacity_attribute_name) * is_building_in_this_zone / array(capacity, dtype=float64)

            r = random(sum(is_unplaced_household_in_this_zone))
            prob_cumsum = ncumsum(prob)
            index_to_bldg = searchsorted(prob_cumsum, r)

            household_building_id[where(is_unplaced_household_in_this_zone)] = buildings.get_attribute_by_index('building_id', index_to_bldg)

#        import pdb;pdb.set_trace()
        households.set_values_of_one_attribute('building_id', household_building_id)
        households.write_dataset(out_table_name='households', out_storage=out_storage)
  
if __name__ == '__main__':
    from caching_configuration import CachingConfiguration
    config = CachingConfiguration()
#    del config['output_configuration']['db_output_database']
    HouseholdSynthesizer(config)
