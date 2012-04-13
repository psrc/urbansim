from urbansim_parcel.proposal.pycel.excelutil import *
from urbansim_parcel.proposal.pycel.excellib import *
from scipy.optimize import *
from numpy import array
from opus_core.logger import logger
import copy

DEBUG = 0
SQFTFACTOR = 300.0
COMMERCIALTYPES_D = {7:82,8:82,9:79,10:80,11:81,12:83,13:84}

PROFORMA_INPUTS = {            
            'parcel':
            {
                "parcel_id":        array([1]),
                "property_tax":     array([0.01]),
                "land_cost":        array([ 1]) * 100000, #Land + other equity
            },
            'proposal_component':
            {
               "proposal_component_id": array([1,  2,  3,  4,  5]),
               "proposal_id":           array([1,  1,  1,  1,  1]),
	           "building_type_id":      array([1,  1,  1,  1,  5]),  
               "bedrooms":              array([1,  2,  3,  4,  0]),
               "sales_revenue":         array([2,  3,  4,  5,  0]) * 1000000, 
               "sales_absorption":      array([.25,0.3,0.35,0.4,  0]) * 1000000,
               "rent_revenue":          array([ .1,0.2,0.3,0.4,  0]) * 1000000,
               "rent_absorption":       array([  8,  4,  4,  8,  8]),
               "leases_revenue":        array([  0,  0,  0,  0,  4]) * 1000000,
               "leases_absorption":     array([  0,  0,  0,  0,  8]),
               "vacancy_rates":        array([ 1.0, 0.5, 0.25, 1.0,  0.6]) / 12,
               "operating_cost":        array([0.2,0.2,0.2,0.2, 0.1]),
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
            },
}

def set_value(excel,sp,sheet,cell,value):
    if excel:
        excel.excel.app.ActiveWorkbook.Sheets(sheet).Range(cell).Value=float(value)
    sp.set_value('%s!%s' % (sheet,cell), value)
    
def save(excel,fname):
    excel.save_as(abspath(fname),True)


def _objfunc(params,btype,saveexcel=0,excelprefix=None):
    global sp
    global c

    e = None
    if saveexcel: e = excel

    if btype == 1: # single family one-off
        assert len(params) == 4
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (63+i), params[i])
    elif btype == 2: # single family builder
        assert len(params) == 4
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (58+i), params[i])
    elif btype == 3: # mf-rental
        assert len(params) == 4
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (68+i), params[i])
    elif btype == 5: # mf-condo
        assert len(params) == 4
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (73+i), params[i])
    elif btype == 6: # mxd-condo
        assert len(params) == 5
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (73+i), params[i])
        set_value(e,sp,'Bldg Form','K78', params[4])
    elif btype in COMMERCIALTYPES_D: # commercial types
        assert len(params) == 1
        set_value(e,sp,'Bldg Form','K%d'%(COMMERCIALTYPES_D[btype]), params[0]*SQFTFACTOR)

    npv = sp.evaluate('Proforma!B52')

    if saveexcel and excel: 
        save(excel.excel,'output/%s.xlsx' % excelprefix)

    if DEBUG > 1: print "PARAMS:", params
    if DEBUG > 1: print "NPV2", npv
    return -1*npv/100000.0
    	
def _objfunc2(params,btype,prices,sp,bounds,saveexcel=0,excelprefix=None):

    global PROFORMA_INPUTS
    proforma_inputs = copy.copy(PROFORMA_INPUTS)
    X = params

    e = None
    if DEBUG > 1: print "PARAMS", params
    if btype == 1: # single family one-off
        assert len(params) == 4
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (63+i), params[i])
    elif btype == 2: # single family builder
        assert len(params) == 4
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (58+i), params[i])
    elif btype == 3: # mf-rental
        assert len(params) == 4
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (68+i), params[i])
    elif btype == 5: # mf-condo
        assert len(params) == 4
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (73+i), params[i])
    elif btype == 6: # mxd-condo
        assert len(params) == 5
        for i in range(4): set_value(e,sp,'Bldg Form','K%d' % (73+i), params[i])
        set_value(e,sp,'Bldg Form','K78', params[4])
    elif btype in COMMERCIALTYPES_D: # commercial types
        assert len(params) == 1
        set_value(e,sp,'Bldg Form','K%d'%(COMMERCIALTYPES_D[btype]), params[0]*SQFTFACTOR)

    d = proforma_inputs['proposal_component']
    logger.set_verbosity_level(0)
    

    d['sales_revenue'] =     array([  0,  0,  0,  0,  0])
    d['rent_revenue'] =      array([  0,  0,  0,  0,  0])
    d['leases_revenue'] =    array([  0,  0,  0,  0,  0])
    if btype in [1,2]: 
      for i in range(4):
        d['sales_revenue'][i] = \
			sp.evaluate('Bldg Form!E%d' % (58+i))*prices[0]*X[i]
			#max(sp.evaluate('Proforma Inputs!B%d' % (60+i)),0)
    elif btype in [5,6]:
      for i in range(4):
        d['sales_revenue'][i] = \
			sp.evaluate('Bldg Form!E%d' % (68+i))*prices[1]*X[i]
			#max(sp.evaluate('Proforma Inputs!B%d' % (48+i)),0)
    elif btype in [3,4]: 
      for i in range(4):
        d['rent_revenue'][i] = \
			sp.evaluate('Bldg Form!E%d' % (68+i))*prices[3]*3*X[i]
            # rents are per month but need to be period so we multiply by 3
			#max(sp.evaluate('Proforma Inputs!B%d' % (74+i)),0)
    else:
        d['leases_revenue'][4] = \
            X[0]*20.0 # we need price info for non-residential!
			#max(sp.evaluate('Proforma Inputs!B%d' % (92)),0)
    d['sales_absorption'] =  .2*d['sales_revenue']
    d['rent_absorption'] =   array([  8,  4,  4,  8,  -1])
    d['leases_absorption'] = array([  -1,  -1,  -1,  -1,  6])

    proforma_inputs['proposal']['construction_cost'] = array(sp.evaluate('Proforma Inputs!B40'))
    if DEBUG > 1: print "COST:",proforma_inputs['proposal']['construction_cost']

    if DEBUG > 1: print "SALES REVENUE", d['sales_revenue']
    if DEBUG > 1: print d['rent_revenue']
    if DEBUG > 1: print d['leases_revenue']
    if DEBUG > 1: print d['sales_absorption']
    if DEBUG > 1: print d['rent_absorption']
    if DEBUG > 1: print d['leases_absorption']

    from opus_core.tests.utils import variable_tester
    po=['urbansim_parcel','urbansim']
    v = variable_tester.VariableTester('/home/ffoti/urbansim/src/urbansim_parcel/proposal/proforma.py',po,proforma_inputs)
    npv = v._get_attribute('npv')
    #print npv, "\n\n"
    return -1*npv/100000.0

def optimize(sp,btype,prices):
   
    bounds = []
 
    if btype == 1: # single family one-off
        for i in range(4):
            v = sp.evaluate('Bldg Form!J%d' % (63+i))
            bounds.append(v)
    
    elif btype == 2: # single family builder
        for i in range(4):
            v = sp.evaluate('Bldg Form!J%d' % (58+i))
            bounds.append(v)

    elif btype in [3,4]: # multifamily
        for i in range(4):
            v = sp.evaluate('Bldg Form!J%d' % (68+i))
            bounds.append(v)
    
    elif btype in [5,6]: # condo
        for i in range(4):
            v = sp.evaluate('Bldg Form!J%d' % (73+i))
            bounds.append(v)

    elif btype in COMMERCIALTYPES_D:
        v = sp.evaluate('Bldg Form!J%d' % COMMERCIALTYPES_D[btype])/SQFTFACTOR
        bounds.append(v)

    if btype in [4,6,8]: # ground floor retail
        v = sp.evaluate('Bldg Form!J78')
        bounds.append(max(v,0))

    if bounds.count(0) == len(bounds):
        if DEBUG > 0: print "Nothing to optimize\n"
        return [], -1.0

    bounds = numpy.array(bounds,dtype=numpy.float32)

    x0 = numpy.array([0 for i in range(len(bounds))])

    bounds = numpy.array([(0,x) for x in bounds],dtype=numpy.float32)
    if DEBUG > 1: print "BOUNDS: ", bounds

    def ieqcons_sf_builder(X,*args):
        sp = args[2]
        bounds = args[3]
        #print X
        cons = []
        for i in range(len(X)):
            cons.append(bounds[i][1]-X[i])
            cons.append(X[i]-bounds[i][0])
        sqft = sp.evaluate('Bldg Form!J88')
        sqft -= sp.evaluate('Bldg Form!D58')*X[0]
        sqft -= sp.evaluate('Bldg Form!D59')*X[1]
        sqft -= sp.evaluate('Bldg Form!D60')*X[2]
        sqft -= sp.evaluate('Bldg Form!D61')*X[3]
        cons.append(sqft)
        #print cons
        return numpy.array(cons)

    def ieqcons_sf_oneoff(X,*args):
        sp = args[2]
        bounds = args[3]
        #print bounds
        #print X
        cons = []
        for i in range(len(X)):
            cons.append(bounds[i][1]-X[i])
            cons.append(X[i]-bounds[i][0])
        units = 1 - X[0] - X[1] - X[2] - X[3]
        cons.append(units)
        #print cons
        return numpy.array(cons)
    
    def ieqcons_mf_rental(X,*args):
        sp = args[2]
        bounds = args[3]
        #print X
        cons = []
        for i in range(len(X)):
            cons.append(bounds[i][1]-X[i])
            cons.append(X[i]-bounds[i][0])
        sqft = sp.evaluate('Bldg Form!C49')
        
        for i in range(4): sqft -= sp.evaluate('Bldg Form!E%d'%(68+i))*X[i]
        #sqft -= X[8]*SQFTFACTOR
        cons.append(sqft)
        #print cons
        return numpy.array(cons)

    def ieqcons_mf_condo(X,*args):
        sp = args[2]
        bounds = args[3]
        #print X
        cons = []
        for i in range(len(X)):
            cons.append(bounds[i][1]-X[i])
            cons.append(X[i]-bounds[i][0])
        sqft = sp.evaluate('Bldg Form!C49')
        #print sqft
        for i in range(4): sqft -= sp.evaluate('Bldg Form!E%d'%(73+i))*X[i]
        #sqft -= X[8]*SQFTFACTOR
        cons.append(sqft)
        #print cons
        return numpy.array(cons)

    def ieqcons_commercial(X,*args):
        sp = args[2]
        cons = []
        sqft = sp.evaluate('Bldg Form!C49')
        sqft -= X[0]*SQFTFACTOR
        cons.append(sqft)
        cons.append(X[0])
        return numpy.array(cons)

    ieqcons = None 
    if btype == 1: ieqcons = ieqcons_sf_oneoff
    elif btype == 2: ieqcons = ieqcons_sf_builder
    elif btype in [3,4]: ieqcons = ieqcons_mf_rental
    elif btype in [5,6]: ieqcons = ieqcons_mf_condo
    elif btype in COMMERCIALTYPES_D: ieqcons = ieqcons_commercial
    else: ieqcons = ieqcons_sf_oneoff 

    #r = fmin_l_bfgs_b(_objfunc,x0,approx_grad=1,bounds=bounds,epsilon=1.0,factr=1e16)
    if 0: #DEBUG:
        r2 = fmin_slsqp(_objfunc,x0,f_ieqcons=ieqcons,iprint=1,full_output=1,epsilon=1,args=[btype],iter=150,acc=.001)
        print r2
        r2[0] = numpy.round(r2[0], decimals=1)
        r2[1] = _objfunc(r2[0],btype)

    r = fmin_slsqp(_objfunc2,x0,f_ieqcons=ieqcons,iprint=0,full_output=1,epsilon=1,args=[btype,prices,sp,bounds],iter=150,acc=.01)
    if DEBUG > 0: print r
    #print r
    r[0] = numpy.round(r[0], decimals=1)
    r[1] = _objfunc2(r[0],btype,prices,sp,bounds)
    if 0: #DEBUG: 
        print r2
        print r
        numpy.testing.assert_approx_equal(r2[1],r[1],significant=1)
    r[1] *= -1*100000

    return r[0], r[1]
