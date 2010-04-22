# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.rate_dataset import RateDataset

class MortalityRateDataset(RateDataset):
    id_name_default = []
    dataset_name = "annual_mortality_rate"
    probability_attribute = "mortality_probability"
    in_table_name_default = "annual_mortality_rates"
    out_table_name_default = "annual_mortality_rates"
