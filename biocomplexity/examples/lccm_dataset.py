# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.opus_package_info import package
import os

parent_dir_path = package().get_package_parent_path()

flt_directory = os.path.join(parent_dir_path, "LCCM_small_test_set_opus", "1991")
if __name__ == "__main__":
    lc =  LandCoverDataset(in_storage = StorageFactory().get_storage("flt_storage", storage_location = flt_directory))
    lc.summary()
    for attr in lc.get_attribute_names():
        print attr
        lc.plot_map(attr, main=attr)