# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.control_total.household_total_growth_luv import household_total_growth_luv

class job_total_growth_luv(household_total_growth_luv):
    """The total growth for the total column between the 5-years LUV totals.
    """
    
    target_attribute_name = 'total_number_of_jobs'

