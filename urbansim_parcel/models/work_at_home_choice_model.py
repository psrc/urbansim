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
from opus_core.choice_model import ChoiceModel, prepare_specification_and_coefficients
from urbansim.estimation.estimator import get_specification_for_estimation
from numpy import arange, where, ones
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.misc import unique_values
from opus_core.logger import logger

class WorkAtHomeChoiceModel(ChoiceModel):
    """
    This model first predicts the probability of workers working at home, 
    then assigns them to one of the home-based jobs 
    """
    model_name = "Work At Home Choice Model"
    model_short_name = "WAHCM"

    def __init__(self, choice_set, filter=None, choice_attribute_name='work_at_home', location_id_name='urbansim_parcel.person.building_id', **kwargs):
        self.job_set = choice_set
        self.filter = filter
        self.choice_attribute_name = choice_attribute_name
        self.location_id_name = location_id_name
        ChoiceModel.__init__(self, [1, 2], choice_attribute_name=choice_attribute_name, **kwargs)
        
    def run(self, *args, **kwargs):
        choices = ChoiceModel.run(self, *args, **kwargs)
        #prob_work_at_home = self.upc_sequence.probabilities[:, 0]
        
        if self.filter is not None:
            choice_set_index = where( self.job_set.compute_variables(self.filter) )[0]
        else:
            choice_set_index = arange( self.job_set.size() )
        
        at_home_worker_index = kwargs['agents_index'][choices==1]
        if at_home_worker_index.size >= choice_set_index.size: 
           #number of at home workers is greater than the available choice (home_based jobs by default)
            assigned_worker_index = sample_noreplace(at_home_worker_index, choice_set_index.size)
            assigned_choice_index = choice_set_index
        else:
            assigned_worker_index = at_home_work_index
            assigned_choice_index=sample_noreplace(choice_set_index, at_home_work_index.size)
        
        ## each worker can only be assigned to 1 job
        #assert assigned_worker_index.size == unique_values(assigned_worker_index).size
        agent_set = kwargs['agent_set']
        agent_set.set_values_of_one_attribute(self.choice_attribute_name, 
                                              choices, 
                                              index=kwargs['agents_index'])
        agent_set.set_values_of_one_attribute(self.job_set.get_id_name()[0], 
                                              self.job_set.get_id_attribute()[assigned_choice_index], 
                                              index=assigned_worker_index)
        agent_set.compute_variables([self.location_id_name], dataset_pool=self.dataset_pool)
        self.job_set.modify_attribute(name=VariableName(self.location_id_name).get_alias(), 
                                      data=agent_set.get_attribute_by_index(self.location_id_name, assigned_worker_index),
                                      index=assigned_choice_index)
        logger.log_status("%s workers chose to work at home, %s workers chose to work out of home." % 
                          (where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 1)[0].size,
                           where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 2)[0].size))
        logger.log_status("Total: %s workers work at home, %s workers work out of home." % 
                          (where(agent_set.get_attribute(self.choice_attribute_name) == 1)[0].size,
                           where(agent_set.get_attribute(self.choice_attribute_name) == 2)[0].size))
        
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
    
    def prepare_for_estimate(self, *args, **kwargs):
        return prepare_for_estimate(*args, **kwargs)

    
def prepare_for_estimate(specification_dict = None, 
                         specification_storage=None, 
                         specification_table=None,
                         agent_set=None, 
                         household_set=None,
                         agents_for_estimation_storage=None,
                         agents_for_estimation_table=None,
                         households_for_estimation_table=None,
                         join_datasets=False,
                         filter=None,
                         data_objects=None):
    specification = get_specification_for_estimation(specification_dict, 
                                                     specification_storage, 
                                                     specification_table)
    if agents_for_estimation_storage is not None:                 
        estimation_set = Dataset(in_storage = agents_for_estimation_storage, 
                                 in_table_name=agents_for_estimation_table,
                                 id_name=agent_set.get_id_name(), 
                                 dataset_name=agent_set.get_dataset_name())
        hh_estimation_set = None
        if households_for_estimation_table is not None:
            hh_estimation_set = Dataset(in_storage = agents_for_estimation_storage, 
                                     in_table_name=households_for_estimation_table,
                                     id_name=household_set.get_id_name(), 
                                     dataset_name=household_set.get_dataset_name())
        
        filter_index = arange(estimation_set.size())
        if filter:
            estimation_set.compute_variables(filter, resources=Resources(data_objects))
            filter_index = where(estimation_set.get_attribute(filter) > 0)[0]
            #estimation_set.subset_by_index(index, flush_attributes_if_not_loaded=False)
        
        if join_datasets:
            if hh_estimation_set is not None:
                household_set.join_by_rows(hh_estimation_set, require_all_attributes=False,
                                           change_ids_if_not_unique=True)
                
            agent_set.join_by_rows(estimation_set, require_all_attributes=False,
                                   change_ids_if_not_unique=True)
            index = arange(agent_set.size() - estimation_set.size(), agent_set.size())[filter_index]
        else:
            index = agent_set.get_id_index(estimation_set.get_id_attribute()[filter_index])
    else:
        if agent_set is not None:
            index = arange(agent_set.size())
        else:
            index = None
            
    return (specification, index)
