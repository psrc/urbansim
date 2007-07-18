#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

from numpy import arange, zeros, logical_and, where
from opus_core.logger import logger
from opus_core.misc import unique_values
from urbansim.models.employment_location_choice_model import EmploymentLocationChoiceModel

class RegionalEmploymentLocationChoiceModel(EmploymentLocationChoiceModel):
    """Run the urbansim ELCM separately for each large area."""
    model_name = "Regional Employment Location Choice Model" 
    large_area_id_name = "large_area_id"
    
    def run(self, specification, coefficients, agent_set, agents_index=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        large_areas = agent_set.compute_variables(["washtenaw.%s.%s" % (agent_set.get_dataset_name(), self.large_area_id_name)],
                                                  dataset_pool=self.dataset_pool)
        self.choice_set.compute_variables(["washtenaw.%s.%s" % (self.choice_set.get_dataset_name(), self.large_area_id_name)],
                                                  dataset_pool=self.dataset_pool)
        unique_large_areas = unique_values(large_areas[agents_index])
        cond_array = zeros(agent_set.size(), dtype="bool8")
        cond_array[agents_index] = True
        for area in unique_large_areas:
            new_index = where(logical_and(cond_array, large_areas == area))[0]
            self.filter = "%s.%s == %s" % (self.choice_set.get_dataset_name(), self.large_area_id_name, area)
            logger.log_status("ELCM for area %s" % area)
            EmploymentLocationChoiceModel.run(self, specification, coefficients, agent_set, 
                                             agents_index=new_index, **kwargs)
