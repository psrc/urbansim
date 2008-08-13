#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.logger import logger

class NodeTravelDataDataset(UrbansimDataset):
    
    id_name_default = ["from_node_id", "to_node_id"]
    in_table_name_default = "node_travel_data"
    out_table_name_default = "node_travel_data"
    dataset_name = "node_travel_data"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
    def _get_attribute_sum_from_path(self, name, path):
        """Returns a sum of values of the given attribute along the given path."""
        result = 0
        for step in range(len(path)-1):
            try:
                #print " (%s) %s (%s)" % (path[step], self.get_attribute_by_id(name, [[path[step], path[step+1]]]), path[step+1])
                result = result + self.get_attribute_by_id(name, [[path[step], path[step+1]]])
            except:
                logger.log_warning("Path from %s to %s not found." % (path[step], path[step+1]))
        return result