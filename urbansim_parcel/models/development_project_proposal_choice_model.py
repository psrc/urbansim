# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from opus_core.choice_model import ChoiceModel
from opus_core.model import prepare_specification_and_coefficients
from opus_core.model import get_specification_for_estimation
from numpy import array, arange, where, ones, concatenate
from opus_core.variables.variable_name import VariableName
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.misc import unique
from opus_core.logger import logger
from urbansim_parcel.datasets.development_project_proposal_dataset import DevelopmentProjectProposalDataset
from urbansim_parcel.models.development_project_proposal_sampling_model import DevelopmentProjectProposalSamplingModel
import copy

class DevelopmentProjectProposalChoiceModel(ChoiceModel, DevelopmentProjectProposalSamplingModel):
    """
    """
    model_name = "Development Project Proposal Choice Model"
    model_short_name = "DPPCM"

    def __init__(self, 
                 proposal_set,
                 sampler="opus_core.samplers.weighted_sampler",
                 weight_string = None,
                 run_config=None, 
                 estimate_config=None,
                 debuglevel=0, 
                 dataset_pool=None,
                 filter="development_project_proposal.status_id==%s" % DevelopmentProjectProposalDataset.id_tentative,
                 choice_attribute_name='is_chosen', 
                 **kwargs):
        self.id_selected = 9
        self.proposal_set = proposal_set
        self.filter = filter
        self.choice_attribute_name = copy.copy(choice_attribute_name)
        ChoiceModel.__init__(self, [1, 2], 
                             choice_attribute_name=choice_attribute_name, 
                             **kwargs)
        DevelopmentProjectProposalSamplingModel.__init__(self, 
                                                         proposal_set,
                                                         sampler="opus_core.samplers.weighted_sampler",
                                                         weight_string = "development_project_proposal.status_id==%s" % self.id_selected,
                                                         #weight_string = "development_project_proposal.status_id==%s" % self.id_selected, 
                                                         run_config=run_config, 
                                                         estimate_config=estimate_config,
                                                         debuglevel=debuglevel, 
                                                         dataset_pool=dataset_pool)
        
    def run(self, agents_index=None, n=500, *args, **kwargs):
        agent_set = self.proposal_set
        if self.filter is not None:
            agents_index = where( self.proposal_set.compute_variables(self.filter) )[0]
            
        choices = ChoiceModel.run(self, agent_set=agent_set, agents_index=agents_index, *args, **kwargs)

        #logger.log_status("%s workers chose to work at home, %s workers chose to work out of home." % 
                          #(where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 1)[0].size,
                           #where(agent_set.get_attribute_by_index(self.choice_attribute_name, kwargs['agents_index']) == 2)[0].size))
        #logger.log_status("Total: %s workers work at home, %s workers work out of home." % 
                          #(where(agent_set.get_attribute(self.choice_attribute_name) == 1)[0].size,
                           #where(agent_set.get_attribute(self.choice_attribute_name) == 2)[0].size))

        self.proposal_set.set_values_of_one_attribute('is_chosen', 
                                                      choices, 
                                                      index=agents_index)
        
        #DevelopmentProjectProposalSamplingModel.run(self, n=n)
 
    def prepare_for_run(self, 
                        specification_storage=None, 
                        specification_table=None,
                        coefficients_storage=None,
                        coefficients_table=None,
                        data_objects=None,
                        **kwargs):
        
        spec, coeff = prepare_specification_and_coefficients(specification_storage=specification_storage,
                                               specification_table=specification_table, 
                                               coefficients_storage=coefficients_storage,
                                               coefficients_table=coefficients_table, **kwargs)
        return (spec, coeff)
        
    def prepare_for_estimate(self, specification_dict = None, 
                             specification_storage=None, 
                             specification_table=None,
                             agent_set=None, 
                             agents_for_estimation_storage=None,
                             agents_for_estimation_table=None,
                             filter_for_estimation_set=None,
                             data_objects=None):
        specification = get_specification_for_estimation(specification_dict, 
                                                         specification_storage, 
                                                         specification_table)
        if self.filter is not None:
            agents_index = where( self.proposal_set.compute_variables(self.filter) )[0]        
        
        id_attribute_name = ['parcel_id', 'template_id', 'is_redevelopment']
        if agents_for_estimation_storage is not None:
            estimation_set = Dataset(in_storage = agents_for_estimation_storage, 
                                     in_table_name=agents_for_estimation_table,
                                     id_name=id_attribute_name, 
                                     dataset_name=agent_set.get_dataset_name())
            
            filter_index = arange(estimation_set.size())
            if filter_for_estimation_set:
                filter_index = where(estimation_set.compute_variables(filter_for_estimation_set, resources=Resources(data_objects)))[0]
                estimation_set.subset_by_index(filter_index, flush_attributes_if_not_loaded=False)
                
            id_attributes = None
            for attr_name in id_attribute_name:
                attr_value = agent_set.get_attribute_as_column(attr_name)
                if id_attributes == None:
                    id_attributes = attr_value
                else:
                    id_attributes = concatenate((id_attributes, attr_value), axis=1)
                    
            id_index = estimation_set.try_get_id_index(id_attributes, return_value_if_not_found=-1)

            status_id = 2 * ones(agent_set.size(), dtype="int8")
            status_id[where(id_index != -1)] = 1
            name = self.choice_attribute_name.get_alias()
            if name in agent_set.get_known_attribute_names():
                agent_set.set_values_of_one_attribute(name, status_id[where(id_index != -1)], where(id_index!=-1)[0])
            else:
                agent_set.add_primary_attribute(status_id, name)
            
        return (specification, agents_index)
