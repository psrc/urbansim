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

from opus_core.datasets.dataset import Dataset
from opus_core.resources import Resources
from urbansim.models.agent_location_choice_model import AgentLocationChoiceModel
from urbansim_parcel.models.work_at_home_choice_model import prepare_for_estimate
from opus_core.model import get_specification_for_estimation
from numpy import arange, where
from opus_core.variables.variable_name import VariableName

class WorkplaceChoiceModel(AgentLocationChoiceModel):
    """
    """
    model_name = "Workplace Choice Model"
    model_short_name = "WCM"
    
    def prepare_for_estimate(self, *args, **kwargs):
        return prepare_for_estimate(*args, **kwargs)
