# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import logical_and, arange, array, where
from numpy.random import seed
from opus_core.misc import ismember
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.sampling_toolbox import sample_noreplace

class FltStorage:
    def get(self, location):
        storage = StorageFactory().get_storage('flt_storage', storage_location=location)
        return storage
    
class AssignJBLM:
    job_id_range = [1843795, 1863794]
    faz_worker_mapping = {1: ([315,405,505,506,605,606,2910,2925,2926,2927], 8353),
                          2: ([705,706,805,806,900,1000,1115,1120,1130,1200,2000], 4176),
                          3: ([205,206,325,1330,2215,2216,2225,2935,2936,2940], 6961)
                        }

    def run(self, dataset_pool):
        workers = dataset_pool['person']
        faz_ids = workers.compute_variables('faz_id = person.disaggregate(zone.faz_id, intermediates=[parcel, building, household])',
                                               dataset_pool=dataset_pool)
        is_worker = workers.compute_variables('urbansim_parcel.person.is_worker', dataset_pool=dataset_pool)
        workers_jobs = workers['job_id']
        job_ids = arange(self.job_id_range[0], self.job_id_range[1]+1)
        for area, values in self.faz_worker_mapping.items():
            fazes = array(values[0])
            amount = values[1]
            indicator = logical_and(ismember(faz_ids, fazes), is_worker)
            job_idx = where(job_ids > 0)[0]
            sampled_jobs = sample_noreplace(job_idx, amount)
            workers_idx = where(indicator > 0)[0]
            sampled_workers = sample_noreplace(workers_idx, amount)
            workers_jobs[sampled_workers] = job_ids[sampled_jobs]
            job_ids[sampled_jobs] = 0
            
        workers.modify_attribute(name='job_id', data=workers_jobs)
        
if __name__ == '__main__':
    input_cache =  "/Users/hana/workspace/data/psrc_parcel/JBLM/base_year_data/2000"
    output_cache =  "/Users/hana/workspace/data/psrc_parcel/JBLM/run/2000"
    instorage = FltStorage().get(input_cache)
    outstorage = FltStorage().get(output_cache)
    dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'], storage=instorage)
    seed(1)
    AssignJBLM().run(dataset_pool)
    dataset_pool['person'].write_dataset(out_storage=outstorage, attributes=1)
    print("Assignment finished.")
            
            
        