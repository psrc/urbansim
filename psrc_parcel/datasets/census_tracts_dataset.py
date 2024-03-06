# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class CityDataset(UrbansimDataset):

    id_name_default = "census_tract_id"
    in_table_name_default = "census_tracts"
    out_table_name_default = "census_tracts"
    dataset_name = "census_tracts"

    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)