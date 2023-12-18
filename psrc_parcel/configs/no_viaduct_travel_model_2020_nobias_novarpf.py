# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from .baseline_travel_model_2020_nobias_novarpf import BaselineTravelModel2020NobiasNovarpf

class NoViaductTravelModel2020NobiasNovarpf(BaselineTravelModel2020NobiasNovarpf):
    tm_scenario = 'no_viaduct_v1.0bb_C1'
    