#
# Opus software. Copyright (C) 2005-2008 University of Washington
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
from opus_core.storage_factory import StorageFactory
from opus_core.variables.attribute_type import AttributeType
from opus_core.datasets.dataset_pool import DatasetPool
from numpy.random import normal, seed
from numpy import log, exp, sqrt

base_commute_directory = '/Users/hana/urbansim_cache/psrc/parcel/bm/emme2_on_observed_data'
all_emme_dirs = {'with_viaduct1': '/Users/hana/urbansim_cache/psrc/parcel/bm/highest_weight_5637/with_viaduct_5714',
                 'no_viaduct1':   '/Users/hana/urbansim_cache/psrc/parcel/bm/highest_weight_5637/without_viaduct_5706',
                 'with_viaduct2': '/Users/hana/urbansim_cache/psrc/parcel/bm/second_weight_5656/with_viaduct_5707',
                 'no_viaduct2':   '/Users/hana/urbansim_cache/psrc/parcel/bm/second_weight_5656/without_viaduct_5708',
                 'with_viaduct3': '/Users/hana/urbansim_cache/psrc/parcel/bm/third_weight_5689/with_viaduct_5715',
                 'no_viaduct3': '/Users/hana/urbansim_cache/psrc/parcel/bm/third_weight_5689/without_viaduct_5716',
                 'with_viaduct4': '/Users/hana/urbansim_cache/psrc/parcel/bm/fourth_weight_5662/with_viaduct_5717',
                 'no_viaduct4': '/Users/hana/urbansim_cache/psrc/parcel/bm/fourth_weight_5662/without_viaduct_5718',
                 'with_viaduct_pe': '/Users/hana/urbansim_cache/psrc/parcel/bm/point_est/with_viaduct_5838',
                 'no_viaduct_pe': '/Users/hana/urbansim_cache/psrc/parcel/bm/point_est/without_viaduct_5839',
                 'observed_impr_fast_tm': '/Users/hana/urbansim_cache/psrc/parcel/bm/emme2_on_observed_data/improved_fast_tm'
                 }

#which_dirs = 'with_viaduct_pe'
which_dirs = 'no_viaduct_pe'
#which_dirs = 'observed_impr_fast_tm'

year = 2021
random_seed = 1

base_emme_dir = all_emme_dirs[which_dirs]
emme_dirs = os.listdir(base_emme_dir)
emme_dirs = [x for x in emme_dirs if x.startswith('emme_')]

#for i in range(len(emme_dirs)):
#    emme_dirs[i] = os.path.join(base_emme_dir, emme_dirs[i], str(year))

emme_dirs = [ #os.path.join(base_emme_dir, str(2006)), os.path.join(base_emme_dir, str(2011))] #, 
             os.path.join(base_emme_dir, str(2016))]

storage_com = StorageFactory().get_storage('flt_storage', storage_location = base_commute_directory )
pool_com = DatasetPool(storage=storage_com, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
commutes = pool_com.get_dataset('commute_travel_data')

dist = "psrc_parcel.commute_travel_data.subtract_from_travel_data_single_vehicle_to_work_travel_distance"
tt = "psrc_parcel.commute_travel_data.subtract_from_travel_data_am_single_vehicle_to_work_travel_time"

seed(random_seed)

for dir in emme_dirs:
    print dir
    storage = StorageFactory().get_storage('flt_storage', storage_location = dir)
    pool = DatasetPool(storage=storage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
    #pool._add_dataset('commute_travel_data', commutes)
    values = commutes.compute_variables([dist], dataset_pool=pool)
    commutes.delete_one_attribute(dist)
    commutes.add_attribute(name="travel_distance", data=values, metadata=AttributeType.PRIMARY)
    values = commutes.compute_variables([tt], dataset_pool=pool)
    #sim_values = exp(normal(log(values) - 0.41, 0.0181)) # fast run
    sim_values = normal(sqrt(values) - 0.33, 0.465**2)**2
    print values
    print sim_values
    commutes.delete_one_attribute(tt)
    commutes.add_attribute(name="am_pk_travel_time", data=values, metadata=AttributeType.PRIMARY)
    commutes.add_attribute(name="sim_am_pk_travel_time", data=sim_values, metadata=AttributeType.PRIMARY)
    commutes.write_dataset(out_storage=storage)
    commutes.delete_one_attribute(dist)
    commutes.delete_one_attribute(tt)
    
    #tab_storage = StorageFactory().get_storage('tab_storage', storage_location = os.path.join('/Users/hana/bm/psrc_parcel/simulation_results/%s' % which_dirs))
    #commutes.write_dataset(out_storage=tab_storage)                                         