#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
                                        return_indices=False)
        if 'tour_id' in person_set.get_known_attribute_names():
            person_set.set_values_of_one_attribute('tour_id', sampled_tour_id,
                                                   person_index)
        else:
            tour_id = -1 * ones(person_set.size(), dtype="int32")
            tour_id[person_index] = sampled_tour_id
            person_set.add_primary_attribute(tour_id, 'tour_id')

        return sampled_tour_id
