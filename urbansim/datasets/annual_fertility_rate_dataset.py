# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.rate_dataset import RateDataset

class AnnualFertilityRateDataset(RateDataset):
    id_name_default = []
    dataset_name = "annual_fertility_rate"
    probability_attribute = "fertility_probability"
    in_table_name_default = "annual_fertility_rates"
    out_table_name_default = "annual_fertility_rates"
