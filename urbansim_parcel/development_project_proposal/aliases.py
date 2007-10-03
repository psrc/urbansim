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

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "construction_cost_per_unit = development_project_proposal.disaggregate(urbansim_parcel.development_template.construction_cost_per_unit)",
   "construction_cost = (urbansim_parcel.development_project_proposal.construction_cost_per_unit * urbansim_parcel.development_project_proposal.units_proposed).astype(float32)",
   "total_revenue = (urbansim_parcel.development_project_proposal.building_sqft * development_project_proposal.unit_price_expected).astype(float32)",
   "unit_price = development_project_proposal.disaggregate(urbansim_parcel.parcel.unit_price)",
   "existing_units = development_project_proposal.disaggregate(urbansim_parcel.parcel.existing_units)",
   "acquisition_cost = (urbansim_parcel.development_project_proposal.unit_price * urbansim_parcel.development_project_proposal.existing_units).astype(float32)",
   "total_investment = (urbansim_parcel.development_project_proposal.acquisition_cost + urbansim_parcel.development_project_proposal.demolition_cost + urbansim_parcel.development_project_proposal.construction_cost).astype(float32)",
   "profit = urbansim_parcel.development_project_proposal.total_revenue - urbansim_parcel.development_project_proposal.total_investment",
   "building_sqft = (development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.building_sqft)).astype(float32)",
   "number_of_components = (development_project_proposal.number_of_agents(development_project_proposal_component)).astype(int32)",
   "demolition_cost = development_project_proposal.disaggregate(urbansim_parcel.parcel.demolition_cost) * development_project_proposal.is_redevelopment",
    ]
