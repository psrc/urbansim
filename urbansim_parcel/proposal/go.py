'''
Simple example file showing how a spreadsheet can be translated to python and executed
'''

from __future__ import division
import os, sys, cPickle, traceback
from pycel.excelutil import *
from pycel.excellib import *
from os.path import normpath,abspath
import getopt
from devmdl_utils import *
import numpy
from numpy import array
from scipy.optimize import *
import scipy
from openopt import *
sys.path.insert(1,'d:\urban_sim_ffoti')
import proforma
from pycel.excelcompiler import ExcelCompiler, Spreadsheet
from opus_core.logger import logger

DEBUG = 0
SQFTFACTOR = 300.0
COMMERCIALTYPES_D = {7:82,9:79,10:80,11:81,12:83,13:84}

'''
deal with hardcoded paths
cost factor by county
deal with outliers in accessibility computations
write buildings back to db

land cost
deal with nonresidential building prices

get scenario-based zoning when it exists
account for parking
reimplement cost model
check all the constants?
'''

'''
DONE:
run multithreaded
'''

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

    if DEBUG: print "PARAMS:", params
    if DEBUG: print "NPV2", npv
    return -1*npv/100000.0
    	
def _objfunc2(params,btype,saveexcel=0,excelprefix=None):

    global proforma_inputs
    e = None
    if DEBUG: print "PARAMS", params
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
			max(sp.evaluate('Proforma Inputs!B%d' % (60+i)),0)
    elif btype in [5,6]:
      for i in range(4):
        d['sales_revenue'][i] = \
			max(sp.evaluate('Proforma Inputs!B%d' % (48+i)),0)
    elif btype in [3,4]: 
      for i in range(4):
        d['rent_revenue'][i] = \
			max(sp.evaluate('Proforma Inputs!B%d' % (74+i)),0)
    else:
        d['leases_revenue'][4] = \
			max(sp.evaluate('Proforma Inputs!B%d' % (92)),0)
    d['sales_absorption'] =  .2*d['sales_revenue']
    d['rent_absorption'] =   array([  8,  4,  4,  8,  8])
    d['leases_absorption'] = array([  1,  1,  1,  1,  6])

    proforma_inputs['proposal']['construction_cost'] = array(sp.evaluate('Proforma Inputs!B40'))
    if DEBUG: print "COST:",proforma_inputs['proposal']['construction_cost']

    if DEBUG: print "SALES REVENUE", d['sales_revenue']
    if DEBUG: print d['rent_revenue']
    if DEBUG: print d['leases_revenue']
    if DEBUG: print d['sales_absorption']
    if DEBUG: print d['rent_absorption']
    if DEBUG: print d['leases_absorption']

    from opus_core.tests.utils import variable_tester
    po=['urbansim_parcel','urbansim']
    v = variable_tester.VariableTester('proforma.py',po,proforma_inputs)
    npv = v._get_attribute('npv')
    #print npv, "\n\n"
    return -1*npv/100000.0

def optimize(sp,btype):
   
    global bounds
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
        bounds.append(v)

    if bounds.count(0) == len(bounds):
        print "Nothing to optimize\n"
        return [], -1.0

    bounds = numpy.array(bounds,dtype=numpy.float32)

    x0 = numpy.array([0 for i in range(len(bounds))])

    bounds = numpy.array([(0,x) for x in bounds],dtype=numpy.float32)
    if DEBUG: print "BOUNDS: ", bounds

    def ieqcons_sf_builder(X,*args):
        global bounds
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
        global bounds
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
        global bounds
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
        global bounds
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
    else: assert 0

    #r = fmin_l_bfgs_b(_objfunc,x0,approx_grad=1,bounds=bounds,epsilon=1.0,factr=1e16)
    if DEBUG:
        r2 = fmin_slsqp(_objfunc,x0,f_ieqcons=ieqcons,iprint=1,full_output=1,epsilon=1,args=[btype],iter=150,acc=.001)
        print r2
        r2[0] = numpy.round(r2[0], decimals=1)
        r2[1] = _objfunc(r2[0],btype)

    r = fmin_slsqp(_objfunc2,x0,f_ieqcons=ieqcons,iprint=1,full_output=1,epsilon=1,args=[btype],iter=150,acc=.001)
    print r
    r[0] = numpy.round(r[0], decimals=1)
    r[1] = _objfunc2(r[0],btype)
    if DEBUG: 
        print r2
        print r
        numpy.testing.assert_approx_equal(r2[1],r[1],significant=1)

    return r[0], r[1]

def set_value(excel,sp,sheet,cell,value):
    if excel:
        excel.excel.app.ActiveWorkbook.Sheets(sheet).Range(cell).Value=float(value)
    sp.set_value('%s!%s' % (sheet,cell), value)
    
def save(excel,fname):
    excel.save_as(abspath(fname),True)
	
proforma_inputs = {            
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

class DeveloperModel:

  def __init__(my):
    pass

  def load(my):
    generatepython = 0
    generatedb = 0
    repressoutput = 0
    fname = None
    opts, args = getopt.getopt(sys.argv[1:], "dgrf:")
    for o, a in opts:
        if o == "-d": generatedb = 1
        if o == "-g": generatepython = 1
        if o == "-f": fname = a
        if o == "-r": repressoutput = 1

    global excel
    excel = None
    if fname:
        fname = normpath(abspath(fname))
        print "Loading %s..." % fname
    if not repressoutput:
        excel = ExcelCompiler(filename=fname)
        my.excel = excel

    if generatedb:
        z = Zoning()
        p = Parcels()
        cPickle.dump((z,p),open('databaseinfo.jar','w'))
    else:
        print "Reading db info from jar..."
        z,p = cPickle.load(open('databaseinfo.jar'))

    global sp
    if generatepython:
        print "Compiling..., starting from NPV"
        sp = c.gen_graph('B52',sheet='Proforma')
        print "Serializing to disk..."
        sp.save_to_file(fname + ".jar")
    
        # show the graph usisng matplotlib
        #print "Plotting using matplotlib..."
        #sp.plot_graph()

        # export the graph, can be loaded by a viewer like gephi
        print "Exporting to gexf..."
        sp.export_to_gexf(fname + ".gexf")
    else:
        print "Reading formula from jar..."
        sp = Spreadsheet.load_from_file(fname+'.jar')

    if generatedb or generatepython: 
        print "Done generating, run again for proforma"
        sys.exit(0)

    #set_value(excel,sp,'Revenue Model','B97',100.0) # artificially increase retail revenue for testing

    print "Num of parcels:", len(p.get_pids())
    for pid in p.get_pids()[:100]:
        #proforma_inputs['parcel']['parcel_id'] = pid

        print "parcel_id is %d" % pid
        v = float(p.get_attr(pid,'shape_area'))*10.7639
        set_value(excel,sp,"Bldg Form","C28",v)

        try: zoning = z.get_zoning(pid)
        except: 
            print "Can't find zoning for parcel: %d, skipping\n" % pid
            continue
        btypes = z.get_building_types(pid)
        if not zoning:
            print "NO ZONING FOR PARCEL\n"
            continue
        if not btypes:
            print "NO BUILDING TYPES FOR PARCEL\n"
            continue
        print "Parcel size is %f" % v
        far = z.get_attr(zoning,'max_far', 100)
        height = int(z.get_attr(zoning,'max_height', 1000))

        if far == 100 and height == 1000: far,height = .75,10
        set_value(excel,sp,"Bldg Form","C34",far) # far
        set_value(excel,sp,"Bldg Form","C33",height) # height

        if far > 1 or height > 15:
            set_value(excel,sp,"Bldg Form","C39",1) # multi-story

        print "ZONING BTYPES:", btypes

        # right now we can't have MF-CONDO (type 5)
        devmdl_btypes = []
        if 1 in btypes or 2 in btypes: devmdl_btypes+=[1,2]
        if 3 in btypes: 
	    devmdl_btypes+=[3,5] # MF to MF-rental and MF-condo
        if 4 in btypes: devmdl_btypes.append(7) # office to office
        #if 5 in btypes: continue # hotel
        #if 6 in btypes: continue # schools
        if 7 in btypes or 8 in btypes: # light industrial and warehouse to warehouse
	    devmdl_btypes.append(13) 
        if 9 in btypes: devmdl_btypes.append(12) # heavy industrial to manufacturing
        if 10 in btypes: devmdl_btypes.append(10) # strip mall to auto
        if 11 in btypes: devmdl_btypes.append(11) # big box to big box
        if 12 in btypes: devmdl_btypes+=[4,6] # residential-focused to MXD-MF and MXD-condo
        if 13 in btypes: devmdl_btypes.append(9) # retail focused to neighborhood retail
        if 14 in btypes: devmdl_btypes.append(8) # employment-focused to MXD-office

        btypes = devmdl_btypes

	print "DEVMDL BTYPES:", btypes

        for btype in btypes:
            print "building type = %s" % btype
            
            if btype in [1,2,3,4,5,6]: # RESIDENTIAL
                zone_id = p.get_attr(pid,'zone_id')
                lotsize = p.get_lotsize(zone_id)
                unitsize = p.get_unitsize(zone_id,'HS')
                unitsize2 = p.get_unitsize(zone_id,'MR')
            if not unitsize: unitsize = 1111
            if not unitsize2: unitsize2 = 888
	    if not lotsize: lotsize = 11111
	    print "zone:", zone_id, "lotsize:", lotsize, "HS size:", unitsize, "MF size:", unitsize2

            if btype in [4,6,8,9]:
                set_value(excel,sp,"Bldg Form","C39",1) # ground floor retail

            def unset_uses(e,s):
                for au in [58,59,60,61, 63,64,65,66, 68,69,70,71, 73,74,75,76, \
                           78,79,80,81,82,83,84]: 
                    set_value(excel,sp,"Bldg Form","C%d" % au,0)
                    set_value(excel,sp,"Bldg Form","K%d" % au,0)

            def allowable_uses(e,s,aus): 
                unset_uses(e,s)
                for au in aus: set_value(excel,sp,"Bldg Form","C%d" % au,1)

            if btype == 1: # this is single family one-off
                assert lotsize
                assert unitsize
                set_value(excel,sp,"Bldg Form","D57",lotsize) # lot size for single family
                set_value(excel,sp,"Bldg Form","E57",unitsize) # unit size for single family
                allowable_uses(excel,sp,[63,64,65,66])

            elif btype == 2: # this is single family builder
                assert lotsize
                assert unitsize
                set_value(excel,sp,"Bldg Form","D57",lotsize) # lot size for single family
                set_value(excel,sp,"Bldg Form","E57",unitsize) # unit size for single family
                allowable_uses(excel,sp,[58,59,60,61])

            elif btype == 3: # MF-rental
                assert unitsize2
                set_value(excel,sp,"Bldg Form","D67",unitsize2) # unit size for multi family
                allowable_uses(excel,sp,[68,69,70,71])

            elif btype == 4: # MXD-MF
                assert unitsize2
                set_value(excel,sp,"Bldg Form","D67",unitsize2) # unit size for multi family
                allowable_uses(excel,sp,[68,69,70,71,78])
            
            elif btype == 5: # MF-CONDO
                assert unitsize2
                set_value(excel,sp,"Bldg Form","D67",unitsize2) # unit size for multi family
                allowable_uses(excel,sp,[73,74,75,76])

            elif btype == 6: # MXD-CONDO
                assert unitsize2
                set_value(excel,sp,"Bldg Form","D67",unitsize2) # unit size for multi family
                allowable_uses(excel,sp,[73,74,75,76,78])
            
            elif btype == 8: # MXD-OFFICE
                assert unitsize2
                set_value(excel,sp,"Bldg Form","D67",unitsize2) # unit size for multi family
                allowable_uses(excel,sp,[78,82])

            elif btype == 14: # LODGING
                continue # skip fo now

            elif btype in COMMERCIALTYPES_D: # COMMERCIAL TYPES
                allowable_uses(excel,sp,[COMMERCIALTYPES_D[btype]])

            else: assert(0)

            X, npv = optimize(sp,btype)
            if npv == -1: continue # error code

            _objfunc2(X,btype,saveexcel=1,excelprefix='%d_%s' % (pid,btype))
            print

if __name__ == '__main__':
    d = DeveloperModel()
    try:
        d.load()
    except Exception as e:
        traceback.print_exc()
    try: excel.excel.close()
    except: pass
