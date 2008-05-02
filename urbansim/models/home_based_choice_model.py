#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from opus_core.choice_model import ChoiceModel
from opus_core.model import prepare_specification_and_coefficients
from numpy import arange, where
from opus_core.variables.variable_name import VariableName

class HomeBasedChoiceModel(ChoiceModel):
    """
    """
    model_name = "Home Based Choice Model"
    model_short_name = "HBCM"
    
    def prepare_for_estimate(self, 
                             specification_dict = None, 
                             specification_storage=None, 
                             specification_table=None,
                             agent_set=None, 
                             agents_for_estimation_storage=None,
                             agents_for_estimation_table=None, 
                             join_datasets=False,
                             filter=None):
        from opus_core.model import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict, 
                                                         specification_storage, 
                                                         specification_table)
        if agents_for_estimation_storage is not None:                 
            estimation_set = Dataset(in_storage = agents_for_estimation_storage, 
                                      in_table_name=agents_for_estimation_table,
                                      id_name=agent_set.get_id_name(), dataset_name=agent_set.get_dataset_name())
            if filter:
                estimation_set.compute_variables(filter, resources=Resources(data_objects))
                index = where(estimation_set.get_attribute(filter) > 0)[0]
                estimation_set.subset_by_index(index, flush_attributes_if_not_loaded=False)
            
            if join_datasets:
                agent_set.join_by_rows(estimation_set, require_all_attributes=False,
                                       change_ids_if_not_unique=True)
                index = arange(agent_set.size()-estimation_set.size(),agent_set.size()) 
            else:
                index = agent_set.get_id_index(estimation_set.get_id_attribute())
        else:
            if agent_set is not None:
                index = arange(agent_set.size())
            else:
                index = None
        return (specification, index)
    
    def run(self, *args, **kwargs):
        choices = ChoiceModel.run(self, *args, **kwargs)
        kwargs['agent_set'].set_values_of_one_attribute(self.choice_set._id_names[0], choices, index=kwargs['agents_index'])
    
    def prepare_for_run(self, 
                        specification_storage=None, 
                        specification_table=None,
                        coefficients_storage=None,
                        coefficients_table=None,
                        agent_set=None,
                        agents_filter=None,
                        data_objects=None):
        
        spec, coeff = prepare_specification_and_coefficients(specification_storage=specification_storage,
                                               specification_table=specification_table, 
                                               coefficients_storage=coefficients_storage,
                                               coefficients_table=coefficients_table)
        
        if agents_filter is not None:
            agent_set.compute_variables(agents_filter, resources=Resources(data_objects))
            index = where(agent_set.get_attribute(VariableName(agents_filter).get_alias()) > 0)[0]
        
        return (spec, coeff, index)
    
    