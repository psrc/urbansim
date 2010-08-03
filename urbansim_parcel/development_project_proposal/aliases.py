# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "construction_cost = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.construction_cost)",
   "total_revenue = (urbansim_parcel.development_project_proposal.building_sqft * development_project_proposal.unit_price_expected).astype(float32)",
   "unit_price = development_project_proposal.disaggregate(urbansim_parcel.parcel.unit_price)",
   "existing_units = development_project_proposal.disaggregate(urbansim_parcel.parcel.existing_units)",
   "total_investment = (urbansim_parcel.development_project_proposal.acquisition_cost + urbansim_parcel.development_project_proposal.demolition_cost + urbansim_parcel.development_project_proposal.construction_cost).astype(float32)",
   "profit = urbansim_parcel.development_project_proposal.total_revenue - urbansim_parcel.development_project_proposal.total_investment",
   "building_sqft = (development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.building_sqft)).astype(float32)",
   "number_of_components = (development_project_proposal.number_of_agents(development_project_proposal_component)).astype(int32)",
   "demolition_cost = development_project_proposal.disaggregate(urbansim_parcel.parcel.demolition_cost) * development_project_proposal.is_redevelopment",
   "faz_id = development_project_proposal.disaggregate(zone.faz_id, intermediates=[zone])",
   "zone_id = development_project_proposal.disaggregate(parcel.zone_id)",
   "large_area_id = development_project_proposal.disaggregate(parcel.large_area_id)",
    ]
