# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.choice_model import ChoiceModel

class AutoOwnershipChoiceModel(ChoiceModel):
    """
    """
    model_name = "Auto Ownership Choice Model"
    model_short_name = "AOCM"
    
    def prepare_for_estimate(self, 
                             specification_dict = None, 
                             specification_storage=None, 
                             specification_table=None):
        from opus_core.model import get_specification_for_estimation
        return get_specification_for_estimation(specification_dict, 
                                                specification_storage, 
                                                specification_table)
