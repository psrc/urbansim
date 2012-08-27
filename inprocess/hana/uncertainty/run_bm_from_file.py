# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.bayesian_melding import BayesianMeldingFromFile
from run_bm import export_quantiles

if __name__ == "__main__":
    run = 136
    cache_directory = "/Users/hana/workspace/data/psrc_parcel/runs"
    run_name_prefix = "run_%s" % run
    pardir = "/Users/hana/workspace/data/psrc_parcel/runs/bmanal/run129_val2010"
    output_directory = "/Users/hana/workspace/data/psrc_parcel/runs/bmanal/run%s" % run
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    bmf = BayesianMeldingFromFile(pardir + "/bm_parameters", package_order=['urbansim_parcel', 'urbansim', 'core'],
                                  cache_file_location=cache_directory, prefix=run_name_prefix, overwrite_cache_directories_file=True,
                                  transformation_pair = ("sqrt", "**2"))
    export_quantiles(bmf, output_directory, years=[2010, 2015, 2020, 2025, 2030, 2035, 2040], propfac_hh=0.95, propfac_jobs=3.5)
    #export_quantiles(bmf, output_directory, years=[2040], propfac_hh=0.95, propfac_jobs=3.5)
    