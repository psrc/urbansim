#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

from baseline_travel_model_2020_nobias_novarpf import BaselineTravelModel2020NobiasNovarpf

class NoViaductTravelModel2020NobiasNovarpf(BaselineTravelModel2020NobiasNovarpf):
    tm_scenario = 'no_viaduct_v1.0bb_C1'
    