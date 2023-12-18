# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.resources import Resources
from opus_core.misc import unique
from numpy import array, zeros, int16, int8
from opus_core.variables.variable_name import VariableName

class FazdistrictDataset(UrbansimDataset):

    id_name_default = "fazdistrict_id"
    dataset_name = "fazdistrict"

    def __init__(self, id_values=None, fazset=None, **kwargs):

        UrbansimDataset.__init__(self, **kwargs)

        self.same_age_table = None
        self.same_sector_table = None

        if id_values != None:
            self._add_id_attribute(data=id_values, name=self.get_id_name()[0])
        elif fazset != None:
            if (self.get_id_name()[0] not in fazset.get_attribute_names()) and \
                (self.get_id_name()[0] not in fazset.get_primary_attribute_names()):
                raise Exception("Given FazDataset does not contain " + self.get_id_name()[0])
            fazdistricts = fazset.get_attribute(self.get_id_name()[0])
            unique_ids = unique(fazdistricts[fazdistricts >=0])
            self._add_id_attribute(data=unique_ids, name=self.get_id_name()[0])

    #below copied from fazes.py
    def create_same_age_table(self, agents, age_name="age_of_head"):
        max_age = 120
        if self.size() <= 0: # nothing loaded yet
            self.get_id_attribute()
        n = self.size()
        hh_age = agents.get_attribute(age_name).astype(int16)
        ages = unique(hh_age)
        self.same_age_table = zeros((ages.size, n))
        self.same_age_table_mapping = {}
        faz_ids = agents.get_attribute(self.get_id_name()[0])
        i=0
        for age in ages:
            is_age = hh_age == age
            self.same_age_table[i,:] = self.sum_over_ids(faz_ids, is_age.astype(int8))
            self.same_age_table_mapping[age]=i
            i += 1

    def get_value_from_same_age_table(self, age, faz):
        ids = array(faz)
        index = self.get_id_index(ids)
        return self.same_age_table[self.same_age_table_mapping[age], index]

    def create_same_job_sector_table(self, agents, sector_field_name="sector_id"):
        max_sector = agents.get_attribute(sector_field_name).max()
        if self.size() <= 0: # nothing loaded yet
            self.get_id_attribute()
        n = self.size()
        sectors = agents.get_attribute(sector_field_name).astype(int16)
        unique_sectors = unique(sectors)
        self.same_job_sector_table = zeros((unique_sectors.size, n))
        self.same_job_sector_table_mapping = {}
        faz_ids = agents.get_attribute(self.get_id_name()[0])
        i=0
        for sec in unique_sectors:
            is_sector = sectors == sec
            self.same_job_sector_table[i,:] = self.sum_over_ids(faz_ids, is_sector.astype(int8))
            self.same_job_sector_table_mapping[sec]=i
            i += 1

    def get_value_from_same_job_sector_table(self, sector, faz):
        ids = array(faz)
        index = self.get_id_index(ids)
        return self.same_job_sector_table[self.same_job_sector_table_mapping[sector], index]

    def plot_map(self, name, gridcell=None, **opt_args):
        if gridcell is None:
            gridcell = Resources()["gridcell"]
        gridcell.compute_variables("urbansim.gridcell.fazdistrict_id")

        name = VariableName(name).get_alias()
        if name in self.get_known_attribute_names(): # attribute of fazes
            new_name = name+'_of_fazdistrict'
            gridcell.join(self, name=name, new_name=new_name)
        elif name in gridcell.get_known_attribute_names(): # attribute of gridcells
            new_name = name
        else:
            raise Exception("Attribute " + name + " not known.")
        gridcell.plot_map(new_name, **opt_args)
