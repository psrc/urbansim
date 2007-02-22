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
from numarray import Float32, Float64, searchsorted, array, zeros, where
from numarray.random_array import random
from opus_core.misc import ncumsum
from opus_core.simulation_state import SimulationState
from urbansim.session_configuration import SessionConfiguration
from opus_core.services.run_server.scenario_database import ScenarioDatabase
from opus_core.store.opus_database import OpusDatabase
from opus_core.attribute_cache import AttributeCache
from opus_core.resources import Resources
from opus_core.services.run_server.misc import create_datasets_from_flt
#from sandbox.progress import ProgressMeter
from opus_core.services.run_server.storage_creator import StorageCreator
from urbansim.model_coordinators.cache_mysql_data import CacheMysqlData

class HouseholdSynthesizer(object):
    """This class assign household from zone (taz) to parcels. It may not work for the purpose of san francisco project"""
    def __init__(self, config):
        input_db = ScenarioDatabase(host=config['db_host_name'],
                                    user=config['db_user_name'],
                                    password=config['db_password'],
                                    database=config['input_configuration']['db_input_database'])
        sc = SessionConfiguration({'in_storage_location':input_db}).get_session_configuration()
        in_con = sc['in_storage_location']
        
        if 'output_configuration' in config and 'db_output_database' in config['output_configuration']:
            out_con = OpusDatabase(host=config['db_host_name'],
                                   user=config['db_user_name'],
                                   password=config['db_password'],
                                   database=config['output_configuration']['db_output_database'])
            out_storage = StorageCreator().build_storage(
                                          location=out_con, 
                                          type="mysql")
        else:
            out_storage = StorageCreator().build_storage(
                                      location=os.path.join(config['cache_directory'], str(config['base_year']+1)), 
                                      type="flt")

#        sc.set_exceptions_in_storage_type({"employment_sector":"mysql"})
#        sc.set_exceptions_in_storage_location({"employment_sector":input_db})
                
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(config['cache_directory'])
        simulation_state.set_current_time(config['base_year'])
        attribute_cache = AttributeCache()
        
        if not os.path.exists(os.path.join(config['cache_directory'], str(config['base_year']))):
            #raise RuntimeError, "datasets uncached; run prepare_estimation_data.py first"
            CacheMysqlData().run(config, unroll_gridcells=False)

        datasets = create_datasets_from_flt(config['datasets_to_preload'], 
                                            "urbansim",
                                            additional_arguments={'in_storage':attribute_cache})
        sc.merge(datasets)

        zone_ids = sc.pull("zone").get_id_attribute()
        capacity_attribute_name = "residential_units"  #_of_use_id_%s" % id
        capacity_variable_name = "zone:opus_core.func.aggregate(building.%s, sum, [parcel]) as %s" % \
                                 (capacity_attribute_name, capacity_attribute_name)
        datasets['zone'].compute_variables(capacity_variable_name)
        building_zone_id = datasets['building'].get_join_data(datasets['parcel'], 'zone_id')
        
#        is_household_unplace = datasets['household'].get_attribute("building_id") <= 0
        is_household_unplace = 1
        building_ids = zeros(datasets['household'].size())-1 #datasets['household'].get_attribute("building_id")
        
        for zone_id in zone_ids:
            capacity = datasets['zone'].get_attribute_by_id(capacity_attribute_name, zone_id)
            is_household_in_this_zone = (datasets['household'].get_attribute('zone_id') == zone_id)
            is_building_in_this_zone = (building_zone_id == zone_id)
#            if not is_household_in_this_zone.sum() <= capacity:
            if capacity == 0:
                print "WARNING: zone %s has %s households but only %s units" % (zone_id, is_household_in_this_zone.sum(), capacity)
                continue
            
            prob = datasets['building'].get_attribute(capacity_attribute_name) * is_building_in_this_zone / array(capacity, type=Float64)

            r = random(sum(is_household_in_this_zone * is_household_unplace))
            prob_cumsum = ncumsum(prob)
            index_to_bldg = searchsorted(prob_cumsum, r)

            building_ids[where(is_household_in_this_zone * is_household_unplace)] = datasets['building'].get_attribute_by_index('building_id', index_to_bldg)

#        import pdb;pdb.set_trace()
        datasets['household'].set_values_of_one_attribute('building_id', building_ids)
        datasets['household'].write_dataset(out_table_name='households', out_storage=out_storage)
  
if __name__ == '__main__':
    from synthesizer_config import config
#    del config['output_configuration']['db_output_database']
    HouseholdSynthesizer(config)
