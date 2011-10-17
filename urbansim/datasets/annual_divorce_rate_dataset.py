# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.rate_dataset import RateDataset

class AnnualDivorceRateDataset(RateDataset):
    id_name_default = []
    dataset_name = "annual_divorce_rate"
    probability_attribute = "divorce_probability"
    in_table_name_default = "annual_divorce_rates"
    out_table_name_default = "annual_divorce_rates"