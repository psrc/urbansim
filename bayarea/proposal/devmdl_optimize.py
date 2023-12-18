# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

#from urbansim_parcel.proposal.pycel.excelutil import *
#from urbansim_parcel.proposal.pycel.excellib import *
from scipy.optimize import *
from numpy import array
from opus_core.logger import logger
from .proforma import proforma
from .constants import *
import numpy
import copy

DEBUG = 0
SQFTFACTOR = 300.0
OBJCNT = 0

def _objfunc2(params,bform,btype,prices,costdiscount,dataset_pool,baveexcel=0,excelprefix=None):

    global OBJCNT
    OBJCNT += 1    
    if len(params) >= 4: bform.set_num_units(array(params[:4]))
    if len(params) == 5: bform.set_nonres_sqft(params[4]*SQFTFACTOR)
    if len(params) == 1: bform.set_nonres_sqft(params[0]*SQFTFACTOR)

    #global PROFORMA_INPUTS
    #proforma_inputs = copy.copy(PROFORMA_INPUTS)
    X = params

    e = None
    if DEBUG > 1: print("PARAMS", params)

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
            prices[3]*3*numpy.append(X[:4]*bform.condounitsizes,0)
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

    proposal_comp['sales_absorption'] = d['sales_revenue'] * proposal_comp['sales_absorption_ratio']
    #proposal_comp['sales_absorption'] = .25*d['sales_revenue']
    #proposal_comp['rent_absorption'] = array([4 for i in range(5)])
    #proposal_comp['leases_absorption'] = array([4 for i in range(5)])
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
    proposal['land_cost'] = max(bform.procurement_cost(),100000)
    proposal['costdiscount'] = costdiscount
    proposal['construction_cost'] = cost 
    #print proposal['construction_cost']
    if DEBUG: print("COST:", proposal['construction_cost'])
    #if DEBUG: print "COST:",proforma_inputs['proposal']['construction_cost']

    if DEBUG > 1: print("SALES REVENUE", d['sales_revenue'])
    if DEBUG > 1: print(d['rent_revenue'])
    if DEBUG > 1: print(d['leases_revenue'])
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
 
    if DEBUG > 1: print("NPV=", npv, "\n\n")
    return -1*npv/100000.0

#cost discount should be .01 for 1% discount
def optimize(bform,prices,costdiscount,dataset_pool):
   
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
    
    proposal_comp = dataset_pool['proposal_component']
    proposal_comp['sales_absorption_ratio'] = copy.copy(proposal_comp['sales_absorption'])

    bform.sales_absorption = proposal_comp['sales_absorption']
    bform.rent_absorption = proposal_comp['rent_absorption']
    bform.leases_absorption = proposal_comp['leases_absorption']
    bform.sales_vacancy_rates = proposal_comp['sales_vacancy_rates']
    bform.vacancy_rates = proposal_comp['vacancy_rates']


    bldg_type = devmdltypes[btype-1]
    #throttle development when annual vacancy > 10%
    #residential vacancy = min(own, rent)
    max_residential_vacancy = min( proposal_comp['sales_vacancy_rates'][0],
                                   proposal_comp['vacancy_rates'][0]) * 12
    non_residential_vacancy = proposal_comp['vacancy_rates'][4] * 12
   
    if bldg_type in residential_building_types:
        if max_residential_vacancy > .1:
            return [], -1.0
    elif non_residential_vacancy > .1:
        return [], -1.0
    
    logger.set_verbosity_level(0)
    #proposal.compute_variables(["property_tax = proposal.disaggregate(parcel.property_tax)",
    #                            "land_cost = proposal.disaggregate(parcel.land_cost)"], 
    #                           dataset_pool=dataset_pool)

    #r = fmin_l_bfgs_b(_objfunc,x0,approx_grad=1,bounds=bounds,epsilon=1.0,factr=1e16)
    if 0: #DEBUG:
        r = fmin_slsqp(_objfunc,x0,f_ieqcons=ieqcons,iprint=0,full_output=1,epsilon=1,args=[btype,prices,dataset_pool],iter=150,acc=.01)
        print(r)
        #r2[0] = numpy.round(r2[0], decimals=1)
        #r2[1] = _objfunc(r2[0],btype)
   
    r = fmin_slsqp(_objfunc2,x0,f_ieqcons=ieqcons,iprint=0,full_output=1,epsilon=1,args=[bform,btype,prices,costdiscount,dataset_pool],iter=150,acc=.01)
    r = list(r)
    logger.log_status("type r: %s" % (type(r)))
    logger.log_status("len r: %s" % (len(r)))
    logger.log_status("r0: %s" % (r[0]))
    logger.log_status("r1: %s" % (r[1]))
    #if DEBUG > 0: print r
    #print r
    if r[3] != 0: return r[0], -1
    r[0] = numpy.round(r[0], decimals=1)
    r[1] = _objfunc2(r[0],bform,btype,prices,costdiscount,dataset_pool)
    if 0: #DEBUG: 
        print(r2)
        print(r)
        numpy.testing.assert_approx_equal(r2[1],r[1],significant=1)
    r[1] *= -1*100000

    return r[0], r[1]
