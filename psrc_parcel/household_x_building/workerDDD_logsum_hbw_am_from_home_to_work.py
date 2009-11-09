# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_logsum_variable import abstract_logsum_variable

class workerDDD_logsum_hbw_am_from_home_to_work(abstract_logsum_variable):
    """logsum_hbw_am_time_from_home_to_work
       logsum breaks by income:
           Less than $25K;
           $25K to $45K;
           $45 to $75K;
           More than $75K.
    """
    
    def __init__(self, number):
        self.default_value = -9
        self.agent_zone_id = "work%s_workplace_zone_id = household.aggregate((person.worker%s == 1).astype(int32) * urbansim_parcel.person.workplace_zone_id)" % (number, number)
        self.agent_category_attribute = "(psrc.household.logsum_income_break).astype(int32)"
        self.location_zone_id = "urbansim_parcel.building.zone_id"
        self.travel_data_attributes = {1: "travel_data.logsum_hbw_am_income_1", 
                                       2: "travel_data.logsum_hbw_am_income_2", 
                                       3: "travel_data.logsum_hbw_am_income_3", 
                                       4: "travel_data.logsum_hbw_am_income_4" }
        self.direction_from_home = False
        abstract_logsum_variable.__init__(self)
