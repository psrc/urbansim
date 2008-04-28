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
from urbansim_parcel.models.scaling_jobs_model import ScalingJobsModel


class RegionalScalingJobsModel(ScalingJobsModel):
    """Run the urbansim ScalingJobsModel separately for each faz."""
    model_name = "Regional Scaling Jobs Model" 
    regional_id_name = "faz_id"
    
    def run(self, location_set, agent_set, agents_index=None, data_objects=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        regions = agent_set.get_attribute(self.regional_id_name)
        location_region = location_set.compute_variables(["urbansim_parcel.%s.%s" % (location_set.get_dataset_name(), self.regional_id_name)],
                                                  dataset_pool=self.dataset_pool)
        valid_region = where(regions[agents_index] > 0)[0]
        if valid_region.size > 0:
            unique_regions = unique_values(regions[agents_index][valid_region])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_region]] = True
            for area in unique_regions:
                new_index = where(logical_and(cond_array, regions == area))[0]
                self.filter = "%s.%s == %s" % (location_set.get_dataset_name(), self.regional_id_name, area)
                logger.log_status("SJM for area %s" % area)
                ScalingJobsModel.run(self, location_set, agent_set, agents_index=new_index, **kwargs)

        no_region = where(regions[agents_index] <= 0)[0]
        if no_region.size > 0: # run the model for jobs that don't have assigned region
            self.filter = None
            logger.log_status("SJM for jobs with no area assigned")
            choices = ScalingJobsModel.run(self, location_set, agent_set, agents_index=agents_index[no_region], **kwargs)
            where_valid_choice = where(choices > 0)[0]
            choices_index = location_set.get_id_index(choices[where_valid_choice])
            chosen_regions = location_set.get_attribute_by_index(self.regional_id_name, choices_index)
            agent_set.modify_attribute(name=self.regional_id_name, data=chosen_regions, 
                                       index=no_region[where_valid_choice])