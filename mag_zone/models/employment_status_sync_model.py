# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from opus_core.models.model import Model
from opus_core.sampling_toolbox import sample_noreplace
from numpy import array, arange, where, zeros, ones, abs
from numpy.random import random
from opus_core.logger import logger

class EmploymentStatusSyncModel(Model):
    """
    Synchronize person's employment_status to match household workers count
    """
    model_name = "Employment Status Sync Model"
    model_short_name = "ESSM"

    def run(self, household, person, work_eligible='person.age>15', full_time_ratio=1.0, **kwargs):
        if 'employment_status' in person.get_known_attribute_names():
            employment_status = person['employment_status']
            assigned_workers = household.compute_variables('household.aggregate(person.employment_status)')
        else:
            employment_status = zeros(person.size(), dtype='i4')
            assigned_workers = zeros(household.size(), dtype='i4')

        if 'full_time' in person.get_known_attribute_names():
            full_time = person['full_time']
        else:
            full_time = zeros(person.size(), dtype='i4')

        predicted_workers = household['workers']

        diff = predicted_workers - assigned_workers
        indices = where(diff != 0)[0]
        
        eligible = person.compute_variables(work_eligible)
        import pdb; pdb.set_trace()
        logger.log_status('Updating employment_status for {} workers in {} households'.format(abs(diff).sum(), indices.size))
        for index in indices:
            in_hh = person['household_id'] == household['household_id'][index]
            if diff[index] > 0:
                sample_pool = where( (~ employment_status) & eligible & in_hh )[0]
                new_workers = sample_noreplace(sample_pool, diff[index])
                employment_status[new_workers] = 1
                chance = random(new_workers.size)
                full_time[new_workers] = ((1 - full_time_ratio) < chance).astype('i4')
            else:
                sample_pool = where( (employment_status) & in_hh )[0]
                exit_workers = sample_noreplace(sample_pool, -diff[index])
                employment_status[exit_workers] = 0
                full_time[exit_workers] = -1

        if 'employment_status' in person.get_known_attribute_names():
            person.modify_attribute('employment_status', employment_status)
        else:
            person.add_primary_attribute(employment_status, 'employment_status')

        if 'full_time' in person.get_known_attribute_names():
            person.modify_attribute('full_time', full_time)
        else:
            person.add_primary_attribute(full_time, 'full_time')

