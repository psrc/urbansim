# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.rate_dataset import RateDataset

class AnnualEduExitRateDataset(RateDataset):
    id_name_default = []
    dataset_name = "annual_edu_exit_rate"
    probability_attribute = "edu_exit_probability"
    in_table_name_default = "annual_edu_exit_rates"
    out_table_name_default = "annual_edu_exit_rates"