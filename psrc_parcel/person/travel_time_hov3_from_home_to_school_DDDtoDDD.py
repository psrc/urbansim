# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc_parcel.person.travel_time_from_home_to_school_DDDtoDDD import travel_time_from_home_to_school_DDDtoDDD

class travel_time_hov3_from_home_to_school_DDDtoDDD(travel_time_from_home_to_school_DDDtoDDD):
    """Travel time for hov3+ from home to school obtained from hdf5 skims. Time periods can be 
        given in the variable name, e.g. travel_time_hov3_from_home_to_school_6to8.
        
    """
    travel_data_attribute = "h3tlINCt"
