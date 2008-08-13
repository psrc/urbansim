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

from opus_core.resources import merge_resources_if_not_None
from urbansim.models.agent_relocation_model import AgentRelocationModel

class EmploymentRelocationModelCreator(object):
    def get_model(self, choices = "opus_core.random_choices",
                  probabilities = "urbansim.employment_relocation_probabilities",
                  location_id_name = "grid_id",
                  debuglevel=0):
        return AgentRelocationModel(probabilities = probabilities,
                                    choices = choices,
                                    location_id_name = location_id_name,
                                    model_name="Employment Relocation Model",
                                    debuglevel=debuglevel)