# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class RegionalGeographyDataset(UrbansimDataset):

    id_name_default = "regional_geography_id"
    in_table_name_default = "regional_geography"
    out_table_name_default = "regional_geography"
    dataset_name = "regional_geography"

    def __init__(self, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)


