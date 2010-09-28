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

variables_for_development_project_proposal = {
    'ln_distance_to_highway' : 'ln_bounded(development_project_proposal.disaggregate(parcel.distance_to_highway))',
    'lnlotsqftunit' : '(ln_bounded(development_project_proposal.disaggregate(urbansim_parcel.parcel.parcel_sqft_per_unit))).astype(float32)',
    'lnsqft' : '(ln_bounded(development_project_proposal.disaggregate(urbansim_parcel.parcel.building_sqft))).astype(float32)',
    'lnsqftunit' : '(ln_bounded(development_project_proposal.disaggregate(urbansim_parcel.parcel.building_sqft_per_unit))).astype(float32)',
    'ln_bldgage' : '(ln_bounded(urbansim_parcel.development_project_proposal.building_age)).astype(float32)',
    'ln_existing_units' : '(ln_bounded(development_project_proposal.disaggregate(urbansim_parcel.parcel.existing_units))+urbansim_parcel.development_project_proposal.units_proposed).astype(float32)',
    'ln_number_of_jobs' : 'ln_bounded(development_project_proposal.disaggregate(parcel.aggregate(urbansim_parcel.building.number_of_jobs)))',
    'lnavginc' : '(ln_bounded(development_project_proposal.disaggregate(parcel.disaggregate(urbansim_parcel.zone.average_income)))).astype(float32)',
    'lnpopden' : '(ln_bounded(development_project_proposal.disaggregate(urbansim_parcel.zone.population_per_acre))).astype(float32)',
    'lnlotsqft' : '(ln_bounded(development_project_proposal.disaggregate(parcel.parcel_sqft))).astype(float32)',
    'ln_distance_to_art' : 'ln_bounded(development_project_proposal.disaggregate(parcel.distance_to_arterial))',
    'ln_invfar' : 'ln_bounded(development_project_proposal.disaggregate(safe_array_divide(parcel.parcel_sqft,(urbansim_parcel.parcel.building_sqft).astype(float32)))).astype(float32)',
    'lnunits' : '(development_project_proposal.disaggregate(urbansim_parcel.parcel.residential_units)).astype(float32)'
                                                }