# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import arange, zeros, logical_and, where, array, ones, ma, resize
from scipy.ndimage import sum as ndimage_sum
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.misc import DebugPrinter, sample, unique
from opus_core.sampling_toolbox import probsample_replace
from opus_core.datasets.dataset import DatasetSubset
from opus_core.model import Model
from urbansim_parcel.models.scaling_jobs_model import ScalingJobsModel


class SubareaScalingJobsModel(ScalingJobsModel):
    """Run the urbansim ScalingJobsModel separately for each subarea."""
    model_name = "Subarea Scaling Jobs Model" 

    def __init__(self, subarea_id_name, **kwargs):
        super(SubareaScalingJobsModel, self).__init__(**kwargs)
        self.subarea_id_name = subarea_id_name
    
    def run(self, location_set, agent_set, agents_index=None, data_objects=None, **kwargs):
        if agents_index is None:
            agents_index = arange(agent_set.size())
        regions = agent_set.get_attribute(self.subarea_id_name)

        location_region = location_set.compute_one_variable_with_unknown_package(variable_name="%s" % (self.subarea_id_name), dataset_pool=self.dataset_pool)
        valid_region = where(regions[agents_index] > 0)[0]
        if valid_region.size > 0:
            unique_regions = unique(regions[agents_index][valid_region])
            cond_array = zeros(agent_set.size(), dtype="bool8")
            cond_array[agents_index[valid_region]] = True
            for area in unique_regions:
                new_index = where(logical_and(cond_array, regions == area))[0]
                self.filter = "%s.%s == %s" % (location_set.get_dataset_name(), self.subarea_id_name, area)
                logger.log_status("SJM for area %s" % area)
                ScalingJobsModel.run(self, location_set, agent_set, agents_index=new_index, **kwargs)

        no_region = where(regions[agents_index] <= 0)[0]
        if no_region.size > 0: # run the model for jobs that don't have assigned region
            self.filter = None
            logger.log_status("SJM for jobs with no area assigned")
            choices = ScalingJobsModel.run(self, location_set, agent_set, agents_index=agents_index[no_region], **kwargs)
            where_valid_choice = where(choices > 0)[0]
            choices_index = location_set.get_id_index(choices[where_valid_choice])
            chosen_regions = location_set.get_attribute_by_index(self.subarea_id_name, choices_index)
            agent_set.modify_attribute(name=self.subarea_id_name, data=chosen_regions, 
                                       index=no_region[where_valid_choice])
