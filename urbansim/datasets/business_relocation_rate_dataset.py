# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from .rate_dataset import RateDataset

class BusinessRelocationRateDataset(RateDataset):

    id_name_default = ["sector_id"]
    dataset_name = "business_relocation_rate"
    probability_attribute = "business_relocation_probability"
    in_table_name_default = "annual_relocation_rates_for_business"
    out_table_name_default = "annual_relocation_rates_for_business"