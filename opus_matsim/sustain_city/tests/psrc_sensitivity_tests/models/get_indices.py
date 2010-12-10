# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

class GetIndices(object):
    ''' Calulates the indices of key words.
    '''
    
    def __init__(self, header):
        ''' Constructor
        '''
        # header
        self.header = header
        
        # identifyer
        self.from_zone_id = 'from_zone_id'
        self.to_zone_id = 'to_zone_id'
        self.single_vehicle_to_work_travel_cost = 'single_vehicle_to_work_travel_cost'
        self.am_single_vehicle_to_work_travel_time = 'am_single_vehicle_to_work_travel_time'
        
        # default value
        self.from_zone_id_value = -1
        self.to_zone_id_value = -1
        self.single_vehicle_to_work_travel_cost_value = -1
        self.am_single_vehicle_to_work_travel_time_value = -1
        self.number_of_elements = -1
        
        self.init_values()
        
    def init_values(self):
        
        header_list = self.header.split(',')
        
        if header_list != None and len(header_list) > 0:
            for i in range(len(header_list)):
                item = header_list[i]
                # remove space chars
                item = item.strip(' ')
                tmp_list = item.split(':')
                item = tmp_list[0]
                
                if item == self.from_zone_id:
                    self.from_zone_id_value = i
                    continue
                elif item == self.to_zone_id:
                    self.to_zone_id_value = i
                    continue
                elif item == self.single_vehicle_to_work_travel_cost:
                    self.single_vehicle_to_work_travel_cost_value = i
                    continue
                elif item == self.am_single_vehicle_to_work_travel_time:
                    self.am_single_vehicle_to_work_travel_time_value = i
                    continue
            self.number_of_elements = len(header_list)
                
    def get_from_zone_index(self):
        return self.from_zone_id_value
    
    def get_to_zone_index(self):
        return self.to_zone_id_value
    
    def get_single_vehicle_to_work_travel_cost_index(self):
        return self.single_vehicle_to_work_travel_cost_value
    
    def get_am_single_vehicle_to_work_travel_time_index(self):
        return self.am_single_vehicle_to_work_travel_time_value
    
    def get_number_of_colums(self):
        return self.number_of_elements

    