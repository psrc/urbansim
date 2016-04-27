# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.control_total.household_growth_rate_luv import household_growth_rate_luv

class job_growth_rate_luv(household_growth_rate_luv):
    """The rate of growth for the total column between the 5-years LUV totals.
    """
    
    target_attribute_name = 'total_number_of_jobs'

