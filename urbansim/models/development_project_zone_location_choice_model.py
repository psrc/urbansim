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

from urbansim.models.location_choice_model import LocationChoiceModel
from urbansim.datasets.development_event_dataset import DevelopmentEventDataset
from urbansim.datasets.development_project_dataset import DevelopmentProjectCreator
from opus_core.logger import logger

class DevelopmentProjectZoneLocationChoiceModel(LocationChoiceModel):
    
    model_name = "Development Project Zone Location Choice Model"
    model_short_name = "DPZLCM"
    
    def __init__(self, location_set, project_type, units,
                 model_name=None, **kargs):
        """
        'project_type' is a string such as 'Residential', or 'Commercial'.
        """
        self.project_type = project_type
        self.units = units
        if model_name is not None:
            self.model_name = model_name
        else:
            self.model_name = "%s %s" % (self.project_type, self.model_name)
        self.model_short_name = "%s %s" % (self.project_type[:3], self.model_short_name)
        
        LocationChoiceModel.__init__(self, location_set=location_set, **kargs)
        
    def run(self, *args, **kargs):
        agent_set = kargs["agent_set"]
        if agent_set is None:
            logger.log_status("No development projects for this model") 
            return None
        logger.log_status("project size: %d" % (agent_set.get_attribute(agent_set.get_attribute_name()).sum()))
        LocationChoiceModel.run(self, *args, **kargs)
                
    def prepare_for_estimate(self, specification_dict = None, specification_storage=None, 
                              specification_table=None, 
                              events_for_estimation_storage=None,
                              events_for_estimation_table=None, urbansim_constant=None, base_year=0,
                              categories=None):
                                  
        from opus_core.model import get_specification_for_estimation
        specification = get_specification_for_estimation(specification_dict, 
                                                          specification_storage, 
                                                          specification_table)
        projects = None                                                  
        # create agents for estimation        
        if events_for_estimation_storage is not None:                
            event_set = DevelopmentEventDataset(urbansim_constant,
                                            in_storage = events_for_estimation_storage, 
                                            in_table_name= events_for_estimation_table)
            event_set.remove_non_recent_data(base_year, urbansim_constant['recent_years'])
            projects = DevelopmentProjectCreator().create_projects_from_history(
                                               event_set, self.project_type,
                                               self.units, categories) 
        return (specification, projects)                                                                                             