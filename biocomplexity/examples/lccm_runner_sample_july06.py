# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

""" This module is a sample configuration of the Land Change Cover Model (LCCM).
It is intended to be modified to specify parameters to the model, or to
make basic modifications to its behavior."""


#############################################################################
# Configuration settings
#############################################################################

"""
how to start a lccm run?

1). need urbansim cache for the run.
    - create a new folder in your local drive: c:\urbansim_cache
    - use windows explorer go to this address: \\ukiah\lccm_urbansim_cache
    - copy the 2006_02_14__11_43 folder to c:\urbansim_cache

2). go to biocomplexity.examples.lccm_runner_sample, fill in the
configurations for the run (Notice that if you use the same folder name
in step 1, it is good to go now).

3). execute the file lccm_runner_sample in eclipse to run the
simulation.
"""


class LccmConfiguration:

    # Years - the years for which the model is run. The first year
    #   in the list is taken to be the base year; the model runs for
    #   each subsequent year.
    years = [2003,2007,2011,2015,2019,2023,2027]
    
    # Base directory - the input directory that contains all the input flt
    base_directory = r"c:\eclipse\LCCM_4County_converted/1999"
    
    # Urbansim output data - cache directory
    #   (notice that this is the folder that contains all years folder)
    urbansim_cache_directory = r"c:\eclipse\urbansim_cache"
    
    # specification and cofficients use:
    #    look under biocomplexity.data folder for the coefficients and specification
    #    fill in the names of the ones that shuold be used for the simulation
    coefficients = "land_cover_change_model_coefficients_a95_99corrected"
    specification = "land_cover_change_model_specification_a95_99corrected"
    
    # Output directory - the directory that contains the output flt files
    #output_directory = r"g:\lccm_output\LCCM_4County_output_a95_99_run2"
    output_directory = r"g:\lccm_output\LCCM_4County_output_a95_99_run9"
    
    # Temporary swapt folder, if not provided, a system temp directory will be used                                                                      
    temp_folder = r"g:\temp"
    
    # Default flt file info -- DO NOT MODIFIED IF NOT NEEDED
    ncols = 5869
    nrows = 6412
    nodata_values = -9999
    cellsize = 30
    xllcorner = 480556.90625
    yllcorner = 5173318.5
    offset = 1000000 # chunk size to run

##############################################################################

import os

if __name__ == "__main__":
    # this import should put under the main
    from biocomplexity.examples.run_simulation_all_chunks import Simulation
    
    Simulation().run(LccmConfiguration.base_directory, 
                     LccmConfiguration.urbansim_cache_directory, 
                     LccmConfiguration.years, 
                     LccmConfiguration.output_directory,
                     LccmConfiguration.temp_folder,
                     LccmConfiguration.coefficients,
                     LccmConfiguration.specification,
                     convert_flt=True, convert_input=False)
    





