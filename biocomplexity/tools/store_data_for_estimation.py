# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE
    

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.opus_package_info import package
from opus_core.datasets.dataset import DatasetSubset
from opus_core.storage_factory import StorageFactory
from numpy import where
import os

parent_dir_path = package().get_package_parent_path()

# directory of the input data
flt_directory_in = os.path.join(parent_dir_path, "LCCM_4County")
#directory of the output data
#flt_directory_out = os.path.join(parent_dir_path, "LCCM_4County", "data_for_urban")
#flt_directory_out = os.path.join(parent_dir_path, "LCCM_4County", "data_for_suburban")
flt_directory_out = os.path.join(parent_dir_path, "LCCM_4County", "data_for_estimation_all")

index_attribute = "urbsamp95_99_0"
#index_attribute = "up91x95-old-samp0"
#index_attribute = "sall91-95-0"
index_attribute = "all_sample_95_99_0"
#index_attribute = "suburb91-95sample0"
#index_attribute = "suburb95-99sample0"

years = [1995, 1999]


lc1 =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = os.path.join(flt_directory_in, str(years[0]))),
    out_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = os.path.join(flt_directory_out, str(years[0]))))

agents_index = where(lc1.get_attribute(index_attribute))[0]
lc1subset = DatasetSubset(lc1, agents_index)
print "Writing set 1:"
for attr in lc1.get_primary_attribute_names():
    print "   ", attr
    lc1subset.write_dataset(attributes=[attr], out_table_name="land_covers")
    lc1.delete_one_attribute(attr)
    
lc2 =  LandCoverDataset(in_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = os.path.join(flt_directory_in, str(years[1]))),
    out_storage = StorageFactory().get_storage('flt_storage',
        storage_location = os.path.join(flt_directory_out, str(years[1]))))
                  
lc2subset = DatasetSubset(lc2, agents_index)
print "Writing set 2:"
for attr in lc2.get_primary_attribute_names():
    print "   ", attr
    lc2subset.write_dataset(attributes=[attr], out_table_name="land_covers")
    lc2.delete_one_attribute(attr)                  
print "done."