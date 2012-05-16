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
             "developable_capacity = clip_to_zero(development_project_proposal.disaggregate(psrc_parcel.parcel.max_developable_capacity)-urbansim_parcel.development_project_proposal.building_sqft)",
             #"acquisition_cost = clip_to_zero(development_project_proposal.disaggregate(parcel.total_value_per_sqft*parcel.parcel_sqft) - development_project_proposal.disaggregate(urbansim_parcel.parcel.improvement_value) * (development_project_proposal.is_redevelopment == 0))",
             "acquisition_cost = clip_to_zero(development_project_proposal.disaggregate(parcel.land_value + urbansim_parcel.parcel.improvement_value) - development_project_proposal.disaggregate(urbansim_parcel.parcel.improvement_value) * (development_project_proposal.is_redevelopment == 0))",
             "total_investment = (psrc_parcel.development_project_proposal.acquisition_cost + urbansim_parcel.development_project_proposal.demolition_cost + urbansim_parcel.development_project_proposal.construction_cost).astype(float32)",
             #"total_revenue = development_project_proposal.total_parcel_value_per_sqft * urbansim_parcel.development_project_proposal.parcel_sqft",
             #"total_revenue = development_project_proposal.parcel_land_value + urbansim_parcel.development_project_proposal.construction_cost",
             "total_revenue = development_project_proposal.expected_sales_price_per_sqft * urbansim_parcel.development_project_proposal.building_sqft",
             "profit = psrc_parcel.development_project_proposal.total_revenue - psrc_parcel.development_project_proposal.total_investment",
             "expected_rate_of_return_on_investment = safe_array_divide(psrc_parcel.development_project_proposal.profit, psrc_parcel.development_project_proposal.total_investment)",
             "land_value = development_project_proposal.disaggregate(parcel.land_value)",
             "prcl_imp_value = development_project_proposal.disaggregate(parcel.land_value + urbansim_parcel.parcel.improvement_value)"
           ]
