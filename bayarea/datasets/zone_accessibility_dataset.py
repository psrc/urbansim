# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ZoneAccessibilityDataset(UrbansimDataset):
    id_name_default = "taz"
    in_table_name_default = "zone_accessibility"
    out_table_name_default = "zone_accessibility"
    dataset_name = "zone_accessibility"

