# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim_parcel.proposal.pycel.excelutil import *
from urbansim_parcel.proposal.pycel.excellib import *
from scipy.optimize import *
from numpy import array
from opus_core.logger import logger
from proforma import proforma
import copy

DEBUG = 0
SQFTFACTOR = 300.0
COMMERCIALTYPES_D = {7:82,8:82,9:79,10:80,11:81,12:83,13:84}
OBJCNT = 0

def setup_dataset_pool(opus=True, submarket_info=None):
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
                "property_tax":     array([0.01]),
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

    if submarket_info is not None:
        proposal_comp = proforma_inputs['proposal_component']
        for i in xrange(proposal_comp['proposal_component_id'].size):
            bldg_type = proposal_comp['building_type_id'][i]
            submarket_sales_idx = numpy.logical_and( submarket_info['building_type'] == bldg_type,
                                                     submarket_info['tenure_id'] == 2)
            submarket_rent_idx = numpy.logical_and( submarket_info['building_type'] == bldg_type,
                                                    submarket_info['tenure_id'] == 1)
            if submarket_sales_idx.sum() == 1:
                v = submarket_info['sales_absorption'][submarket_sales_idx]
                if v != 0: 
                    proposal_comp['sales_absorption'][i] = v 
            elif submarket_sales_idx.sum() > 1:
                raise ValueError, "more than 1 submarkets matched to proposal_component %s" % proposal_comp['proposal_component_id'][i]
            #use default if the building_type & tenure isn't in submarket (submarket_sales_idx.size==0)

            if submarket_rent_idx.sum() == 1:
                v = submarket_info['rent_absorption'][submarket_rent_idx]
                if v != 0: 
                    proposal_comp['rent_absorption'][i] = round(1 / v)
                proposal_comp['vacancy_rates'][i] = submarket_info['vacancy_rates'][submarket_rent_idx]
            elif submarket_sales_idx.sum() > 1:
                raise ValueError, "more than 1 submarkets matched to proposal_component %s" % proposal_comp['proposal_component_id'][i]
            
        ## adjust for quarter/month
        proposal_comp['sales_absorption'] = proposal_comp['sales_absorption']
        #proposal_comp['rent_absorption'] = 4/proposal_comp['rent_absorption']
        #proposal_comp['leases_absorption'] = 4/proposal_comp['leases_absorption']
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

def _objfunc2(params,bform,btype,prices,dataset_pool,baveexcel=0,excelprefix=None):

    global OBJCNT
    OBJCNT += 1    
    if len(params) >= 4: bform.set_num_units(array(params[:4]))
    if len(params) == 5: bform.set_nonres_sqft(params[4]*SQFTFACTOR)
    if len(params) == 1: bform.set_nonres_sqft(params[0]*SQFTFACTOR)

    #global PROFORMA_INPUTS
    #proforma_inputs = copy.copy(PROFORMA_INPUTS)
    X = params

    e = None
    if DEBUG > 1: print "PARAMS", params

    #d = proforma_inputs['proposal_component']
    if type(dataset_pool) == dict:
        proposal = dataset_pool['proposal']
        proposal_comp = dataset_pool['proposal_component']
    else:
        proposal = dataset_pool.get_dataset('proposal')
        proposal_comp = dataset_pool.get_dataset('proposal_component')

    d = {}
    d['sales_revenue'] =     array([  0,  0,  0,  0,  0])
    d['rent_revenue'] =      array([  0,  0,  0,  0,  0])
    d['leases_revenue'] =    array([  0,  0,  0,  0,  0])

    if btype in [1,2]: 
        d['sales_revenue'] = \
            prices[0]*numpy.append(X*bform.sfunitsizes,0)
    elif btype in [5,6]:
        d['sales_revenue'] = \
            prices[1]*numpy.append(X[:4]*bform.condounitsizes,0)
    elif btype in [3,4]: 
        d['rent_revenue'] = \
            prices[3]*3*numpy.append(X[:4]*bform.mfunitsizes,0)
            # rents are per month but need to be period so we multiply by 3
    elif btype in [7,8]: # office
        d['leases_revenue'][4] = X[0]*prices[4]*SQFTFACTOR
        #print "X", X
        #print d['leases_revenue']
    elif btype in [9,10,11]: # retail
        d['leases_revenue'][4] = X[0]*prices[5]*SQFTFACTOR
        #print "X", X
        #print d['leases_revenue']
    elif btype in [12,13]: # industrial
        d['leases_revenue'][4] = X[0]*prices[6]*SQFTFACTOR
        #print "X", X
        #print d['leases_revenue']
    else: assert 0

    #print btype
    #print params
    #print d

    proposal_comp['sales_revenue'] = d['sales_revenue']
    proposal_comp['rent_revenue'] = d['rent_revenue']
    proposal_comp['leases_revenue'] = d['leases_revenue']
    proposal['sales_revenue'] = proposal_comp['sales_revenue'].sum()
    proposal['rent_revenue'] = proposal_comp['rent_revenue'].sum()
    proposal['leases_revenue'] = proposal_comp['leases_revenue'].sum()

    proposal_comp['sales_absorption'] *= d['sales_revenue']
    proposal_comp['sales_absorption'] = .25*d['sales_revenue']
    ##updatate these when needed
    #proposal_comp['rent_absorption'] =  ?
    #proposal_comp['leases_absorption'] = ?
    #d['rent_absorption'] =   array([  8,  4,  4,  8,  8])
    #d['leases_absorption'] = array([  1,  1,  1,  1,  6])
    proposal_comp['rent_revenue_per_period'] = proposal_comp['rent_revenue'] / proposal_comp['rent_absorption']
    proposal_comp['leases_revenue_per_period'] = proposal_comp['leases_revenue'] / proposal_comp['leases_absorption']

    proposal['rent_revenue_per_period'] =  proposal_comp['rent_revenue_per_period'].sum()
    proposal['leases_revenue_per_period'] = proposal_comp['leases_revenue_per_period'].sum()
    proposal['rent_operating_cost_per_period'] = (proposal_comp['rent_revenue_per_period'] * proposal_comp['operating_cost']).sum()
    proposal['leases_operating_cost_per_period'] = (proposal_comp['leases_revenue_per_period'] * proposal_comp['operating_cost']).sum()
    proposal['rent_vacancy_per_period'] = (proposal_comp['rent_revenue_per_period'] * proposal_comp['vacancy_rates']).sum()
    proposal['leases_vacancy_per_period'] = (proposal_comp['leases_revenue_per_period'] * proposal_comp['vacancy_rates']).sum()

    if btype in [1,2]: cost = bform.sf_cost()
    elif btype in [3,4]: cost = bform.mf_cost('apt')
    elif btype in [5,6]: cost = bform.mf_cost('condo')
    else: cost = bform.commercial_cost(btype)

    #print btype, params
    #print "cost", cost
    proposal['land_cost'] = bform.procurement_cost()
    if proposal['land_cost'] == 0: proposal['land_cost'] = 100000
    proposal['construction_cost'] = cost 
    #print proposal['construction_cost']
    if DEBUG: print "COST:", proposal['construction_cost']
    #if DEBUG: print "COST:",proforma_inputs['proposal']['construction_cost']

    if DEBUG > 1: print "SALES REVENUE", d['sales_revenue']
    if DEBUG > 1: print d['rent_revenue']
    if DEBUG > 1: print d['leases_revenue']
    #if DEBUG > 1: print d['sales_absorption']
    #if DEBUG > 1: print d['rent_absorption']
    #if DEBUG > 1: print d['leases_absorption']

    #from opus_core.tests.utils import variable_tester
    #po=['urbansim_parcel','urbansim']
    #v = variable_tester.VariableTester('proforma.py',po,proforma_inputs)
    #npv = v._get_attribute('npv')
    npv = proforma.do_proforma(proposal, proposal_comp)
    #npv = proposal.compute_variables('urbansim_parcel.proposal.proforma', 
    #                                 dataset_pool=dataset_pool)
 
    #print npv, "\n\n"
    return -1*npv/100000.0

def optimize(bform,prices,submarket_info=None):
   
    btype = bform.btype

    ieqcons = None 
    if btype == 1: ieqcons = bform.sfoneoff_bounds
    elif btype == 2: ieqcons = bform.sfbuilder_bounds
    elif btype in [3,4]: ieqcons = bform.mf_bounds
    elif btype in [5,6]: ieqcons = bform.mf_bounds
    elif btype in COMMERCIALTYPES_D: ieqcons = bform.commercial_bounds
    else: assert 0

    #if btype == 2: return [], -1.0

    if btype in [4,6]: nf = 5
    elif btype in COMMERCIALTYPES_D: nf = 1
    else: nf = 4
    x0 = array([0 for i in range(nf)])
    
    dataset_pool = setup_dataset_pool(opus=False,submarket_info=submarket_info)
    #proposal = dataset_pool.get_dataset('proposal')
    logger.set_verbosity_level(0)
    #proposal.compute_variables(["property_tax = proposal.disaggregate(parcel.property_tax)",
    #                            "land_cost = proposal.disaggregate(parcel.land_cost)"], 
    #                           dataset_pool=dataset_pool)

    #r = fmin_l_bfgs_b(_objfunc,x0,approx_grad=1,bounds=bounds,epsilon=1.0,factr=1e16)
    if 0: #DEBUG:
        r = fmin_slsqp(_objfunc,x0,f_ieqcons=ieqcons,iprint=0,full_output=1,epsilon=1,args=[btype,prices,dataset_pool],iter=150,acc=.01)
        print r
        #r2[0] = numpy.round(r2[0], decimals=1)
        #r2[1] = _objfunc(r2[0],btype)
   
    r = fmin_slsqp(_objfunc2,x0,f_ieqcons=ieqcons,iprint=0,full_output=1,epsilon=1,args=[bform,btype,prices,dataset_pool],iter=150,acc=.01)
    #if DEBUG > 0: print r
    #print r
    r[0] = numpy.round(r[0], decimals=1)
    r[1] = _objfunc2(r[0],bform,btype,prices,dataset_pool)
    if 0: #DEBUG: 
        print r2
        print r
        numpy.testing.assert_approx_equal(r2[1],r[1],significant=1)
    r[1] *= -1*100000

    return r[0], r[1]
