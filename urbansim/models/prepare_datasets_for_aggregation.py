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

from opus_core.model import Model
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class PrepareDatasetsForAggregation(Model):
    """Model for preparing datasets for running on higher aggregation level. It computes 
    given variables and sets them as primary attributes. The corresponding old variable box is 
    deleted and created a new one.
    """
    def run(self, datasets_variables={}, data_objects={}, flush_dataset=True):
        """
        datasets_variables is a dictionary where keys are dataset objects and each 
        value is a list of variables (as fully qualified names) to be computed.
        data_objects is a dictionary to be passed in the variable computation.
        If 'flush_dataset' is True, the datasets given as keys in 'datasets_variables'
        are flushed to cache.
        """
        for dataset in datasets_variables.keys():
            variables = datasets_variables[dataset]
            dataset.compute_variables(variables, resources=Resources(data_objects))
            for var in variables:
                varname = VariableName(var)
                values = dataset.get_attribute(varname)
                dataset.delete_one_attribute(varname)
                dataset.add_primary_attribute(values, varname.get_alias())
            if flush_dataset:
                dataset.flush_dataset()
