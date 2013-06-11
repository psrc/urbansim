# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_iv_residual import abstract_iv_residual

class price_residual(abstract_iv_residual):
    """"""
    p = "honolulu_parcel.employment_submarket.avg_price_per_unit_in_esubmarket"
    iv = "honolulu_parcel.employment_submarket.avg_price_per_unit_in_district"
    filter = "honolulu_parcel.employment_submarket.avg_price_per_unit_in_esubmarket > 0"
