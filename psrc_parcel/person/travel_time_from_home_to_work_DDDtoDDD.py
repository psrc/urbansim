# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from psrc.abstract_variables.abstract_travel_data_h5_income_variable_DDDtoDDD import abstract_travel_data_h5_income_variable_DDDtoDDD

class travel_time_from_home_to_work_DDDtoDDD(abstract_travel_data_h5_income_variable_DDDtoDDD):
    """Travel time from home to work obtained from hdf5 skims. Time periods can be 
        given in the variable name, e.g. travel_time_from_home_to_work_6to8.
        
    """
    default_value = 0
    origin_zone_id = "residence_zone_id = person.disaggregate(urbansim_parcel.household.zone_id)"
    destination_zone_id = "workplace_zone_id = urbansim_parcel.person.workplace_zone_id"
    travel_data_attribute = "svtlINCt"
    income_groups_attribute = "psrc_parcel.person.income_groups_for_tm"
    
    def __init__(self, from_time, to_time):
        abstract_travel_data_h5_income_variable_DDDtoDDD.__init__(self, from_time, to_time)
    
# unit test implemented in travel_distance_from_home_to_work_DDDtoDDD