# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from urbansim.datasets.gridcell_dataset import GridcellDataset
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName
from numpy import indices, ceil, sqrt, arange
from opus_core.storage_factory import StorageFactory


class VariableTestToolbox(object):

    datasets = ["land_cover","gridcell"]
    id_names = {"land_cover":[],"gridcell":"grid_id"}#Dataset.hidden_id_name}
    interactions = []

    def get_resources(self, data_dictionary, dataset):
        """Create resources for computing a variable. """
        resources=Resources()
        for key in data_dictionary.keys():
            if key in self.datasets:
                data = data_dictionary[key]
                if self.id_names[key] not in data_dictionary[key].keys() and not isinstance(self.id_names[key], list):
            
                    data[self.id_names[key]] = arange(1,\
                        len(data_dictionary[key][data_dictionary[key].keys()[0]])+1) # add id array
                
                if key == "land_cover":
                    land_cover_storage = StorageFactory().get_storage('dict_storage')
                    land_cover_table_name = 'land_cover'
                    land_cover_storage.write_table(
                            table_name=land_cover_table_name,
                            table_data=data,
                        )

                    lc = LandCoverDataset(
                        in_storage=land_cover_storage, 
                        in_table_name=land_cover_table_name, 
                        )
                        
                    # add relative_x and relative_y
                    lc.get_id_attribute()
                    n = int(ceil(sqrt(lc.size())))
                    
                    if "relative_x" not in data.keys():
                        x = (indices((n,n))+1)[1].ravel()
                        lc.add_attribute(x[0:lc.size()], "relative_x", metadata=1)
                    if "relative_y" not in data.keys():
                        y = (indices((n,n))+1)[0].ravel()
                        lc.add_attribute(y[0:lc.size()], "relative_y", metadata=1)
                        
                    resources.merge({key: lc})
                    
                if key == "gridcell":
                    gridcell_storage = StorageFactory().get_storage('dict_storage')
                    gridcell_table_name = 'gridcell'
                    gridcell_storage.write_table(
                            table_name=gridcell_table_name,
                            table_data=data,
                        )
                    
                    gridcell_dataset = GridcellDataset(
                        in_storage = gridcell_storage,
                        in_table_name = gridcell_table_name,
                        )
                    
                    resources.merge({key: gridcell_dataset})
            else:
                resources.merge({key:data_dictionary[key]})

        if dataset in self.interactions:
            pass
        else:
            resources.merge({"dataset": resources[dataset]})
        resources.merge({"check_variables":'*', "debug":4})
        return resources

    def compute_variable(self, variable_name, data_dictionary, dataset, package=None):
        """Compute variable 'variable_name' from fake data and return the computed values.
        Arguments:
            variable_name - name of variable to be computed
            data_dictionary - a dictionary where each key is either an item of the list self.datasets or the string 'constant'.
                                Values of such entry are again dictionaries, where each key is
                                an attribute/variable/constant name and the value is a list of values for this attribute or a single
                                value in case of a constant.
            dataset - name of the dataset that the variable belongs to.
        """
        varname = VariableName(variable_name)
        resources = self.get_resources(data_dictionary, dataset)
        resources["dataset"].compute_variables(variable_name, resources=resources)
        return resources["dataset"].get_attribute(varname)