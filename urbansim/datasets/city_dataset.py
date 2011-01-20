# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.misc import unique
from numpy import array, zeros, int16, int8, ones, take, arange
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class CityDataset(UrbansimDataset):

    id_name_default = "city_id"
    in_table_name_default = "cities"
    out_table_name_default = "cities"
    dataset_name = "city"

    def __init__(self, id_values=None, gridcellset=None, **kwargs):

        UrbansimDataset.__init__(self, **kwargs)

        if id_values <> None:
            self._add_id_attribute(data=id_values, name=self.get_id_name()[0])
        elif gridcellset <> None:
            if (self.get_id_name()[0] not in gridcellset.get_attribute_names()) and \
                (self.get_id_name()[0] not in gridcellset.get_primary_attribute_names()):
                raise StandardError, "Given gridcellset does not contain " + self.get_id_name()[0]
            large_area_ids = gridcellset.get_attribute(self.get_id_name()[0])
            idx = large_area_ids >=0
            unique_ids = unique(large_area_ids[idx])
            self._add_id_attribute(data=unique_ids, name=self.get_id_name()[0])
        self._create_id_mapping_array()

    def _update_id_mapping(self):
        UrbansimDataset._update_id_mapping(self)
        self._create_id_mapping_array()

    def _create_id_mapping_array(self):
        ids = self.get_id_attribute()
        self.__id_mapping_array = -1*ones(ids.max())
        self.__id_mapping_array[self.get_id_attribute()-1] = self.get_id_index(ids)


    # TODO: delete commented out code as soon as mapping by city is tested with Mapnik (JLM)
    
#    def plot_map(self, name, gridcell=None, **opt_args):
#        if gridcell is None:
#            gridcell = Resources()["gridcell"]
#        gridcell.compute_variables("urbansim.gridcell.city_id")
#
#        name = VariableName(name).get_alias()
#        if name in self.get_known_attribute_names():
#            new_name = name+'_of_city'
#            gridcell.join(self, name=name, new_name=new_name)
#        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
#            new_name = name
#        else:
#            raise StandardError, "Attribute " + name + " not known."
#        gridcell.plot_map(new_name, **opt_args)

#<<<<<<< .mine
    def openev_plot(self, name, gridcell=None, **opt_args):
        if gridcell is None:
            gridcell = Resources()["gridcell"]
        gridcell.compute_variables("urbansim.gridcell.city_id")

#        if prototype_dataset is None and self.default_prototype_dataset is not None:
#            prototype_dataset = self.default_prototype_dataset
#        if template_project is None and self.default_template_project is not None:
#            template_project = self.default_template_project
#        if legend_file is None and self.default_legend_file is not None:
#            legend_file = self.default_legend_file

        if name in self.get_known_attribute_names(): # attribute of fazes
            new_name = name+'_of_city'
            gridcell.join(self, name=name, new_name=new_name)
        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
            new_name = name
        else:
            raise StandardError, "Attribute " + name + " not known."

        gridcell.openev_plot(new_name, **opt_args)

#=======
#        name = VariableName(name).get_alias()
#        if name in self.get_known_attribute_names():
#            new_name = name+'_of_city'
#            gridcell.join(self, name=name, new_name=new_name)
#        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
#            new_name = name
#        else:
#            raise StandardError, "Attribute " + name + " not known."
#        gridcell.plot_map(new_name, **opt_args)
#>>>>>>> .r5247

