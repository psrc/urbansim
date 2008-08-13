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
from opus_core.misc import write_to_text_file
from opus_core.multiple_runs import MultipleRuns

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    years = range(2010, 2021, 10)
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/highest_weight_5637/with_viaduct_5714", 'viad1_')    
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/highest_weight_5637/without_viaduct_5706", 'no_viad1_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/second_weight_5656/with_viaduct_5707", 'viad2_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/second_weight_5656/without_viaduct_5708", 'no_viad2_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/third_weight_5689/with_viaduct_5715", 'viad3_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/third_weight_5689/without_viaduct_5716", 'no_viad3_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/fourth_weight_5662/with_viaduct_5717", 'viad4_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/fourth_weight_5662/without_viaduct_5718", 'no_viad4_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/point_est/with_viaduct_5838", 'viadp_')
    cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/point_est/without_viaduct_5839", 'no_viadp_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5257_highest_weight", 'viad_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5286_highest_weight", 'viadI_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5264_second_weight", 'viad2_')
#    cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5289_second_weight", 'viad2I_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_with_viaduct/run_5272_point_estimates", 'viad3_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5263_highest_weight", 'no_viad_')
#    cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5287_highest_weight", 'no_viadI_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5270_second_weight", 'no_viad2_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5291_second_weight", 'no_viad2I_')
    #cache_directory, prefix = ("/Users/hana/urbansim_cache/psrc/parcel/bm/runs_without_viaduct/run_5273_point_estimates", 'no_viad3_')
    
    for year in years:
        mr = MultipleRuns(cache_directory, package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
        #variable_list = ['urbansim_parcel.zone.number_of_households', 'urbansim_parcel.zone.number_of_jobs']
        variable_list = []
        for group in ['mining', 'constr', 'retail', 'manu', 'wtcu', 'fires', 'gov', 'edu']:
            variable_list = variable_list + ["urbansim_parcel.zone.number_of_jobs_of_sector_group_%s" % group]
        #for sec in range(1,20):
        #    variable_list = variable_list + ["urbansim_parcel.zone.number_of_jobs_of_sector_%s" % sec]
        mr.set_values_from_mr(year, variable_list)
        mr.export_values_from_mr('/Users/hana/bm/psrc_parcel/simulation_results/zones_%s' % year, prefix = prefix)
