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
from opus_core.misc import write_to_text_file
from opus_core.multiple_runs import MultipleRuns

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5257_highest_weight/emme_run_1_2008_02_15_14_54", 'viad_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5264_second_weight/emme_run_1_2008_02_14_12_22", 'viad2_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5272_point_estimates/emme_run_1_2008_02_20_10_05", 'viad3_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5263_highest_weight/emme_run_1_2008_02_15_13_00", 'no_viad_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5270_second_weight/emme_run_1_2008_02_21_18_07", 'no_viad2_')
    cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5273_point_estimates/emme_run_1_2008_02_20_10_10", 'no_viad3_')

    base_emme_dir = os.path.join(os.path.split(cache_directory)[0:-1])[0]
    emme_dirs = os.listdir(base_emme_dir)
    emme_dirs = [x for x in emme_dirs if x.startswith('emme_')]

    for i in range(len(emme_dirs)):
        emme_dirs[i] = os.path.join(base_emme_dir, emme_dirs[i])
        
    write_to_text_file(os.path.join(cache_directory, 'cache_directories'), emme_dirs)

    mr = MultipleRuns(cache_directory, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
    commutes = mr.get_datasets_from_multiple_runs(2021, ['commute_travel_data.sim_am_pk_travel_time', 'commute_travel_data.am_pk_travel_time'], 'commute_travel_data', name_attribute='name')
    mr.export_values_from_mr('/Users/hana/bm/psrc_parcel/simulation_results/tt_2020', prefix = prefix)