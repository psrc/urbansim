# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from .income_to_avg_val_per_unit_ratio import income_to_avg_val_per_unit_ratio

class income_to_avg_val_per_unit_wwd_ratio(income_to_avg_val_per_unit_ratio):
    """ income / (avg_val_per_unit_residential_wwd/10)""" 
    
    val_per_unit = "residential_avg_val_per_unit_within_walking_distance"
    hh_income = "income"
