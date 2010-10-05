# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_iv_residual import abstract_iv_residual

class ln_price_residual(abstract_iv_residual):
    """"""
    p = "ln(urbansim_parcel.building.price_per_unit)"
    iv = "ln(urbansim_parcel.building.avg_price_per_unit_in_zone)"
    filter = "numpy.logical_and(urbansim_parcel.building.building_id>0, urbansim_parcel.building.price_per_unit > 0)"
