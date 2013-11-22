# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.bayesian_melding import BayesianMeldingFromFile
from run_bm import export_quantiles
import run_bm


def export_quant(bm, output_directory, validation_geography):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    propfac = {'faz': {#'pfhh195'=1.0,
                    #'pfj195':3.55,
                    'pfhh':0.38, # run 213
                    'pfj':2.2,
                    'pfp':3.94},
               'large_area': {
                    'pfhh':2, # run 213
                    'pfj':10.4,
                    'pfp':12.1}}
    propfac['zone'] = propfac['faz']
    propfac['large_area'] = propfac['faz']
    pf = propfac[validation_geography]
    export_quantiles(bm, output_directory, #years=[2020, 2025, 2030, 2035, 2040], 
                     years=[2040],
                     validation_geography=validation_geography,
                     propfac_hh=pf['pfhh'], propfac_jobs=pf['pfj'], propfac_pop=pf['pfp'])
    
if __name__ == "__main__":
    run = 231
    #run = 213
    run = 'MR'
    #cache_directory = "/Users/hana/psrc3656/workspace/data/psrc_parcel/runs"
    cache_directory = "/Users/hana/workspace/data/psrc_parcel/runs"
    run_name_prefix = "run_%sref" % run
    run_name_prefix = "run_%s" % run
    #validation_geography = 'large_area'
    validation_geography = 'faz'
    #validation_geography = 'zone'
    #pardir = "/Users/hana/psrc3656/workspace/data/psrc_parcel/runs/bmanal/run213_val2010_%s" % validation_geography
    pardir = "/Users/hana/psrc3656/workspace/data/psrc_parcel/runs/bmanal/runMR_val2010_%s" % validation_geography
    #output_directory = "/Users/hana/psrc3656/workspace/data/psrc_parcel/runs/bmanal/paper_run%s_quantiles_%s" % (run, validation_geography)
    output_directory = "/Users/hana/psrc3656/workspace/data/psrc_parcel/runs/bmanal/run%s_quantiles_%s" % (run, validation_geography)

    
    bmf = BayesianMeldingFromFile(pardir + "/bm_parameters", package_order=['urbansim_parcel', 'urbansim', 'core'],
                                  cache_file_location=cache_directory, prefix=run_name_prefix, overwrite_cache_directories_file=True,
                                  transformation_pair = ("sqrt", "**2"))
    #bmf.year = 2020 # move it by ten years if refinement run is used (refined 10 years after base year)
    #bmf.base_year = 2010
    
    #export_quantiles(bmf, output_directory, years=[2010, 2015, 2020, 2025, 2030, 2035, 2040], propfac_hh=0.95, propfac_jobs=3.5)
    #export_quantiles(bmf, output_directory, years=[2040], propfac_hh=0.95, propfac_jobs=3.5)
    export_quant(bmf, output_directory, validation_geography)
    
    