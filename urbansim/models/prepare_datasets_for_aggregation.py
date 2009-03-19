# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.model import Model
from opus_core.variables.variable_name import VariableName

class PrepareDatasetsForAggregation(Model):
    """Model for preparing datasets for running on higher aggregation level. It computes 
    given variables and sets them as primary attributes. The corresponding old variable box is 
    deleted and created a new one.
    """
    def run(self, datasets_variables={}, dataset_pool=None, flush_dataset=True):
        """
        datasets_variables is a dictionary where keys are dataset objects and each 
        value is a list of variables (as fully qualified names) to be computed.
        data_objects is a dictionary to be passed in the variable computation.
        If 'flush_dataset' is True, the datasets given as keys in 'datasets_variables'
        are flushed to cache.
        """
        for dataset in datasets_variables.keys():
            variables = datasets_variables[dataset]
            dataset.compute_variables(variables, dataset_pool=dataset_pool)
            for var in variables:
                varname = VariableName(var)
                values = dataset.get_attribute(varname)
                dataset.delete_one_attribute(varname)
                dataset.add_primary_attribute(values, varname.get_alias())
            if flush_dataset:
                dataset.flush_dataset()
