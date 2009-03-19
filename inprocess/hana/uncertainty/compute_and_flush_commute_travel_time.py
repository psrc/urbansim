# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os
from opus_core.storage_factory import StorageFactory
from opus_core.variables.attribute_type import AttributeType
from opus_core.datasets.dataset_pool import DatasetPool

base_commute_directory = '/Users/hana/urbansim_cache/psrc/parcel/bm/emme2_on_observed_data'
all_emme_dirs = {'0818/with_viaduct1': ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_5_paris_viad_highest_weight',False),
                 '0818/no_viaduct1':   ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_4_paris_no_viad_highest_weight',False),
                 '0818/with_viaduct1_2020': ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_5_paris_viad_highest_weight/emme_run_point_est',True),
                 '0818/with_viaduct1_2010': ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_5_paris_viad_highest_weight',True),
                 '0818/no_viaduct1_2020': ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_4_paris_no_viad_highest_weight/emme_run_point_est',True),
                 '0818/no_viaduct1_2010':   ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_4_paris_no_viad_highest_weight',True),
                 '0818/with_viaduct1_2000': ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_5_paris_viad_highest_weight',True),
                 'with_viaduct2': '/Users/hana/urbansim_cache/psrc/parcel/bm/second_weight_5656/with_viaduct_5707',
                 'no_viaduct2':   '/Users/hana/urbansim_cache/psrc/parcel/bm/second_weight_5656/without_viaduct_5708',
                 'with_viaduct3': '/Users/hana/urbansim_cache/psrc/parcel/bm/third_weight_5689/with_viaduct_5715',
                 'no_viaduct3': '/Users/hana/urbansim_cache/psrc/parcel/bm/third_weight_5689/without_viaduct_5716',
                 'with_viaduct4': '/Users/hana/urbansim_cache/psrc/parcel/bm/fourth_weight_5662/with_viaduct_5717',
                 'no_viaduct4': '/Users/hana/urbansim_cache/psrc/parcel/bm/fourth_weight_5662/without_viaduct_5718',
                 '0818/with_viaduct_pe': ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_3_paris_viad_point_est', False),
                 '0818/no_viaduct_pe':   ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/full_runs/run_1_paris_no_viad_point_est', False),
                 '0818/observed': ('/Users/hana/urbansim_cache/psrc/parcel/bm/0818/observed_with_point_est_sim', True),
                 '0127/with_viaduct_pe': ('/Users/hana/urbansim_cache/psrc_parcel/runs/bm/0127/full_runs/wv_run_7650_pe', True),
                 '0127/no_viaduct_pe':   ('/Users/hana/urbansim_cache/psrc_parcel/runs/bm/0127/full_runs/nov_run_7585_pe', True),
                 '1031/observed': ('/Users/hana/urbansim_cache/psrc/parcel/bm/1031/observed', False),
                 }

#which_dirs = '0127/with_viaduct_pe'
which_dirs = '0127/no_viaduct_pe'
#which_dirs = '0818/with_viaduct1'
#which_dirs = '0818/no_viaduct1'
#which_dirs = '1031/observed'
#which_dirs = '0818/with_viaduct1_2010'
#which_dirs = '0818/with_viaduct1_2000'
#which_dirs = '0818/no_viaduct1_2010'
#which_dirs = '0818/with_viaduct1_2020'
#which_dirs = '0818/no_viaduct1_2020'

years = [2006, 2011, 2016]

base_emme_dir, is_cache = all_emme_dirs[which_dirs]

if not is_cache:
    emme_dirs = os.listdir(base_emme_dir)
    emme_dirs = [x for x in emme_dirs if x.startswith('emme_')]

    full_emme_dirs = []
    for i in range(len(emme_dirs)):
        for year in years:
            full_emme_dirs.append(os.path.join(base_emme_dir, emme_dirs[i], str(year)))
    emme_dirs = full_emme_dirs
else:
    emme_dirs = []
    for year in years:
        emme_dirs.append(os.path.join(base_emme_dir, str(year)))

write_dirs = []
for year in years:
    write_dirs.append(os.path.join(which_dirs, str(year)))
    
storage_com = StorageFactory().get_storage('tab_storage', storage_location = base_commute_directory )
pool_com = DatasetPool(storage=storage_com, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
commutes = pool_com.get_dataset('commute_travel_data')

storage_base = StorageFactory().get_storage('flt_storage', storage_location = os.path.join(base_emme_dir, str(year-1)))
pool_base = DatasetPool(storage=storage_base, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
try:
    zones = pool_base.get_dataset('zone')
except:
    pass

dist = "psrc_parcel.commute_travel_data.subtract_from_travel_data_single_vehicle_to_work_travel_distance"
tt = "psrc_parcel.commute_travel_data.subtract_from_travel_data_am_single_vehicle_to_work_travel_time"

for idir in range(len(emme_dirs)):
    dir = emme_dirs[idir]
    print dir
    storage = StorageFactory().get_storage('flt_storage', storage_location = dir)
    pool = DatasetPool(storage=storage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
    #pool._add_dataset('commute_travel_data', commutes)
    values = commutes.compute_variables([dist], dataset_pool=pool)
    commutes.delete_one_attribute(dist)
    commutes.add_attribute(name="travel_distance", data=values, metadata=AttributeType.PRIMARY)
    values = commutes.compute_variables([tt], dataset_pool=pool)
    print values
    commutes.delete_one_attribute(tt)
    commutes.add_attribute(name="am_pk_travel_time", data=values, metadata=AttributeType.PRIMARY)
    commutes.write_dataset(out_storage=storage)
    commutes.delete_one_attribute(dist)
    commutes.delete_one_attribute(tt)
    try:
        pool.get_dataset('zone')
    except:
        try:
            zones.write_dataset(out_storage=storage)
        except:
            pass
    if is_cache:
        tab_storage = StorageFactory().get_storage('tab_storage', storage_location = '/Users/hana/bm/psrc_parcel/simulation_results/%s' % write_dirs[idir])
        commutes.write_dataset(out_storage=tab_storage)
        print 'Dataset %s writen into %s.' %(commutes.get_dataset_name(), tab_storage.get_storage_location())
