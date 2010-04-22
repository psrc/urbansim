# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.rate_dataset import RateDataset

class ChildLeavingHomeRateDataset(RateDataset):
    id_name_default = []
    dataset_name = "child_leaving_home_rate"
    probability_attribute = "probability"
    in_table_name_default = "child_leaving_home_rates"
    out_table_name_default = "child_leaving_home_rates"
