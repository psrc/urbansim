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
from opus_core.multiple_runs import MultipleRuns
from create_file_cache_directories import create_file_cache_directories

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    
    cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/1031/full_runs/run_7486_no_viad_point_est", 'no_viad_lv_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/1031/full_runs/run_7485_with_viad_point_est", 'viad_lv_')

    if os.path.exists(os.path.join(cache_directory, 'cache_directories')):
        os.remove(os.path.join(cache_directory, 'cache_directories'))

    mr = MultipleRuns(cache_directory, prefix='emme_run_lvar_', package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
    commutes = mr.get_datasets_from_multiple_runs(2021, ['commute_travel_data.am_pk_travel_time'], 'commute_travel_data', name_attribute='name')
    mr.simulate_from_normal_and_export('/Users/hana/bm/psrc_parcel/simulation_results/1031/2020', prefix = prefix, variable_prefix='sim_',
                                                    n=100, bias=-0.346, sd=0.118)  # from runs 10/31/08
    mr.export_values_from_mr('/Users/hana/bm/psrc_parcel/simulation_results/1031/2020', prefix = prefix)
