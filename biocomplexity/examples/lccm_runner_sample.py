# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

""" This module is a sample configuration of the Land Change Cover Model (LCCM).
It is intended to be modified to specify parameters to the model, or to
make basic modifications to its behavior."""


#############################################################################
# Configuration settings
#############################################################################

"""
how to start a lccm run?

1). need urbansim cache for the run.
    - create a new folder in your local drive: c:\\urbansim_cache
    - use windows explorer go to this address: \\ukiah\lccm_urbansim_cache
    - copy the 2006_02_14__11_43 folder to c:\\urbansim_cache

2). go to biocomplexity.examples.lccm_runner_sample, fill in the
configurations for the run (Notice that if you use the same folder name
in step 1, it is good to go now).

3). execute the file lccm_runner_sample in eclipse to run the
simulation.
"""


class LccmConfiguration(object):

    # 1. Years - the years for which the model is run. The first year
    #   in the list is taken to be the base year; the model runs for
    #   each subsequent year.
#    years = [2005, 2008, 2011, 2014, 2017, 2020, 2023, 2026, 2029, 2032, 2035, 2038]
#    years = [2008, 2011]
    years = [2005]

#    years = [2003, 2007, 2011, 2015, 2019, 2023, 2027]
#    years = [1999, 2003, 2007]
    
    # 2. Base directory - the input directory that contains all the input flt data
    base_directory = r"C:\eclipse\opus\src\biocomplexity\data\LCCM_4County_converted\2002"
    
#    base_directory = r"C:\eclipse\opus\src\biocomplexity\data\LCCM_4County\1999"
#    base_directory = r"C:\eclipse\opus\src\biocomplexity\data\LCCM_4County_converted\1999"
#    base_directory = r"C:\eclipse\opus\src\biocomplexity\data\small_test_set_opus\1995"

    # 3. Urbansim output data - cache directory
    #   (notice that this is the folder that contains all years folder)
    urbansim_cache_directory = r"C:\eclipse\opus\src\urbansim_cache\data\2009_10_15__13_44"
    
#    urbansim_cache_directory = r"C:\eclipse\opus\src\urbansim_cache\data\2006_02_14__11_43"
#    urbansim_cache_directory = r"C:\eclipse\opus\src\urbansim_cache\data\2006_02_17__16_23"

    # 4. specification and cofficients use:
    #    look under biocomplexity.data folder for the coefficients and specification
    #    fill in the names of the ones that shuold be used for the simulation
    # current (3 July 2006) set to choose from:
    
#    coefficients = "lccm_coefficients_all99to02_9599_respec"
#    specification = "lccm_specification_all99to02_9599_respec"

#    coefficients = "lccm_coefficients_all99to02_nosmall_v3_from_allspecc"
#    specification = "lccm_specification_all99to02_nosmall_v3_from_allspecc"

    coefficients = "lccm_coefficients_all95to99_CAOsc"
    specification = "lccm_specification_all95to99_CAOsc"

    # 4a. coefficients store the parameter estimate - pick one:
#    coefficients = "lccm_coefficients_all99to02v2c"
#    coefficients = "lccm_coefficients_all99to02v5_from_minspecc"
#    coefficients = "lccm_coefficients_all99to02v4_use4predictionsc"
#    coefficients = "lccm_coefficients_all99to02v6_from_allspecc"

#    coefficients = "land_cover_change_model_coefficients_small_test"
#    coefficients = "land_cover_change_model_coefficients_a91_95corrected"
#    coefficients = "land_cover_change_model_coefficients_a95_99corrected"
    
    # 4b. specification stores the variables to use - pick one:
#    specification = "lccm_specification_all99to02v2c"
#    specification = "lccm_specification_all99to02v5_from_minspecc"
#    specification = "lccm_specification_all99to02v4_use4predictionsc"
#    specification = "lccm_specification_all99to02v6_from_allspecc"
    
#    specification = "land_cover_change_model_specification_small_test"
#    specification = "land_cover_change_model_specification_a91_95corrected"
#    specification = "land_cover_change_model_specification_a95_99corrected"
    
    # 5. Output directory - the directory that contains the output flt files
#    output_directory = r"C:\mmarsik\lccm\data\output\lc9902_9599_respec"
#    output_directory = r"C:\mmarsik\lccm\data\output\lc2038_from_9195"
#    output_directory = r"C:\mmarsik\lccm\data\output\lc2038_from_9599"
#    output_directory = r"C:\mmarsik\lccm\data\output\a9902c_v5"
#    output_directory = r"C:\mmarsik\lccm\data\output\a9902c_v4"
#    output_directory = r"C:\mmarsik\lccm\data\output\a9902c_v6"
#    output_directory = r"C:\temp\test"
#    output_directory = r"C:\mmarsik\lccm\data\output\a9902c_nosmall_v3"
    output_directory = r"C:\mmarsik\lccm\data\output\a9599c_CAOs"
    
    # 6. Temporary swapt folder, if not provided, a system temp directory will be used
    temp_folder = None
    
    # Default flt file info -- DO NOT MODIFIED IF NOT NEEDED
    ncols = 5869
    nrows = 6412
    nodata_values = -9999
    cellsize = 30
    xllcorner = 480556.90625
    yllcorner = 5173318.5
    offset = 500000 # chunk size to run # <-- changed from 1mil to current value on 18 May 2009 by mm

##############################################################################
from opus_core.logger import logger
from time import time
import os

if __name__ == "__main__":
    # this import should put under the main
    from biocomplexity.examples.run_simulation_all_chunks import Simulation

    t1 = time()
    # convert_flt=False for multi year prediction - output in urbansim_cache (number 3. above),
    # convert_flt=True for 1 year prediction only - output in specified output directory (number 5. above),
    Simulation().run(LccmConfiguration.base_directory, 
                     LccmConfiguration.urbansim_cache_directory, 
                     LccmConfiguration.years, 
                     LccmConfiguration.output_directory,
                     LccmConfiguration.temp_folder,
                     LccmConfiguration.coefficients,
                     LccmConfiguration.specification,
                     convert_flt=True, convert_input=False)
    logger.log_status("Model prediction done. " + str(time()-t1) + " s")





