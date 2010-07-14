# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "building_sqft_per_unit = development_project_proposal_component.disaggregate(development_template_component.building_sqft_per_unit)",
   "percent_building_sqft = development_project_proposal_component.disaggregate(development_template_component.percent_building_sqft)",
   "is_residential = (development_project_proposal_component.disaggregate(building_type.is_residential)).astype('bool')",
   "is_non_residential = numpy.logical_not(development_project_proposal_component.disaggregate(building_type.is_residential))",
   "building_sqft = (urbansim_parcel.development_project_proposal_component.building_sqft_per_unit * urbansim_parcel.development_project_proposal_component.units_proposed).astype(int32)",
   "residential_units = (urbansim_parcel.development_project_proposal_component.units_proposed * urbansim_parcel.development_project_proposal_component.is_residential).astype(int32)",
   "non_residential_sqft = urbansim_parcel.development_project_proposal_component.building_sqft * urbansim_parcel.development_project_proposal_component.is_non_residential",
   "land_area_taken = urbansim_parcel.development_project_proposal_component.percent_building_sqft * (development_project_proposal_component.disaggregate(urbansim_parcel.development_project_proposal.land_area_taken) / 100.)",
#   "construction_cost = development_project_proposal_component.disaggregate(development_template_component.construction_cost_per_unit) * urbansim_parcel.development_project_proposal_component.units_proposed",
   "construction_cost = development_project_proposal_component.disaggregate(urbansim_parcel.development_template_component.component_construction_cost_per_unit) * urbansim_parcel.development_project_proposal_component.units_proposed",   
   "velocity_function_id = development_project_proposal_component.disaggregate(development_template_component.velocity_function_id)",
   "city_id = development_project_proposal_component.disaggregate(parcel.city_id, intermediates=[development_project_proposal])",
   "zone_id = development_project_proposal_component.disaggregate(urbansim_parcel.development_project_proposal.zone_id)",
   ]