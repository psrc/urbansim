# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

## Original code
##aliases = [
##           "minimum_1DU_per_legal_lot_yield = numpy.logical_and(%s, numpy.logical_and(%s, numpy.logical_and(%s, %s)))" % (
##             # variables connected by AND:
##             "urbansim_parcel.development_project_proposal.units_proposed_fraction <= 0.5",
##             "urbansim_parcel.development_project_proposal.units_proposed_fraction > 0",
##             "numpy.logical_not(development_project_proposal.disaggregate(urbansim_parcel.development_template.is_far))",
##             "numpy.logical_not(development_project_proposal.disaggregate(parcel.is_inside_urban_growth_boundary))",
##             ),
##            "units_proposed_plus_minimum_1DU_per_legal_lot_yield = %s + numpy.logical_and(%s, %s)" % (
##                    "urbansim_parcel.development_project_proposal.units_proposed",
##                    "psrc_parcel.development_project_proposal.minimum_1DU_per_legal_lot_yield",
##                    "development_project_proposal.disaggregate(parcel.parcel_sqft > 10000)")
##           ]




aliases = [
           # altered Hana's original script to define both a Rural and Urban legal lot - this is Rural
           "minimum_1DU_per_legal_rural_lot_yield = numpy.logical_and(%s, numpy.logical_and(%s, numpy.logical_and(%s, %s)))" % (
             # variables connected by AND:
             "urbansim_parcel.development_project_proposal.units_proposed_fraction <= 0.5",
             "urbansim_parcel.development_project_proposal.units_proposed_fraction > 0",
             "development_project_proposal.disaggregate(parcel.parcel_sqft > 9999)",
             "numpy.logical_not(development_project_proposal.disaggregate(parcel.is_inside_urban_growth_boundary))",
             ),
           #  Urban Legal Lot
           "minimum_1DU_per_legal_urban_lot_yield = numpy.logical_and(%s, numpy.logical_and(%s, numpy.logical_and(%s, %s)))" % (
             # variables connected by AND:
             "urbansim_parcel.development_project_proposal.units_proposed_fraction <= 0.5",
             "urbansim_parcel.development_project_proposal.units_proposed_fraction > 0",
             "development_project_proposal.disaggregate(parcel.parcel_sqft > 3499)",
             "development_project_proposal.disaggregate(parcel.is_inside_urban_growth_boundary)",
             ),

          #  This is the actual term called in the Project XML file - two above are defining variables used below
            "units_proposed_plus_minimum_1DU_per_legal_lot_yield = %s + numpy.logical_and(%s, numpy.logical_or(%s,%s))" % (
                    "urbansim_parcel.development_project_proposal.units_proposed",
                    "numpy.logical_not(development_project_proposal.disaggregate(urbansim_parcel.development_template.is_far))",
                    "psrc_parcel.development_project_proposal.minimum_1DU_per_legal_rural_lot_yield",
                    "psrc_parcel.development_project_proposal.minimum_1DU_per_legal_urban_lot_yield",
             ),
           ]
