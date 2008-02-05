#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from urbansim.datasets.dataset import NodeTravelDataDataset as UrbansimNodeTravelDataDataset

class NodeTravelDataDataset(UrbansimNodeTravelDataDataset):
    
    connection_mapping = { # connection path from a node (key) to the centroid of the 'zone'
        1842: {'zone': 136,
               'path': (1844,)},
        2319: {'zone': 549,
               'path': (2396, 3313, 3293)},
        2873: {'zone': 368,
               'path': (1348, 1421,)},
        3050: {'zone': 410,
               'path': (1288, 3521)},
        4489: {'zone': 293,
               'path': (2642, 4492)},
                   }
        
    def get_attribute_from_travel_data(self, name, from_node, to_node, travel_data):
        """ Return attribute derived from the travel_data dataset, where values along the path given by 
        connection_mapping are subtracted.
        """
        from_zone, path_to_from_zone = (self.connection_mapping[from_node]['zone'], self.connection_mapping[from_node]['path'])
        to_zone, path_to_to_zone = (self.connection_mapping[to_node]['zone'], self.connection_mapping[to_node]['path'])                                
        td_value = travel_data.get_attribute_by_id(name, [from_zone, to_zone])
        return td_value - self._get_attribute_sum_from_path(name, path_to_from_zone) - self._get_attribute_sum_from_path(name, path_to_to_zone)
        