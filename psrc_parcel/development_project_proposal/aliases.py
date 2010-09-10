# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "minimum_1DU_per_legal_lot_yield = %s + numpy.logical_and(%s, numpy.logical_and(%s, numpy.logical_and(%s, numpy.logical_and(%s, %s))))" % (           
             "urbansim_parcel.development_project_proposal.units_proposed",
             # variables connected by AND:
             "urbansim_parcel.development_project_proposal.units_proposed_fraction <= 0.5",
             "urbansim_parcel.development_project_proposal.units_proposed_fraction > 0",
             "numpy.logical_not(development_project_proposal.disaggregate(urbansim_parcel.development_template.is_far))",
             "numpy.logical_not(development_project_proposal.disaggregate(parcel.is_inside_urban_growth_boundary))",
             "development_project_proposal.disaggregate(parcel.parcel_sqft > 10000)")
           ]