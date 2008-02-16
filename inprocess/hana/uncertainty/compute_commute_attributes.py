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


directory = '/Users/hana/urbansim_cache/psrc/parcel/bm/emme2_on_observed_data/emme_run_1_2008_02_11_18_55/2006'
#directory = '/Users/hana/urbansim_cache/psrc/parcel/bm/emme2_on_observed_data/full_tm/emme_run_1_2008_02_11_18_26/2006'
export_directory = '/Users/hana/bm/psrc_parcel/simulation_results/fast_run/'
export_file = "commute_travel_data"
from opus_core.storage_factory import StorageFactory
from opus_core.variables.attribute_type import AttributeType
from opus_core.datasets.dataset_pool import DatasetPool

storage = StorageFactory().get_storage('flt_storage',storage_location = directory )
pool = DatasetPool(storage=storage, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'])
commutes = pool.get_dataset('commute_travel_data')
dist = "psrc_parcel.commute_travel_data.subtract_from_travel_data_single_vehicle_to_work_travel_distance"
values = commutes.compute_variables([dist], dataset_pool=pool)
commutes.delete_one_attribute(dist)
commutes.add_attribute(name="travel_distance", data=values, metadata=AttributeType.PRIMARY)

var = "psrc_parcel.commute_travel_data.subtract_from_travel_data_am_single_vehicle_to_work_travel_time"
values = commutes.compute_variables([var], dataset_pool=pool)

commutes.delete_one_attribute(var)
commutes.add_attribute(name="am_pk_travel_time", data=values, metadata=AttributeType.PRIMARY)
out_storage = StorageFactory().get_storage('tab_storage',storage_location = export_directory )
commutes.write_dataset(out_storage=out_storage, out_table_name=export_file)