# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import *
import numpy
from .constants import *

def setup_dataset_pool(opus=True, btype=None, submarket_info=None, esubmarket_info=None ):
    proforma_inputs = {            
        #'parcel':
        #    {
        #        "parcel_id":        array([1]),
        #        "property_tax":     array([0.01]),
        #        "land_cost":        array([ 1]) * 100000, #Land + other equity
        #    },
            
            'proposal_component':
            {
               "proposal_component_id": array([1,  2,  3,  4,  5]),
               "proposal_id":           array([1,  1,  1,  1,  1]),
               "building_type_id":      array([1,  1,  1,  1,  5]),  
               "bedrooms":              array([1,  2,  3,  4,  0]),
               "sales_revenue":         array([2,  3,  4,  5,  0]) * 1000000, 
               "sales_absorption":      array([.25,0.3,0.35,0.4,  0]), #* 1000000,
               "rent_revenue":          array([ .1,0.2,0.3,0.4,  0]) * 1000000,
               "leases_revenue":        array([  0,  0,  0,  0,  4]) * 1000000,
                #"rent_absorption":       array([  8,  4,  4,  8,  8]),
                #"leases_absorption":     array([  0,  0,  0,  0,  8]),
               'rent_absorption':      array([  8,  4,  4,  8, 1]),
               'leases_absorption':    array([  1,  1,  1,  1,  6]),
                #vacany rates for residential units for sale; not used by proforma
               "sales_vacancy_rates":  array([ 1.0, 0.5, 0.25, 1.0,  0.0]),  
               "vacancy_rates":         array([ 1.0, 0.5, 0.25, 1.0,  0.6]), # / 12,
               "operating_cost":        array([0.2,0.2,0.2,0.2, 0.1]),

                ##below are supposedly computed attributes; converted to primary attributes for speed
                "rent_revenue_per_period":   array([0, 0, 0, 0, 0]),
                "leases_revenue_per_period": array([0, 0, 0, 0, 0]),
             },

            'proposal':
            {
             
               "proposal_id":array([1]),
               "parcel_id":array([1]),
               "construction_start_period":array([ 1]),
               "sales_start_period":    array([ 5]),
               "rent_sqft":             array([ 75]) * 100,
               "total_sqft":            array([ 75]) * 100,
               "construction_cost":     array([ 30]) * 1000000,
               "public_contribution":   array([ 0.0]),

                ##below are supposedly computed attributes; converted to primary attributes for speed
                "property_tax":     array([0]),
                "land_cost":        array([ 1]) * 100000, #Land + other equity

                "sales_revenue":         array([ 0.0]),
                "sales_revenue_per_period": array([ 0.0]),
                "rent_revenue":             array([ 0.0]),
                "rent_revenue_per_period":  array([0.0]),
                "rent_vacancy_per_period":  array([0.0]),
                "rent_operating_cost_per_period": array([0.0]),
                "leases_revenue":           array([0.0]),
                "leases_revenue_per_period":array([0.0]),
                "leases_vacancy_per_period":array([0.0]),
                "leases_operating_cost_per_period": array([0.0])

            },
    }
    
    mixed_type = [12]
    if submarket_info is not None:
        bldg_type = devmdltypes[btype-1]
        proposal_comp = proforma_inputs['proposal_component']
        for i in range(proposal_comp['proposal_component_id'].size):
            #bldg_type = proposal_comp['building_type_id'][i]
            submarket_sales_idx = numpy.logical_and( submarket_info['building_type'] == bldg_type,
                                                     submarket_info['tenure_id'] == 2)
            submarket_rent_idx = numpy.logical_and( submarket_info['building_type'] == bldg_type,
                                                    submarket_info['tenure_id'] == 1)
            esubmarket_idx = esubmarket_info['building_type_id'] == bldg_type

            if submarket_sales_idx.sum() == 1:
                v_sales = submarket_info['sales_absorption'][submarket_sales_idx]
                if v_sales != 0: 
                    proposal_comp['sales_absorption'][i] = v_sales
                if bldg_type in residential_building_types:
                    k_sales = submarket_info['vacancy_rates'][submarket_sales_idx]
                    proposal_comp['sales_vacancy_rates'][i] = k_sales

            elif submarket_sales_idx.sum() > 1:
                raise ValueError("more than 1 submarkets matched to proposal_component %s" % proposal_comp['proposal_component_id'][i])
            #use default if the building_type & tenure isn't in submarket (submarket_sales_idx.size==0)

            if submarket_rent_idx.sum() == 1:
                v_rent = submarket_info['rent_absorption'][submarket_rent_idx]
                if v_rent != 0: 
                    proposal_comp['rent_absorption'][i] = round(1.0 / v_rent)
                if bldg_type in residential_building_types:
                    k_rent = submarket_info['vacancy_rates'][submarket_rent_idx]
                    proposal_comp['vacancy_rates'][i] = k_rent
            elif submarket_sales_idx.sum() > 1:
                raise ValueError("more than 1 submarkets matched to proposal_component %s" % proposal_comp['proposal_component_id'][i])

            if esubmarket_idx.sum() == 1:
                v_leases = esubmarket_info['leases_absorption'][esubmarket_idx]
                if v_leases != 0: 
                    proposal_comp['leases_absorption'][i] = round(1.0 / v_leases)
                if bldg_type not in residential_building_types:
                    k_leases = esubmarket_info['vacancy_rates'][esubmarket_idx]
                    proposal_comp['vacancy_rates'][i] = k_leases
            elif esubmarket_idx.sum() > 1:
                raise ValueError("more than 1 submarkets matched to proposal_component %s" % proposal_comp['proposal_component_id'][i])
            
        ## adjust for quarter/month
        proposal_comp['sales_absorption'] = proposal_comp['sales_absorption'] / 4
        proposal_comp['rent_absorption'] = proposal_comp['rent_absorption'] * 4
        proposal_comp['leases_absorption'] = proposal_comp['leases_absorption'] * 4
        proposal_comp['sales_vacancy_rates'] = proposal_comp['sales_vacancy_rates'] / 12
        proposal_comp['vacancy_rates'] = proposal_comp['vacancy_rates'] / 12

        #print "sales absorption", proposal_comp['sales_absorption']
        #print "rent absorption", proposal_comp['rent_absorption']
        #print "vacancy rates", proposal_comp['vacancy_rates']

    if opus:
        from opus_core.tests.utils import variable_tester
        po=['urbansim_parcel','urbansim']
        v = variable_tester.VariableTester('proforma.py',po,proforma_inputs)
        dataset_pool = v.dataset_pool
    else:
        dataset_pool = proforma_inputs
    return dataset_pool
