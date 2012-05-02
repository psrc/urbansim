# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from pandas import read_csv, DataFrame, merge
from numpy import where, allclose, round
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import Dataset
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory
from opus_core.paths import get_opus_data_path_path
from opus_core.logger import block
import cPickle, pickle

pickle_filename = '/workspace/price_equilibration/dump_cached.pickle'
pickle_data = pickle.load(open(pickle_filename, 'rb'))

pickle_filename = '/workspace/price_equilibration/submarket_id.pickle'
submkt_data = pickle.load(open(pickle_filename, 'rb'))

data_path = get_opus_data_path_path()
cache_dir = os.path.join(data_path, 'bay_area_zone/base_year_data.original')
year = 2000
simulation_state = SimulationState()
simulation_state.set_current_time(year)
SimulationState().set_cache_directory(cache_dir)
attribute_cache = AttributeCache()
dataset_pool = SessionConfiguration(new_instance=True,
                         package_order=['bayarea', 'urbansim_parcel', 
                                        'urbansim', 'opus_core'],
                         in_storage=attribute_cache
                        ).get_dataset_pool()

hh = dataset_pool.get_dataset('household')
proportion = float(pickle_data['Xpagents'].size) / hh.size()

hh_cnty = hh.compute_variables('county=household.disaggregate(zone.county, intermediates=[building])')
hh_bldg_type = hh.compute_variables('building_type_id=household.disaggregate(building.building_type_id)')
hh_df = hh.to_dataframe()
import pdb; pdb.set_trace()
hh_cnty = round(hh_df.groupby(['county']).size() * proportion)
hh_cnty_bldg_type = round(hh_df.groupby(['county', 'building_type_id']).size()* proportion)
targets = {}
targets['target_by_county'] = {'county': hh_cnty.index.values,
                               'target': hh_cnty.values}

targets['target_by_county_building_type'] = \
    {'county': hh_cnty_bldg_type.index.get_level_values('county'),
     'building_type_id': hh_cnty_bldg_type.index.get_level_values('building_type_id'),
     'target': hh_cnty_bldg_type.values}
zones = dataset_pool.get_dataset('zone')
id_index = zones.get_id_index(submkt_data['zone_id'])
submkt_data['county'] = zones['county'][id_index]
pickle_filename = '/workspace/price_equilibration/county.pickle'
pickle_file = file(pickle_filename, 'wb')
pickle.dump(submkt_data, file=pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

pickle_filename = '/workspace/price_equilibration/targets.pickle'
pickle_file = file(pickle_filename, 'wb')
pickle.dump(targets, file=pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

