#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

sampled_shares = {
4: 0.007159353,
11: 0.02517321,
12: 0.037413395, 
19: 0.930254042,
}

observed_shares = {
4: 0.080947425, #condo
11:0.019761348, #mobile home
12:0.230847302, #mfh
19:0.668443925, #sfh
}




      
observed_share_var = "observed_building_type_share = %s * (urbansim.building.building_type_id == %s)" % (observed_shares[observed_shares.keys()[0]],
                                                                                                     observed_shares.keys()[0])
sampled_share_var = "sampled_building_type_share = %s * (urbansim.building.building_type_id == %s)" % (sampled_shares[sampled_shares.keys()[0]],
                                                                                                     sampled_shares.keys()[0])
for bt in observed_shares.keys()[1:len(observed_shares.keys())]:
    observed_share_var = observed_share_var + " + %s * (urbansim.building.building_type_id == %s)" % (observed_shares[bt], bt)
    sampled_share_var = sampled_share_var + " + %s * (urbansim.building.building_type_id == %s)" % (sampled_shares[bt], bt)
                   
aliases = [
       observed_share_var,
       sampled_share_var,
       "wesml_sampling_correction_variable = safe_array_divide(psrc_parcel.building.observed_building_type_share, psrc_parcel.building.sampled_building_type_share)",
       "district_id = building.disaggregate(zone.district_id, intermediates=[parcel])",
           ]
