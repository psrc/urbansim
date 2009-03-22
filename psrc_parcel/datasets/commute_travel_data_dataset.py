# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.node_travel_data_dataset import NodeTravelDataDataset as UrbansimNodeTravelDataDataset
from opus_core.logger import logger

class CommuteTravelDataDataset(UrbansimNodeTravelDataDataset):
    in_table_name_default = "commute_travel_data"
    out_table_name_default = "commute_travel_data"
    dataset_name = "commute_travel_data"
    
    connection_mapping = { # connection path from a node (key) to the centroid of the 'zone'
        3232: {'zone': 136,
               'path': (3231, 1842)},
        2319: {'zone': 549,
               'path': (2396, 3313, 3293)},
        2873: {'zone': 368,
               'path': (1348, 1421,)},
        4835: {'zone': 416,
               'path': (6628, 6523)},
        4489: {'zone': 293,
               'path': (2642, 4492)},
        2189: {'zone': 605,
               'path': (2190, 605)},
        5325: {'zone': 341,
               'path': (341,)},
        3069: {'zone': 411,
               'path': (1296, 411)},
        3120: {'zone': 489,
               'path': (1688, 2991, 4200)},
        3160: {'zone': 499,
               'path': (2217, 499)},
        2958: {'zone': 340,
               'path': (5217, 340)},
        3256: {'zone': 285,
               'path': (2754, 285)},
        3601: {'zone': 604,
               'path': (2190, 2014, 2580, 604)},
        4812: {'zone': 293,
               'path': (3256, 4489, 2642, 4492)},
        3173: {'zone': 366,
               'path': (3183, 2698, 366)},
                   }
        
    def get_attribute_from_travel_data(self, name, from_node, to_node, node_travel_data, travel_data, return_value_if_not_found=0.0):
        """ Return attribute derived from the travel_data dataset, where values along the path given by 
        connection_mapping are subtracted.
        """
        if from_node not in self.connection_mapping.keys():
            from_zone, path_to_from_zone = from_node, ()
        else:
            from_zone, path_to_from_zone = (self.connection_mapping[from_node]['zone'], self.connection_mapping[from_node]['path'])
        if to_node not in self.connection_mapping.keys():
            to_zone, path_to_to_zone = to_node, ()
        else:
            to_zone, path_to_to_zone = (self.connection_mapping[to_node]['zone'], self.connection_mapping[to_node]['path'])
        try:                            
            td_value = travel_data.get_attribute_by_id(name, [[from_zone, to_zone]])
        except:
            logger.log_warning('Connection from %s to %s not found.' % (from_node, to_node))
            return return_value_if_not_found
        #print "zones: (%s) %s (%s)" % (from_zone, td_value, to_zone)
        attr_from_node_to_zone = node_travel_data._get_attribute_sum_from_path(name, [from_node] + list(path_to_from_zone)) + node_travel_data._get_attribute_sum_from_path(name, [to_node] + list(path_to_to_zone))
        #print "from node to zone: %s" % attr_from_node_to_zone
        return td_value - attr_from_node_to_zone