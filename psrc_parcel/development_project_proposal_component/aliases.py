# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 
                  
aliases = [
           "job_capacity_computed = safe_array_divide(urbansim_parcel.development_project_proposal_component.non_residential_sqft, urbansim_parcel.development_project_proposal_component.building_sqft_per_job)",
           "land_value = development_project_proposal_component.disaggregate(psrc_parcel.development_project_proposal.land_value)",
           "parcel_sqft = development_project_proposal_component.disaggregate(urbansim_parcel.development_project_proposal.parcel_sqft)",
           ]
