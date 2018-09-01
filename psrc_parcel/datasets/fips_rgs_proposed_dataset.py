# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class FipsRgsProposedDataset(UrbansimDataset):

    id_name_default = "fips_rgs_proposed_id"
    in_table_name_default = "fips_rgs_proposed"
    out_table_name_default = "fips_rgs_proposed"
    dataset_name = "fips_rgs_proposed"

    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)