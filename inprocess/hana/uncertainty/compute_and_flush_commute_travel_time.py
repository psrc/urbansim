#
# Opus software. Copyright (C) 1998-2007 University of Washington
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
from numpy.random import normal
from numpy import log, exp

base_commute_directory = '/Users/hana/urbansim_cache/psrc/parcel/bm/emme2_on_observed_data'
all_emme_dirs = {'with_viaduct': '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5257_highest_weight',
                 'with_viaduct2': '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5264_second_weight',
                 'with_viaduct3': '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5272_point_estimates',
                 'without_viaduct': '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5263_highest_weight',
                 'without_viaduct2': '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5270_second_weight',
                 'without_viaduct3': '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5273_point_estimates'
                 }

which_dirs = 'without_viaduct3'

base_emme_dir = all_emme_dirs[which_dirs]
emme_dirs = os.listdir(base_emme_dir)
emme_dirs = [x for x in emme_dirs if x.startswith('emme_')]

for i in range(len(emme_dirs)):
    emme_dirs[i] = os.path.join(base_emme_dir, emme_dirs[i], str(2021))

storage_com = StorageFactory().get_storage('flt_storage', storage_location = base_commute_directory )
pool_com = DatasetPool(storage=storage_com, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
commutes = pool_com.get_dataset('commute_travel_data')

dist = "psrc_parcel.commute_travel_data.subtract_from_travel_data_single_vehicle_to_work_travel_distance"
tt = "psrc_parcel.commute_travel_data.subtract_from_travel_data_am_single_vehicle_to_work_travel_time"

for dir in emme_dirs:
    print dir
    storage = StorageFactory().get_storage('flt_storage', storage_location = dir)
    pool = DatasetPool(storage=storage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
    #pool._add_dataset('commute_travel_data', commutes)
    values = commutes.compute_variables([dist], dataset_pool=pool)
    commutes.delete_one_attribute(dist)
    commutes.add_attribute(name="travel_distance", data=values, metadata=AttributeType.PRIMARY)
    values = commutes.compute_variables([tt], dataset_pool=pool)
    sim_values = exp(normal(log(values) - 0.41, 0.0181))
    commutes.delete_one_attribute(tt)
    commutes.add_attribute(name="am_pk_travel_time", data=values, metadata=AttributeType.PRIMARY)
    commutes.add_attribute(name="sim_am_pk_travel_time", data=sim_values, metadata=AttributeType.PRIMARY)
    commutes.write_dataset(out_storage=storage)
    commutes.delete_one_attribute(dist)
    commutes.delete_one_attribute(tt)