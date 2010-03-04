# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.abstract_variables.abstract_iv_residual import abstract_iv_residual

class price_residual(abstract_iv_residual):
    """"""
    p = "building.average_value_per_unit"
    iv = "urbansim_zone.building.average_value_per_unit_in_faz"
    filter = "building.building_id>0"

