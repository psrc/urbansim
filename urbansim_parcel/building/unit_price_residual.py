# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_iv_residual import abstract_iv_residual

class unit_price_residual(abstract_iv_residual):
    """"""
    p = "urbansim_parcel.building.unit_price" 
    #iv = "urbansim_parcel.building.avg_price_per_sqft_in_zone" # IV
    iv = "urbansim_parcel.building.avg_price_per_sqft_in_faz" # IV
    filter = "building.building_id>0" 

