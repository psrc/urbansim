# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from psrc_parcel.data_preparation.unroll_jobs_from_establishments import UnrollJobsFromEstablishments
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_type import AttributeType
from numpy import zeros, ones
import os

class UnrollJobsFromGrowthSummary(UnrollJobsFromEstablishments):
    
    number_of_jobs_attr = "jobs"
    sqft_attr = "_unused_sqft"
    geography_id_attr = "_unused_geography_id"
    compute_sqft_per_job = False
    unplace_jobs_with_non_existing_buildings = False
    
if __name__ == '__main__':
    data_dir = "D:\documents\work\psrc\jobs_for_estimation"
    growth_table = "GrowthJobs"
    business_table = 'pseudo_businesses'
    storage = StorageFactory().get_storage('csv_storage', storage_location=data_dir)
    if not os.path.exists(os.path.join(data_dir, business_table + ".csv")):
        ## add attributes required by the UnrollJobsFromEstablishments class
        growth_dataset = Dataset(in_storage=storage, id_name=["parcel_id", "sector_id"], in_table_name=growth_table)
        growth_dataset._create_hidden_id()
        
        n = growth_dataset.size()
        id = growth_dataset.get_attribute('_hidden_id_')
        growth_dataset.add_primary_attribute(id, 'business_id')
        growth_dataset.add_primary_attribute(zeros(n, dtype='i'), '_unused_sqft')
        growth_dataset.add_primary_attribute(ones(n, dtype='i'), '_unused_geography_id')
        
        growth_dataset.write_dataset(attributes=AttributeType.PRIMARY, out_storage=storage, out_table_name=business_table)
    
    UnrollJobsFromGrowthSummary().run(storage, storage, business_table=business_table, control_totals_table=None)