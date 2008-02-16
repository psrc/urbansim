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
all_emme_dirs = {'with_viaduct': {'/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5264_second_weight':
                                  ['emme_run_1_2008_02_14_12_22', 'emme_run_2_2008_02_14_14_15', 'emme_run_3_2008_02_14_16_01',
                                   'emme_run_4_2008_02_14_17_46', 'emme_run_5_2008_02_14_19_37', 'emme_run_6_2008_02_14_21_26',
                                   'emme_run_7_2008_02_14_23_06', 'emme_run_8_2008_02_15_00_45', 'emme_run_9_2008_02_15_02_24', 
                                   'emme_run_10_2008_02_15_04_02', 'emme_run_11_2008_02_15_05_44', 'emme_run_12_2008_02_15_07_23',
                                   'emme_run_13_2008_02_15_09_02'
                                   ]
                                  },
             'without_viaduct': {
                            '/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5263_highest_weight':
                                [
                                 'emme_run_1_2008_02_15_13_00', 'emme_run_1_2008_02_15_13_15'
                                 ]
                                 }
             }
which_dirs = 'without_viaduct'

base_emme_dir, emme_dirs = all_emme_dirs[which_dirs].items()[0]
for i in range(len(emme_dirs)):
    emme_dirs[i] = os.path.join(base_emme_dir, emme_dirs[i], str(2021))

storage_com = StorageFactory().get_storage('flt_storage', storage_location = base_commute_directory )
pool_com = DatasetPool(storage=storage_com, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
commutes = pool_com.get_dataset('commute_travel_data')

dist = "psrc_parcel.commute_travel_data.subtract_from_travel_data_single_vehicle_to_work_travel_distance"
tt = "psrc_parcel.commute_travel_data.subtract_from_travel_data_am_single_vehicle_to_work_travel_time"

for dir in emme_dirs:
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