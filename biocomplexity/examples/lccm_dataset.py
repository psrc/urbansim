#
# Opus software. Copyright (C) 2005-2008 University of Washington
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


from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.opus_package_info import package
from opus_core.storage_factory import StorageFactory
import os

parent_dir_path = package().get_package_parent_path()

flt_directory = os.path.join(parent_dir_path, "biocomplexity", "data", "LCCM_small_test_set_opus", "1991")
if __name__ == "__main__":
    lc =  LandCoverDataset(in_storage = StorageFactory().get_storage("flt_storage", storage_location = flt_directory))
    lc.summary()
    for attr in lc.get_attribute_names():
        print attr
        lc.plot_map(attr, main=attr)