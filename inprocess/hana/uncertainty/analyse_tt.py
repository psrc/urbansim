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

from opus_core.multiple_runs import MultipleRuns
from create_file_cache_directories import create_file_cache_directories

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/highest_weight_5637/with_viaduct_5714/emme_run_1_2008_03_02_20_38", 'viad1_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/highest_weight_5637/without_viaduct_5706/emme_run_1_2008_03_01_20_38", 'no_viad1_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/second_weight_5656/with_viaduct_5707/emme_run_1_2008_03_01_20_26", 'viad2_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/second_weight_5656/without_viaduct_5708/emme_run_1_2008_03_01_20_30", 'no_viad2_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/third_weight_5689/with_viaduct_5715/emme_run_1_2008_03_02_19_50", 'viad3_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/third_weight_5689/without_viaduct_5716/emme_run_1_2008_03_02_19_52", 'no_viad3_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/fourth_weight_5662/with_viaduct_5717/emme_run_1_2008_03_02_20_16", 'viad4_')
    cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/fourth_weight_5662/without_viaduct_5718/emme_run_1_2008_03_02_20_19", 'no_viad4_')

    create_file_cache_directories(cache_directory, prefix='emme_')

    mr = MultipleRuns(cache_directory, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
    commutes = mr.get_datasets_from_multiple_runs(2021, ['commute_travel_data.sim_am_pk_travel_time', 'commute_travel_data.am_pk_travel_time'], 'commute_travel_data', name_attribute='name')
    mr.export_values_from_mr('/Users/hana/bm/psrc_parcel/simulation_results/tt_2020', prefix = prefix)
