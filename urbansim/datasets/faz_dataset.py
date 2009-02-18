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
from opus_core.misc import unique_values
from numpy import array, zeros, int16, int8, int32, ones, take, arange
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class FazDataset(UrbansimDataset):

    id_name_default = "faz_id"
    in_table_name_default = "fazes"
    out_table_name_default = "fazes"
    dataset_name = "faz"

    def __init__(self, id_values=None, zoneset=None, **kwargs):

        UrbansimDataset.__init__(self, **kwargs)

        self.same_age_table = None
        self.same_sector_table = None

        if id_values <> None:
            self._add_id_attribute(data=id_values, name=self.get_id_name()[0])
        elif zoneset <> None:
            if (self.get_id_name()[0] not in zoneset.get_known_attribute_names()):
                raise StandardError, "Given ZoneDataset does not contain " + self.get_id_name()[0]
            fazids = zoneset.get_attribute(self.get_id_name()[0])
            unique_ids = unique_values(fazids[fazids >=0])
            self._add_id_attribute(data=unique_ids, name=self.get_id_name()[0])
        self._create_id_mapping_array()

    def _update_id_mapping(self):
        UrbansimDataset._update_id_mapping(self)
        self._create_id_mapping_array()

    def create_same_age_table(self, agents, age_name="age_of_head"):
        max_age = 120
        n = self.size()
        hh_age = agents.get_attribute(age_name).astype(int16)
        ages = unique_values(hh_age)
        self.same_age_table = zeros((ages.size, n), dtype=int32)
        self.same_age_table_mapping = {}
        faz_ids = agents.get_attribute(self.get_id_name()[0])
        for iage in arange(ages.size):
            is_age = hh_age == ages[iage]
            self.same_age_table[iage,:] = self.sum_over_ids(faz_ids, is_age.astype(int8))
            self.same_age_table_mapping[ages[iage]]=iage

    def _create_id_mapping_array(self):
        ids = self.get_id_attribute()
        self.__id_mapping_array = (-1*ones(ids.max())).astype(int32)
        self.__id_mapping_array[self.get_id_attribute()-1] = self.get_id_index(ids)

    def get_value_from_same_age_table(self, ages, fazes):
        age_array = array(map(lambda x: self.same_age_table_mapping[x], ages),
                         dtype=int32).reshape((ages.size,1)).repeat(repeats=fazes.shape[1], axis=1)
        return self.same_age_table[age_array, self.__id_mapping_array[fazes-1]]

    def create_same_job_sector_table(self, agents, sector_field_name="sector_id"):
        max_sector = agents.get_attribute(sector_field_name).max()
        n = self.size()
        sectors = agents.get_attribute(sector_field_name).astype(int16)
        unique_sectors = unique_values(sectors)
        self.same_job_sector_table = zeros((unique_sectors.size, n), dtype=int32)
        self.same_job_sector_table_mapping = {}
        faz_ids = agents.get_attribute(self.get_id_name()[0])
        for isec in arange(unique_sectors.size):
            is_sector = sectors == unique_sectors[isec]
            self.same_job_sector_table[isec,:] = self.sum_over_ids(faz_ids, is_sector.astype(int8))
            self.same_job_sector_table_mapping[unique_sectors[isec]]=isec

    def get_value_from_same_job_sector_table(self, sectors, fazes):
        sector_array = array(map(lambda x: self.same_job_sector_table_mapping[x], sectors),
                             dtype=int32).reshape((sectors.size,1)).repeat(repeats=fazes.shape[1], axis=1)
        return self.same_job_sector_table[sector_array, self.__id_mapping_array[fazes-1]]

    # TODO: delete commented out code as soon as mapping by city is tested with Mapnik (JLM)

#    def plot_map(self, name, gridcell=None, **opt_args):
#        if gridcell is None:
#            gridcell = Resources()["gridcell"]
#        gridcell.compute_variables("urbansim.gridcell.faz_id")
#
#        name = VariableName(name).get_alias()
#        if name in self.get_known_attribute_names():
#            new_name = name+'_of_faz'
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
        gridcell.compute_variables("urbansim.gridcell.faz_id")

#        if prototype_dataset is None and self.default_prototype_dataset is not None:
#            prototype_dataset = self.default_prototype_dataset
#        if template_project is None and self.default_template_project is not None:
#            template_project = self.default_template_project
#        if legend_file is None and self.default_legend_file is not None:
#            legend_file = self.default_legend_file

        if name in self.get_known_attribute_names(): # attribute of fazes
            new_name = name+'_of_faz'
            gridcell.join(self, name=name, new_name=new_name)
        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
            new_name = name
        else:
            raise StandardError, "Attribute " + name + " not known."

        gridcell.openev_plot(new_name, **opt_args)
#=======
#        name = VariableName(name).get_alias()
#        if name in self.get_known_attribute_names():
#            new_name = name+'_of_faz'
#            gridcell.join(self, name=name, new_name=new_name)
#        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
#            new_name = name
#        else:
#            raise StandardError, "Attribute " + name + " not known."
#        gridcell.plot_map(new_name, **opt_args)
#>>>>>>> .r5247
