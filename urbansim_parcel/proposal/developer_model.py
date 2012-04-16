'''
run multithreaded, cost factor by county, buffer queries for revenue, absorption, and unit and lot size
land cost, deal with nonresidential building prices, get scenario-based zoning when it exists
account for parking, reimplement cost model, check all the constants?
'''

from __future__ import division
import os, sys, cPickle, traceback, time, string, StringIO
from os.path import normpath,abspath
import getopt
from devmdl_zoning import *
import devmdl_optimize
from devmdl_optimize import set_value
import numpy
from numpy import array, zeros, ones, where, logical_and, arange, integer, divide
import scipy
import copy
#from openopt import *

sys.path.insert(1,os.path.join(os.environ['OPUS_HOME'],'src/urbansim_parcel/proposal'))
import proforma
from urbansim_parcel.proposal.pycel.excelcompiler import ExcelCompiler, Spreadsheet
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
from opus_core.model import Model
from bayarea.accessibility.pyaccess import PyAccess
from opus_core import paths

DEBUG = 0


class DeveloperModel(Model):

  model_name = "Developer Model"

  def __init__(my):
    pass

  def run(my):
    generatepython = 0
    generatedb = 0
    repressoutput = 0
    fname = os.path.join(os.environ['OPUS_DATA'],'bay_area_parcel/costproforma.xlsx')
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
        z,p = cPickle.load(open(os.path.join(os.environ['OPUS_DATA'],'bay_area_parcel/databaseinfo.jar')))
    opts, args = getopt.getopt(sys.argv[1:], "dgrf:")

    if generatepython:
        print "Compiling..., starting from NPV"
        SP = excel.gen_graph('B52',sheet='Proforma')
        print "Serializing to disk..."
        SP.save_to_file(fname + ".jar")
    
        # show the graph usisng matplotlib
        #print "Plotting using matplotlib..."
        #sp.plot_graph()

        # export the graph, can be loaded by a viewer like gephi
        #print "Exporting to gexf..."
        #sp.export_to_gexf(fname + ".gexf")
    else:
        print "Reading formula from jar..."
        SP = Spreadsheet.load_from_file(fname+'.jar')

    if generatedb or generatepython: 
        print "Done generating, run again for proforma"
        sys.exit(0)

    #set_value(excel,sp,'Revenue Model','B97',100.0) # artificially increase retail revenue for testing
    
    try:
        dataset_pool = SessionConfiguration().get_dataset_pool()
    except:
        from opus_core.store.attribute_cache import AttributeCache
        from opus_core.simulation_state import SimulationState
        ss = SimulationState()
        ss.set_cache_directory(os.path.join(os.environ['OPUS_DATA'], 'bay_area_parcel/runs/run_21.2012_04_13_18_01'))
        ss.set_current_time(2010)
        attribute_cache = AttributeCache()
        dataset_pool = SessionConfiguration(new_instance=True,
                                 package_order=['bayarea', 'urbansim_parcel', 'urbansim', 'opus_core'],
                                 in_storage=attribute_cache
                                ).get_dataset_pool()        

    parcel_set = dataset_pool.get_dataset('parcel')
    building_set = dataset_pool.get_dataset('building')
    building_set = dataset_pool.get_dataset('residential_unit')
    node_set = dataset_pool.get_dataset('node')
    node_ids = array(node_set.node_ids, dtype="int32")
    '''
    node_sum_unit_sqft_sf = node_set.compute_variables('node.aggregate((building.building_sqft - building.non_residential_sqft)*(building.residential_units>0)*(building.building_type_id<3),intermediates=[parcel])')
    node_sum_unit_sqft_sf = array(node_sum_unit_sqft_sf, dtype="float32")

    node_sum_unit_sqft_mf = node_set.compute_variables('node.aggregate((building.building_sqft - building.non_residential_sqft)*(building.residential_units>0)*(building.building_type_id>2),intermediates=[parcel])')
    node_sum_unit_sqft_mf = array(node_sum_unit_sqft_mf, dtype="float32")

    node_sum_sf_parcel_area = node_set.compute_variables('node.aggregate((building.disaggregate(parcel.shape_area))*(building.residential_units==1)*(building.building_type_id==1),intermediates=[parcel])')
    node_sum_sf_parcel_area = array(node_sum_sf_parcel_area, dtype="float32")

    node_sum_sf_price = node_set.compute_variables('node.aggregate((residential_unit.sale_price/1000)*(residential_unit.sale_price>0)*(residential_unit.disaggregate(building.building_type_id<3)),intermediates=[building,parcel])')
    node_sum_sf_price = array(node_sum_sf_price, dtype="float32")

    node_sum_mf_price = node_set.compute_variables('node.aggregate((residential_unit.sale_price/1000)*(residential_unit.sale_price>0)*(residential_unit.disaggregate(building.building_type_id>2)),intermediates=[building,parcel])')
    node_sum_mf_price = array(node_sum_mf_price, dtype="float32")

    node_sum_sf_rent = node_set.compute_variables('node.aggregate((residential_unit.rent)*(residential_unit.rent>0)*(residential_unit.disaggregate(building.building_type_id<3)),intermediates=[building,parcel])')
    node_sum_sf_rent = array(node_sum_sf_rent, dtype="float32")

    node_sum_mf_rent = node_set.compute_variables('node.aggregate((residential_unit.rent)*(residential_unit.rent>0)*(residential_unit.disaggregate(building.building_type_id>2)),intermediates=[building,parcel])')
    node_sum_mf_rent = array(node_sum_mf_rent, dtype="float32")

    node_number_of_sf_resunits = node_set.compute_variables('node.aggregate((building.residential_units)*(building.residential_units>0)*(building.building_type_id<3),intermediates=[parcel])')
    node_number_of_sf_resunits = array(node_number_of_sf_resunits, dtype="float32")

    node_number_of_mf_resunits = node_set.compute_variables('node.aggregate((building.residential_units)*(building.residential_units>0)*(building.building_type_id>2),intermediates=[parcel])')
    node_number_of_mf_resunits = array(node_number_of_mf_resunits, dtype="float32")

    node_number_of_sfdetach_resunits = node_set.compute_variables('node.aggregate((building.residential_units)*(building.residential_units>0)*(building.building_type_id==1),intermediates=[parcel])')
    node_number_of_sfdetach_resunits = array(node_number_of_sfdetach_resunits, dtype="float32")

    node_set.pya.initializeAccVars(10)
    node_set.pya.initializeAccVar(0,node_ids,node_sum_unit_sqft_sf)
    node_set.pya.initializeAccVar(1,node_ids,node_number_of_sf_resunits)
    node_set.pya.initializeAccVar(2,node_ids,node_sum_unit_sqft_mf)
    node_set.pya.initializeAccVar(3,node_ids,node_number_of_mf_resunits)
    node_set.pya.initializeAccVar(4,node_ids,node_sum_sf_parcel_area)
    node_set.pya.initializeAccVar(5,node_ids,node_number_of_sfdetach_resunits)
    node_set.pya.initializeAccVar(6,node_ids,node_sum_sf_price)
    node_set.pya.initializeAccVar(7,node_ids,node_sum_mf_price)
    node_set.pya.initializeAccVar(8,node_ids,node_sum_sf_rent)
    node_set.pya.initializeAccVar(9,node_ids,node_sum_mf_rent)

    sf_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,0,0,1,0)
    sf_units=node_set.pya.getAllAggregateAccessibilityVariables(3000,1,0,1,0)
    sf_sqft=sf_sqft.astype(integer)
    sf_units=sf_units.astype(integer)
    result=divide(sf_sqft,sf_units)
    node_set.add_primary_attribute(name='avg_sf_unit_size', data=result)

    mf_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,2,0,1,0)
    mf_units=node_set.pya.getAllAggregateAccessibilityVariables(3000,3,0,1,0)
    mf_sqft=mf_sqft.astype(integer)
    mf_units=mf_units.astype(integer)
    result=divide(mf_sqft,mf_units)
    node_set.add_primary_attribute(name='avg_mf_unit_size', data=result)

    parcel_area=(node_set.pya.getAllAggregateAccessibilityVariables(3000,4,0,1,0))*10.7639
    sfdetach_resunits=node_set.pya.getAllAggregateAccessibilityVariables(3000,5,0,1,0)
    parcel_area=parcel_area.astype(integer)
    sfdetach_resunits=sfdetach_resunits.astype(integer)
    result=divide(parcel_area,sfdetach_resunits)
    node_set.add_primary_attribute(name='avg_sf_lot_size', data=result)

    sf_price=node_set.pya.getAllAggregateAccessibilityVariables(3000,6,0,1,0)
    sf_price=sf_price.astype(integer)
    result=divide(sf_price,sf_units)
    node_set.add_primary_attribute(name='avg_sf_unit_price', data=(result*1000))

    mf_price=node_set.pya.getAllAggregateAccessibilityVariables(3000,7,0,1,0)
    mf_price=mf_price.astype(integer)
    result=divide(mf_price,mf_units)
    node_set.add_primary_attribute(name='avg_mf_unit_price', data=(result*1000))

    sf_rent=node_set.pya.getAllAggregateAccessibilityVariables(3000,8,0,1,0)
    sf_rent=sf_rent.astype(integer)
    result=divide(sf_rent,sf_units)
    node_set.add_primary_attribute(name='avg_sf_unit_rent', data=result)

    mf_rent=node_set.pya.getAllAggregateAccessibilityVariables(3000,9,0,1,0)
    mf_rent=mf_rent.astype(integer)
    result=divide(mf_rent,mf_units)
    node_set.add_primary_attribute(name='avg_mf_unit_rent', data=result)
    '''

    empty_parcels = parcel_set.compute_variables("(parcel.number_of_agents(building)==0)*(parcel.node_id>0)*(parcel.shape_area>80)")
    test_parcels = where(empty_parcels==1)[0]
    test_parcels = test_parcels[:1000]
    logger.log_status("%s parcels to test" % (test_parcels.size))
    print "Num of parcels:", test_parcels.size
    import time
    t1 = time.time()

    global parcel_set, z, node_set, SP

    #import hotshot, hotshot.stats, test.pystone
    #prof = hotshot.Profile('devmdl.prof')
    #prof.start()

    from multiprocessing import Pool
    pool = Pool(processes=24)
    results = pool.map(process_parcel,test_parcels)
    results = [x for x in results if x <> None and x <> -1]
    print results
    #for p in test_parcels: process_parcel(p)
    t2 = time.time()
    print "Finished in %f seconds" % (t2-t1)
    print "Ran optimization %d times" % devmdl_optimize.OBJCNT
    #print "DONE"
    #prof.stop()
    #prof.close()
    #stats = hotshot.stats.load('devmdl.prof')
    #stats.strip_dirs()
    #stats.sort_stats('cumulative')
    #stats.print_stats(20)

def process_parcel(parcel):

        global parcel_set, z, node_set, SP
        sp = copy.deepcopy(SP)
 
        pid = parcel_set['parcel_id'][parcel]
        node_id = parcel_set['node_id'][parcel]
        print "parcel_id is %d" % pid
        if DEBUG > 0: print "node_id is %d" % node_id
        shape_area = parcel_set['shape_area'][parcel]
        v = float(shape_area)*10.7639
        set_value(excel,sp,"Bldg Form","C28",v)

        try: zoning = z.get_zoning(pid)
        except: 
            print "Can't find zoning for parcel: %d, skipping" % pid
            return
        btypes = z.get_building_types(pid)
        if not zoning:
            print "NO ZONING FOR PARCEL"
            return
        if not btypes:
            print "NO BUILDING TYPES FOR PARCEL"
            return
        if v < 800:
            print "PARCEL SIZE IS TOO SMALL"
            return
        if DEBUG > 0: print "Parcel size is %f" % v
        far = z.get_attr(zoning,'max_far', 100)
        height = int(z.get_attr(zoning,'max_height', 1000))

        if far == 100 and height == 1000: far,height = .75,10
        set_value(excel,sp,"Bldg Form","C34",far) # far
        set_value(excel,sp,"Bldg Form","C33",height) # height

        if far > 1 or height > 15:
            set_value(excel,sp,"Bldg Form","C39",1) # multi-story

        if DEBUG > 0: print "ZONING BTYPES:", btypes

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
        if 14 in btypes: devmdl_btypes.append(7) # employment-focused to MXD-office

        btypes = devmdl_btypes

        idx_node_parcel = where(node_set['node_id']==node_id)[0]

        if DEBUG > 0: print "DEVMDL BTYPES:", btypes

        maxnpv, maxbuilding = 0, -1

        for btype in btypes:
            if DEBUG > 0: print "building type = %s" % btype
            
            if 1: #btype in [1,2,3,4,5,6]: # RESIDENTIAL
                zone_id = parcel_set['zone_id'][parcel]
                lotsize = node_set['avg_sf_lot_size'][idx_node_parcel][0]
                unitsize = node_set['avg_sf_unit_size'][idx_node_parcel][0]
                unitsize2 = node_set['avg_mf_unit_size'][idx_node_parcel][0]
                unitprice = node_set['avg_sf_unit_price'][idx_node_parcel][0]
                unitprice2 = node_set['avg_mf_unit_price'][idx_node_parcel][0]
                unitrent = node_set['avg_sf_unit_rent'][idx_node_parcel][0]
                unitrent2 = node_set['avg_mf_unit_rent'][idx_node_parcel][0]
            if not unitsize: unitsize = 1111  
            if unitsize<250:  unitsize = 1111   
            if unitsize>8000:  unitsize = 8000
            if not unitsize2: unitsize2 = 888  
            if unitsize2<250:  unitsize2 = 888   
            if unitsize2>6000:  unitsize2 = 6000
            price_per_sqft_sf = (unitprice*1.0)/unitsize
            price_per_sqft_mf = (unitprice2*1.0)/unitsize2
            rent_per_sqft_sf = (unitrent*1.0)/unitsize
            rent_per_sqft_mf = (unitrent2*1.0)/unitsize2
            if DEBUG > 0: print "price_per_sqft_sf:", price_per_sqft_sf, "price_per_sqft_mf:", price_per_sqft_mf, "rent_per_sqft_sf:", rent_per_sqft_sf, "rent_per_sqft_mf:", rent_per_sqft_mf
            prices = (price_per_sqft_sf,price_per_sqft_mf,rent_per_sqft_sf,rent_per_sqft_mf)
            if not lotsize: lotsize = 11111    
            if lotsize <1000:  lotsize = 11111   
            if lotsize>10000000: lotsize=10000000
            if DEBUG > 0: print "zone:", zone_id, "lotsize:", lotsize, "HS size:", unitsize, "MF size:", unitsize2

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
                return # skip fo now

            elif btype in devmdl_optimize.COMMERCIALTYPES_D: # COMMERCIAL TYPES
                allowable_uses(excel,sp,[devmdl_optimize.COMMERCIALTYPES_D[btype]])

            else: assert(0)

            X, npv = devmdl_optimize.optimize(sp,btype,prices)
            #if npv == -1: return # error code
            if npv > maxnpv:
                maxnpv = npv
                sqft = 0 #sp.evaluate('Bldg Form!H97') 
                stories = 0 #sqft / sp.evaluate('Bldg Form!H96') 
                if btype in [1,2,3,4,5,6]: # RESIDENTIAL
                    nonres_sqft = sp.evaluate('Bldg Form!K78') 
                    res_sqft = sqft - nonres_sqft
                    res_units = sum(X[0:4])
                else:
                    nonres_sqft = sqft
                    res_sqft = 0
                    res_units = 0
                tenure = 0
                if btype in [3,4]: tenure = 1
                year_built = 2010
                building = (pid, btype, stories, sqft, res_sqft, nonres_sqft, tenure, year_built, res_units)
                maxbuilding = building

            #_objfunc2(X,btype,prices,saveexcel=1,excelprefix='%d_%s' % (pid,btype))
            #print
        return maxbuilding 

if __name__ == "__main__":
    DeveloperModel().run()
