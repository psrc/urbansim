# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from income_to_avg_val_per_unit_ratio import income_to_avg_val_per_unit_ratio

class income_to_avg_val_per_unit_wwd_ratio(income_to_avg_val_per_unit_ratio):
    """ income / (avg_val_per_unit_residential_wwd/10)""" 
    
    val_per_unit = "residential_avg_val_per_unit_within_walking_distance"
    hh_income = "income"
