# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

#######
# In a command line, you can estimate using this command:
#  
# python urbansim/tools/start_estimation.py -c eugene.configs.baseline_estimation --model=residential_land_share_model -s eugene.estimation.RLSM_specification
#
# see 
# python urbansim/tools/start_estimation.py --help
# for other options
#######

specification = {}
#
# ############################# Residential ##############################  
#
specification = {
             -2:  # submodel id
    [
             "constant",

#            "ln(urbansim.gridcell.housing_cost)",
            "urbansim.gridcell.travel_time_to_CBD",
#            "urbansim.gridcell.acres_open_space_within_walking_distance",
#            "urbansim.gridcell.ln_residential_units",
#             "ln_bounded(urbansim.gridcell.non_residential_sqft)",
            "urbansim.gridcell.ln_residential_units_within_walking_distance",\
#            "urbansim.gridcell.ln_service_sector_employment_within_walking_distance",\
#            "urbansim.gridcell.ln_basic_sector_employment_within_walking_distance",\
#            "urbansim.gridcell.ln_retail_sector_employment_within_walking_distance",
#            "urbansim.gridcell.ln_home_access_to_employment_1",\
    ]
}
