# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.misc import unique_values
from numpy import array, zeros, int16, where, int8, ones, take, arange
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class CensusTractDataset(UrbansimDataset):
    
    id_name_default = "tract_id"
    in_table_name_default = "tracts"
    out_table_name_default = "tracts"
    dataset_name = "census_tract"
    
#    def __init__(self, id_values=None, fazset=None, **kwargs):
#
#        UrbansimDataset.__init__(self, **kwargs)
#               
#        if id_values <> None:
#            self._add_id_attribute(data=id_values, name=self.get_id_name()[0])
#        elif fazset <> None:
#            if (self.get_id_name()[0] not in fazset.get_attribute_names()) and \
#                (self.get_id_name()[0] not in fazset.get_primary_attribute_names()):
#                raise StandardError, "Given FazDataset does not contain " + self.get_id_name()[0]               
#            district_ids = fazset.get_attribute(self.get_id_name()[0])
#            idx = where(district_ids >=0)[0]
#            unique_ids = unique_values(district_ids[idx])
#            self._add_id_attribute(data=unique_ids, name=self.get_id_name()[0])
#        self._create_id_mapping_array()
#        
#    def _update_id_mapping(self):
#        UrbansimDataset._update_id_mapping(self)
#        self._create_id_mapping_array()
#              
#    def _create_id_mapping_array(self):
#        ids = self.get_id_attribute()
#        self.__id_mapping_array = -1*ones(ids.max())
#        self.__id_mapping_array[self.get_id_attribute()-1] = self.get_id_index(ids)
#
#    def plot_map(self, name, gridcell=None, **opt_args):
#        if gridcell is None:
#            gridcell = Resources()["gridcell"]
#        gridcell.compute_variables("urbansim.gridcell.district_id")
#
#        name = VariableName(name).alias()
#        if name in self.get_known_attribute_names(): # attribute of fazes
#            new_name = name+'_of_district'
#            gridcell.join(self, name=name, new_name=new_name)
#        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
#            new_name = name
#        else:
#            raise StandardError, "Attribute " + name + " not known."
#        gridcell.plot_map(new_name, **opt_args)
#                                      
