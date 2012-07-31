# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_iv_residual import abstract_iv_residual

class ln_price_residual(abstract_iv_residual):
    """"""
    p = "ln(bayarea.submarket.avg_price_per_unit_in_submarket)"
    iv = "ln(bayarea.submarket.avg_price_per_unit_in_county)"
    filter = "bayarea.submarket.avg_price_per_unit_in_submarket > 0"
