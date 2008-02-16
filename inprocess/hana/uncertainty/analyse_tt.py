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

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    
    #cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5264_second_weight/emme_run_1_2008_02_14_12_22"
    cache_directory = "/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5263_highest_weight/emme_run_1_2008_02_15_13_00"
    #prefix = 'viad_'
    prefix = 'no_viad_'
    
    mr = MultipleRuns(cache_directory, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
    commutes = mr.get_datasets_from_multiple_runs(2021, ['commute_travel_data.sim_am_pk_travel_time', 'commute_travel_data.am_pk_travel_time'], 'commute_travel_data', name_attribute='name')
    mr.export_values_from_mr('/Users/hana/bm/psrc_parcel/simulation_results/tt_2020', prefix = prefix)