# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model import Model
from numpy import arange, where, ones
from opus_core.sampling_toolbox import sample_replace

class TourScheduleModel(Model):
    model_name = "Tour Schedule Model"
    model_short_name = "TSM"
    
    def run(self, person_set, tour_set, person_index=None, tour_filter=None, dataset_pool=None):
        if person_index == None:
            person_index = arange(person_set.size())

        if tour_filter <> None:
            tour_index = where(tour_set.compute_variables(tour_filter))[0]
        else:
            tour_index = arange(tour_set.size())
        
        sampled_tour_id = sample_replace(tour_set.get_id_attribute()[tour_index],
                                        person_index.size,
                                        return_index=False)
        if 'tour_id' in person_set.get_known_attribute_names():
            person_set.set_values_of_one_attribute('tour_id', sampled_tour_id,
                                                   person_index)
        else:
            tour_id = -1 * ones(person_set.size(), dtype="int32")
            tour_id[person_index] = sampled_tour_id
            person_set.add_primary_attribute(tour_id, 'tour_id')

        return sampled_tour_id
