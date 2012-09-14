# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class ZoneGovEdJobDataset(UrbansimDataset):
    id_name_default = "zone_id"
    in_table_name_default = "zone_gov_ed_jobs"
    out_table_name_default = "zone_gov_ed_jobs"
    dataset_name = "zone_gov_ed_job"

