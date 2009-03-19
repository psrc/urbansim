# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import where, ones, logical_and, array, median, resize
from opus_core.misc import unique_values
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingSqftPerJobDataset(UrbansimDataset):
    
    id_name_default = ["zone_id","building_type_id"]
    in_table_name_default = "building_sqft_per_job"
    out_table_name_default = "building_sqft_per_job"
    dataset_name = "building_sqft_per_job"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
    def get_building_sqft_as_table(self, zone_max=0, building_type_max=0):
        """Return a 2-d array (zone.max x buildong_type.max) filled with values from 
         the 'building_sqft_per_job' attribute. Missing combinations are filled with 
         the mean over all values. zone_max and building_type_max are optional maximum values
         for the dimensions of the table.
         """
        zone_ids = self.get_attribute("zone_id").astype("int32")
        bts = self.get_attribute("building_type_id")
        sqft = self.get_attribute("building_sqft_per_job")
        table = resize(array([sqft.mean()]), (max(zone_ids.max(), zone_max) + 1, 
                                              max(bts.max(), building_type_max) + 1))
        table[zone_ids, bts] = sqft
        return table
    
def create_building_sqft_per_job_dataset(dataset_pool, minimum_median=25, maximum_median=2000):
    buildings = dataset_pool.get_dataset('building')
    jobs = dataset_pool.get_dataset('job')
    job_sqft = jobs.get_attribute('sqft')
    has_sqft = job_sqft > 0
    job_building_index = buildings.try_get_id_index(jobs.get_attribute('building_id'))
    is_valid = logical_and(job_building_index >= 0, has_sqft)
    job_building_index = job_building_index[is_valid]
    sqft_of_jobs = buildings.sum_over_ids(jobs.get_attribute("building_id")[is_valid], job_sqft[is_valid])
    building_zones = buildings.get_attribute("zone_id")
    building_types = buildings.get_attribute("building_type_id")
    unique_zones = unique_values(building_zones)
    unique_types = unique_values(building_types)
    result_zone = []
    result_bt = []
    result_sqft = []
    for zone in unique_zones:
        is_zone = building_zones == zone
        for bt in unique_types:
            is_bt = logical_and(is_zone, building_types == bt)
            if (is_bt.sum() > 0) and sqft_of_jobs[is_bt].sum() > 0:
                result_zone.append(zone)
                result_bt.append(bt)
                mid = min(maximum_median, max(minimum_median, round(median(job_sqft[is_valid][is_bt[job_building_index]]))))
                result_sqft.append(mid)
                
    storage = StorageFactory().get_storage('dict_storage')
    storage.write_table(
            table_name='building_sqft_per_job',
            table_data={
                        "zone_id": array(result_zone),
                        "building_type_id" : array(result_bt),
                        "building_sqft_per_job": array(result_sqft, dtype="int32")
                        }
                        )
    return BuildingSqftPerJobDataset(in_storage=storage)