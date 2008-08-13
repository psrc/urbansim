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

    def openev_plot(self, name, gridcell=None, **opt_args):
        if gridcell is None:
            gridcell = Resources()["gridcell"]
#        if not opt_args.has_key['prototype_dataset'] and self.default_prototype_dataset is not None:
#            prototype_dataset = self.default_prototype_dataset
#        if not opt_args.has_key['template_project'] and self.default_template_project is not None:
#            template_project = self.default_template_project
#        if not opt_args.has_key['legend_file'] and self.default_legend_file is not None:
#            legend_file = self.default_legend_file
        
        name = VariableName(name).get_alias()
        if name in self.get_known_attribute_names(): # attribute of fazes
            new_name = name+'_of_zone'
            gridcell.join(self, name=name, new_name=new_name)
        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
            new_name = name
        else:
            raise StandardError, "Attribute " + name + " not known."
        gridcell.openev_plot(new_name, **opt_args)

    def plot_map(self, name, gridcell=None, **opt_args):
        if gridcell is None:
            gridcell = Resources()["gridcell"]
        gridcell.compute_variables("urbansim.gridcell.zone_id")

        name = VariableName(name).get_alias()
        if name in self.get_known_attribute_names(): # attribute of fazes
            new_name = name+'_of_zone'
            gridcell.join(self, name=name, new_name=new_name)
        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
            new_name = name
        else:
            raise StandardError, "Attribute " + name + " not known."
        gridcell.plot_map(new_name, **opt_args)

