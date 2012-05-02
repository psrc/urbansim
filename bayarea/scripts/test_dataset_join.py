# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from pandas import read_csv, DataFrame, merge
from numpy import where, allclose
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import Dataset
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.storage_factory import StorageFactory
from opus_core.paths import get_opus_data_path_path
from opus_core.logger import block

data_path = get_opus_data_path_path()
cache_dir = os.path.join(data_path, 'bay_area_parcel/base_year_data')
year = 2010
simulation_state = SimulationState()
simulation_state.set_current_time(year)
SimulationState().set_cache_directory(cache_dir)
attribute_cache = AttributeCache()
dataset_pool = SessionConfiguration(new_instance=True,
                         package_order=['bayarea', 'urbansim_parcel', 
                                        'urbansim', 'opus_core'],
                         in_storage=attribute_cache
                        ).get_dataset_pool()

units = dataset_pool.get_dataset('residential_unit')
bldg = dataset_pool.get_dataset('building')

def to_dataframe(opus_dataset):
    from pandas import DataFrame
    df = {}
    for attr in opus_dataset.get_known_attribute_names():
        df[attr] = opus_dataset[attr]

    df = DataFrame(df)
    return df

units_df = {}
bldg_df = {}
for attr in units.get_known_attribute_names():
    units_df[attr] = units[attr]
for attr in bldg.get_known_attribute_names():
    bldg_df[attr] = bldg[attr]

with block('opus join'):
    results_opus = units.compute_variables('residential_unit.disaggregate(building.building_type_id)',
                            dataset_pool=dataset_pool)

units_df = DataFrame(units_df)
bldg_df = DataFrame(bldg_df)
with block('pandas join without index'):
    units_merged1 = merge(units_df, bldg_df[['building_id', 'building_type_id']], 
          on='building_id', sort=False, how='left')
    results_df1 = units_merged1['building_type_id'] 
    results_df1.fillna(value=-1, inplace=True)

bldg_df.set_index('building_id', inplace=True)
with block('pandas join with index'):
    units_merged2 = units_df.join(bldg_df['building_type_id'], on='building_id', how='left')
    results_df2 = units_merged2['building_type_id'] 
    results_df2.fillna(value=-1, inplace=True)

assert allclose(results_df1, results_df2)
assert allclose(results_opus, results_df2.values)

