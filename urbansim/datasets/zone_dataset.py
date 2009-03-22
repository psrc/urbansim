# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class ZoneDataset(UrbansimDataset):
    
    id_name_default = "zone_id"
    in_table_name_default = "zones"
    out_table_name_default = "zones"
    dataset_name = "zone"

    default_prototype_dataset = None
    default_template_project = None
    default_legend_file = None

#    # original code for converting dataset to gridcell dataset for plotting with matplotlib
#    def plot_map(self, name, gridcell=None, **opt_args):
#            if gridcell is None:
#                gridcell = Resources()["gridcell"]
#            gridcell.compute_variables("urbansim.gridcell.zone_id")
#    
#            name = VariableName(name).get_alias()
#            if name in self.get_known_attribute_names(): # attribute of fazes
#                new_name = name+'_of_zone'
#                gridcell.join(self, name=name, new_name=new_name)
#            elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
#                new_name = name
#            else:
#                raise StandardError, "Attribute " + name + " not known."
#            gridcell.plot_map(new_name, **opt_args)


# TODO: Delete all code below
#    def plot_map(self, name, gridcell=None, isMapnikMap=False, **opt_args):
#        # TODO: delete the else statement and 'isMapnikMap' arg when all maps are converted to Mapnik
#        if (isMapnikMap):
#            name = VariableName(name).get_alias()
#            if name in self.get_known_attribute_names(): # attribute of zones
#                new_name = name+'_of_zone'
#            else:
#                raise StandardError, "Attribute " + name + " not known."
#            
#            from opus_core.datasets.abstract_dataset import AbstractDataset
#            AbstractDataset.plot_map(self, unique_id='zone_id', unique_id_arr=self.get_id_attribute(), attrib_name=new_name[0:10], attrib_arr=self.get_attribute(name), name=new_name, **opt_args)
#        
#        else: # original code for converting dataset to gridcell dataset for plotting with matplotlib
#            if gridcell is None:
#                gridcell = Resources()["gridcell"]
#            gridcell.compute_variables("urbansim.gridcell.zone_id")
#    
#            name = VariableName(name).get_alias()
#            if name in self.get_known_attribute_names(): # attribute of fazes
#                new_name = name+'_of_zone'
#                gridcell.join(self, name=name, new_name=new_name)
#            elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
#                new_name = name
#            else:
#                raise StandardError, "Attribute " + name + " not known."
#            gridcell.plot_map(new_name, **opt_args)
