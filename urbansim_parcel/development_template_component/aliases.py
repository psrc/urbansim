# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "portion_of_building = development_template_component.percent_building_sqft / 100.0", 
   ##TODO the value in building_sqft_per_unit column of development_template_components for PSRC is actually
   ## building_sqft_per_sqft.  Need to make it consistent
   "component_construction_cost_per_unit = (development_template_component.construction_cost_per_unit * development_template_component.building_sqft_per_unit).astype(float32)",
#   "construction_cost_per_component = (development_template_component.construction_cost_per_unit * urbansim_parcel.development_template_component.portion_of_building * development_template_component.building_sqft_per_unit).astype(float32)",   
      
   ]