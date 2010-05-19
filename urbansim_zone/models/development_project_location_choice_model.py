# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
from opus_core.model import get_specification_for_estimation
from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from opus_core.logger import logger
from numpy import where
import re

class DevelopmentProjectLocationChoiceModel(AgentLocationChoiceModel):

    model_name = "Development Project Location Choice Model"
    model_short_name = "DPLCM"
    
    def run(self, *args, **kwargs):
        if 'agent_set' in args and args['agent_set'] is None:
            logger.log_status("Development project dataset is empty. Skip DPLCM")
            return
        elif kwargs.has_key('agent_set') and kwargs['agent_set'] is None:
            logger.log_status("Development project dataset is empty. Skip DPLCM")
            return
        else:
            return AgentLocationChoiceModel.run(self, *args, **kwargs)
        
    def prepare_for_estimate(self, specification_dict = None, 
                             specification_storage=None,
                             specification_table=None,
                             events_for_estimation_storage=None,
                             events_for_estimation_table=None, 
                             agents_filter='',
                             compute_variables=[],
                             data_objects={}):

        specification = get_specification_for_estimation(specification_dict,
                                                          specification_storage,
                                                          specification_table)
        projects = None
        # create agents for estimation
        if events_for_estimation_storage is not None:
            projects = Dataset(in_storage = events_for_estimation_storage,
                               in_table_name= events_for_estimation_table,
                               id_name=[], dataset_name='development_project'
                               )
            if compute_variables:
                projects.compute_variables(compute_variables, resources=Resources(data_objects))
                # needs to be a primary attribute because of the join method below
                #projects.add_primary_attribute(estimation_set.get_attribute(location_id_variable), 
                #                               VariableName(location_id_variable).get_alias())
            
            if agents_filter:
                values = projects.compute_variables(agents_filter, resources=Resources(data_objects))
                index = where(values > 0)[0]
                projects.subset_by_index(index, flush_attributes_if_not_loaded=False)
                
        return (specification, projects)
    