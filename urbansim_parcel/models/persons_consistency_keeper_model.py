# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.model import Model
from psrc.datasets.person_dataset import PersonDataset
from numpy import where, arange, array, resize, logical_not, in1d
from opus_core.storage_factory import StorageFactory
from opus_core.sampling_toolbox import sample_replace

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
                                "age":   array([], dtype='int32'),
                                "job_id":   array([], dtype='int32')
                                #"work_nonhome_based":
                                #               array([], dtype='int32')
                            },
                    )
                persons = PersonDataset(in_storage=storage, in_table_name=persons_table_name)

            id_name = household_set.get_id_name()[0]
            person_hh_id_array = person_set.get_attribute(id_name)
            if expand_person_set:
                hh_ids = []
                member_ids = []
                job_ids = []
                ages = []
                #work_nonhome_based = []

                #because immigrant households are assigned household_id larger than previous max id
                #max_hh_id = person_hh_id_array.max()
                household_ids = household_set.get_id_attribute()
                #hh_indices = where(household_ids > max_hh_id)[0]
                #workers = household_set.get_attribute("workers")
                #for index in hh_indices:
                    #household_id = household_ids[index]
                    #if workers[index] > 0:
                        #hh_ids += [household_id] * workers[index]
                        #member_ids += range(1, workers[index]+1)
                        #job_ids += [-1] * workers[index]
                        #work_nonhome_based += [-1] * workers[index]

                #TODO: make this code works more robustly: above code depends on Household transition model
                #assigning new households with ids larger than max_id. (HS: Not sure why it's based on workers and not on persons)
                #Code below is extremely SLOW.
                #unique_persons_hh_ids = unique(person_hh_id_array)
                #workers = main_dataset.get_attribute("workers")
                #hh_indices = arange(main_dataset.size())

                #for index in hh_indices:
                    #household_id = id_array[index]
                    #if household_id not in unique_persons_hh_ids:
                        #if workers[index] > 0:
                            #hh_ids += [household_id] * workers[index]
                            #member_ids += range(1, workers[index]+1)
                            #job_ids += [-1] * workers[index]


                hh_indices = where(logical_not(in1d(household_ids, person_hh_id_array)))[0]
                if hh_indices.size > 0:
                    npersons = household_set.get_attribute("persons")
                    age_of_head = household_set.get_attribute("age_of_head")
                    for index in hh_indices:
                        household_id = household_ids[index]
                        hh_ids += [household_id] * npersons[index]
                        member_ids += range(1, npersons[index]+1)
                        ages += [age_of_head[index]]
                        if npersons[index] > 1:
                            ages += [age_of_head[index] - sample_replace(arange(5), 1)[0]]
                            if npersons[index] > 2:
                                ages += (max(28, age_of_head[index]) - 20 - sample_replace(arange(8), npersons[index] - 2)).tolist()
    
    
                    new_persons = {"person_id":arange(len(hh_ids)) + person_set.get_id_attribute().max() + 1,
                                   "household_id":array(hh_ids),
                                   "member_id":array(member_ids),
                                   #"job_id":array(job_ids),
                                   "job_id": array([-1] * len(hh_ids)),
                                   "age": array(ages)
                                   }
                    if "work_at_home" in person_set.get_known_attribute_names():
                        new_persons["work_at_home"] = array([-1] * len(hh_ids))
                    person_set.add_elements(new_persons, require_all_attributes=False)

            #delete a person from person set if its household_id is not in households
            person_attr_index = household_set.try_get_id_index(person_hh_id_array, return_value_if_not_found=-9)
            eliminate_index = where(person_attr_index==-9)[0]
            person_set.remove_elements(eliminate_index)

        return person_set


from opus_core.tests import opus_unittest
from numpy import array, int32, int8, ma, all, allclose, zeros, ones
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim_parcel.datasets.person_dataset import PersonDataset
from opus_core.storage_factory import StorageFactory
    
class Tests(opus_unittest.OpusTestCase):

    def setUp(self):
        #1) 6000 households with age_of_head < 50, income < 40,000, persons < 3.
        #2) 2000 households with age_of_head < 50, income < 40,000, persons >= 3.
        #3) 3000 households with age_of_head < 50, income >= 40,000, persons < 3.
        #4) 4000 households with age_of_head < 50, income >= 40,000, persons >= 3.
        #5) 2000 households with age_of_head >= 50, income < 40,000, persons < 3.
        #6) 5000 households with age_of_head >= 50, income < 40,000, persons >= 3.
        #7) 3000 households with age_of_head >= 50, income >= 40,000, persons < 3.
        #8) 8000 households with age_of_head >= 50, income >= 40,000, persons >= 3.

        households_data = {
            "household_id":arange(33000)+1,
            "age_of_head": array(6000*[40] + 2000*[45] + 3000*[25] + 4000*[35] + 2000*[50] + 5000*[60] +
                                3000*[75]+ 8000*[65], dtype=int32),
            "income": array(6000*[35000] + 2000*[25000] + 3000*[40000] + 4000*[50000] + 2000*[20000] +
                                5000*[25000] + 3000*[45000]+ 8000*[55000], dtype=int32),
            "persons": array(6000*[2] + 2000*[3] + 3000*[1] + 4000*[6] + 2000*[1] + 5000*[4] +
                                3000*[1]+ 8000*[5], dtype=int8),
            }
        
        import itertools
        hh_select = ones(households_data["persons"].size)
        hh_select[array(range(10) + range(11100, 11150))] = 0
        self.hh_index = where(hh_select)[0]
        self.hh_new_persons = where(hh_select == 0)[0]
        total_persons = households_data['persons'][self.hh_index].sum()
        job_ids = range(1, 5000)
        self.non_exist_jobs = range(16000, 17000)
        persons_data = {
            "person_id":arange(total_persons)+1,
            "household_id": array( list(itertools.chain.from_iterable([[i] * p for i,p in zip(households_data['household_id'][self.hh_index], households_data['persons'][self.hh_index])])) ),
            ## head of the household is the oldest
            "age": array( list(itertools.chain.from_iterable([range(a, a-p*2, -2) for a,p in zip(households_data['age_of_head'][self.hh_index], households_data['persons'][self.hh_index])])) ),
            "job_id": array(job_ids + self.non_exist_jobs + [0] * (total_persons - len(job_ids) - len(self.non_exist_jobs)))
            }
        
        job_data = {
            "job_id":arange(15000)+1,
            "sector_id": array(1000*[1] + 1000*[1] + 2000*[1] + 1000*[1] +
                            2000*[2] + 1000*[2] + 1000*[2]+ 1000*[2] +
                            1000*[3] + 1000*[3] + 2000*[3] + 1000*[3])
            }
        
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='hh_set', table_data=households_data)
        self.hh_set = HouseholdDataset(in_storage=storage, in_table_name='hh_set')
        
        storage.write_table(table_name='person_set', table_data=persons_data)
        self.person_set = PersonDataset(in_storage=storage, in_table_name='person_set')            
      
        storage.write_table(table_name='job_set', table_data=job_data)
        self.job_set = JobDataset(in_storage=storage, in_table_name='job_set')            
        
    def test_create_persons(self):
        model = PersonDatasetConsistencyKeeperModel()
        orig_pers_size = self.person_set.size()
        new_pers = model.run(self.person_set, self.hh_set)
        self.assert_(new_pers.size() == orig_pers_size + self.hh_set["persons"][self.hh_new_persons].sum())
            
    def test_delete_persons(self):
        model = PersonDatasetConsistencyKeeperModel()
        persons_to_remove = self.hh_set["persons"][arange(50, 100)].sum()
        self.hh_set.remove_elements(arange(50, 100))
        orig_pers_size = self.person_set.size()
        new_pers = model.run(self.person_set, self.hh_set, expand_person_set = False)
        self.assert_(new_pers.size() == orig_pers_size - persons_to_remove)
        
    def test_delete_jobs(self):
        model = PersonDatasetConsistencyKeeperModel()
        self.assert_(in1d(self.person_set["job_id"], self.non_exist_jobs).sum() == len(self.non_exist_jobs))
        new_pers = model.run(self.person_set, self.hh_set, self.job_set, expand_person_set = False)
        self.assert_(in1d(self.person_set["job_id"], self.non_exist_jobs).sum() == 0)

        
if __name__=='__main__':
    opus_unittest.main()
