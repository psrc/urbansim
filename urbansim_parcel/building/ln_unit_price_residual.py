# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_iv_residual import abstract_iv_residual

class ln_unit_price_residual(abstract_iv_residual):
    """"""
    p = "ln_bounded(urbansim_parcel.building.unit_price)" 
    iv = "ln_bounded(urbansim_parcel.building.avg_price_per_sqft_in_zone)" # IV
    filter = "building.building_id>0" 

