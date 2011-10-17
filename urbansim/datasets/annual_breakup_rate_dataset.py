# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.rate_dataset import RateDataset

class AnnualBreakupRateDataset(RateDataset):
    id_name_default = []
    dataset_name = "annual_breakup_rate"
    probability_attribute = "breakup_probability"
    in_table_name_default = "annual_breakup_rates"
    out_table_name_default = "annual_breakup_rates"