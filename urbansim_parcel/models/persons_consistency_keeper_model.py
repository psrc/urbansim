# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.model import Model
from psrc.datasets.person_dataset import PersonDataset
from numpy import where, arange, array, resize
from opus_core.storage_factory import StorageFactory

## TODO: Is this class in use?

class PersonDatasetConsistencyKeeperModel(Model):
    """this model keeps consistency of between person/worker and job and between person and household datasets"""
    def run(self, person_set, household_set=None, job_set=None, expand_person_set=True, resources=None):
        """main_dataset is either household or job,

          if job_set is not None, it will set job_id of
        person/worker whose job 'disappears' to -1.

          if household_set is not None, it will expand personset 
          to include persons in households that just 'immigrate' 
          by household_transition_model, as well as eliminate 
          persons whose household has emmigrated;
        """

        if person_set is not None and job_set is not None:
            id_name = job_set.get_id_name()[0]
            person_job_id_array = person_set.get_attribute(id_name)
            person_attr_index = job_set.try_get_id_index(person_job_id_array, return_value_if_not_found=-9)
            index = where(person_attr_index==-9)[0]
            person_set.set_values_of_one_attribute("job_id", resize(array([-1], dtype="int32"), index.size), index=index)

        if household_set is not None:
            if person_set is None:
                storage = StorageFactory().get_storage('dict_storage')
                persons_table_name = 'persons'
                storage.write_table(
                        table_name=persons_table_name,
                        table_data={
                                "person_id":   array([], dtype='int32'),
                                "household_id":array([], dtype='int32'),
                                "member_id":   array([], dtype='int32'),
                                "work_nonhome_based":
                                               array([], dtype='int32')
                            },
                    )
                persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)

            id_name = household_set.get_id_name()[0]
            person_hh_id_array = person_set.get_attribute(id_name)
            if expand_person_set:
                hh_ids = []
                member_ids = []
                job_ids = []
                work_nonhome_based = []

                #because immigrant households are assigned household_id larger than previous max id
                max_hh_id = person_hh_id_array.max()
                household_ids = household_set.get_id_attribute()
                hh_indices = where(household_ids > max_hh_id)[0]
                workers = household_set.get_attribute("workers")
                for index in hh_indices:
                    household_id = household_ids[index]
                    if workers[index] > 0:
                        hh_ids += [household_id] * workers[index]
                        member_ids += range(1, workers[index]+1)
                        job_ids += [-1] * workers[index]
                        work_nonhome_based += [-1] * workers[index]

                #TODO: make this code works more robustly: above code depends on Household transition model
                #assigning new households with ids larger than max_id. Code below is extremely SLOW.
                #unique_persons_hh_ids = unique_values(person_hh_id_array)
                #workers = main_dataset.get_attribute("workers")
                #hh_indices = arange(main_dataset.size())

                #for index in hh_indices:
                    #household_id = id_array[index]
                    #if household_id not in unique_persons_hh_ids:
                        #if workers[index] > 0:
                            #hh_ids += [household_id] * workers[index]
                            #member_ids += range(1, workers[index]+1)
                            #job_ids += [-1] * workers[index]

                new_persons = {"person_id":arange(len(hh_ids)) + person_set.get_id_attribute().max() + 1,
                               "household_id":array(hh_ids),
                               "member_id":array(member_ids),
                               "job_id":array(job_ids),
                               "work_nonhome_based":array(work_nonhome_based)}
                person_set.add_elements(new_persons, require_all_attributes=False)

            #delete a person from person set if its household_id is not in households
            person_attr_index = household_set.try_get_id_index(person_hh_id_array, return_value_if_not_found=-9)
            eliminate_index = where(person_attr_index==-9)[0]
            person_set.remove_elements(eliminate_index)

        return person_set
