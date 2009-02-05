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
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    years=[2005]
    cache_directory = "/Users/hana/urbansim_cache/psrc_parcel/runs/bm/0127"
    export_directory = '/Users/hana/bm/psrc_parcel/simulation_results/0127'
    
    for year in years:
        if os.path.exists(os.path.join(cache_directory, 'cache_directories')):
            os.remove(os.path.join(cache_directory, 'cache_directories'))
        mr = MultipleRuns(cache_directory, prefix='run_761', package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'])
        variable_list = ['urbansim_parcel.zone.number_of_households', 'urbansim_parcel.zone.number_of_jobs',
                         'number_of_households = large_area.aggregate(urbansim_parcel.zone.number_of_households, intermediates=[faz])',
                         'number_of_jobs = large_area.aggregate(urbansim_parcel.zone.number_of_jobs, intermediates=[faz])']
        for group in ['mining', 'constr', 'retail', 'manu', 'wtcu', 'fires', 'gov', 'edu']:
            variable_list = variable_list + ["urbansim_parcel.zone.number_of_jobs_of_sector_group_%s" % group,
                                             "number_of_jobs_of_sector_group_%s = large_area.aggregate(urbansim_parcel.zone.number_of_jobs_of_sector_group_%s, intermediates=[faz])" % (group,group)]

        mr.set_values_from_mr(year, variable_list)
        dir = '%s/%s' % (export_directory, year)
        if not os.path.exists(dir):
            os.makedirs(dir)
        mr.export_values_from_mr(dir)

            