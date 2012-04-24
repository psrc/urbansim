# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

'''
absorption
land cost
nonresidential building prices
building construction model
account for parking
'''

import os, sys, cPickle, traceback, time, string, StringIO
import numpy
from numpy import array

from devmdl_zoning import *
import devmdl_optimize
from isr import ISR
from bform import BForm
from devmdl_accvars import compute_devmdl_accvars

sys.path.insert(1,os.path.join(os.environ['OPUS_HOME'],'src/urbansim_parcel/proposal'))
import proforma
from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.model import Model
from opus_core import paths

DEBUG = 0

class DeveloperModel(Model):

  model_name = "Developer Model"

  def __init__(my):
    pass

  def run(my):
    global parcel_set, z, node_set, isr

    '''
    if 0:
        z = Zoning()
        p = Parcels()
        cPickle.dump((z,p),open('databaseinfo.jar','w'))
    else:
        print "Reading db info from jar..."
        z,p = cPickle.load(open(os.path.join(os.environ['OPUS_DATA'],'bay_area_parcel/databaseinfo.jar')))
    '''

    dataset_pool = SessionConfiguration().get_dataset_pool()

    parcel_set = dataset_pool.get_dataset('parcel')
    building_set = dataset_pool.get_dataset('building')
    node_set = dataset_pool.get_dataset('node')
    
    #transit_set = dataset_pool.get_dataset('transit_station')
    #print dataset_pool.datasets_in_pool()
    '''
    from bayarea.node import transit_type_DDD_within_DDD_meters
    for i in range(7):
        print i
        v = transit_type_DDD_within_DDD_meters.transit_type_DDD_within_DDD_meters(i,500)
        d = v.compute(dataset_pool)
        print d.size
        found = d[numpy.nonzero(d)]
        print found.size
    sys.exit()
    '''
    node_ids = array(node_set.node_ids, dtype="int32")
   
    #compute_devmdl_accvars(node_set,node_ids) 

    current_year = SimulationState().get_current_time()
    z = Zoning(1,current_year)
    isr = ISR()

    empty_parcels = parcel_set.compute_variables("(parcel.number_of_agents(building)==0)*(parcel.node_id>0)*(parcel.shape_area>80)")
    test_parcels = numpy.where(empty_parcels==1)[0]
    test_parcels = test_parcels[:1000]
    logger.log_status("%s parcels to test" % (test_parcels.size))
    print "Num of parcels:", test_parcels.size
    import time

    HOTSHOT = 0

    from multiprocessing import Pool, Queue
    pool = Pool(processes=24)

    import hotshot, hotshot.stats, test.pystone
    if HOTSHOT:
        prof = hotshot.Profile('devmdl.prof')
        prof.start()

    t1 = time.time()
    if HOTSHOT:
        for p in test_parcels: process_parcel(p)
    else:
        results = pool.map(process_parcel,test_parcels)
        results = [x for x in results if x <> None and x <> -1]
        #print results
    t2 = time.time()

    print "Finished in %f seconds" % (t2-t1)
    print "Ran optimization %d times" % devmdl_optimize.OBJCNT
    print "DONE"

    if HOTSHOT:
        prof.stop()
        prof.close()
        stats = hotshot.stats.load('devmdl.prof')
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(20)

def process_parcel(parcel):

        global parcel_set, z, node_set, isr
 
        current_year = SimulationState().get_current_time()
        pid = parcel_set['parcel_id'][parcel]
        county_id = parcel_set['county_id'][parcel]
        taz = parcel_set['zone_id'][parcel]
        node_id = parcel_set['node_id'][parcel]
        #print "parcel_id is %d" % pid
        if DEBUG > 0: print "node_id is %d" % node_id
        shape_area = parcel_set['shape_area'][parcel]
        v = float(shape_area)*10.7639
        #set_value(excel,sp,"Bldg Form","C28",v)

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
            
        bform = BForm(v,far,height,county_id,taz,isr)

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
        #print btypes

        idx_node_parcel = numpy.where(node_set['node_id']==node_id)[0]

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
            bform.set_unit_sizes(lotsize,unitsize,unitsize2)

            bform.btype = btype 
            #print btype
            X, npv = devmdl_optimize.optimize(bform,prices)
            #print X, npv
            #if npv == -1: return # error code
            if npv > maxnpv:
                maxnpv = npv
                nonres_sqft = bform.nonres_sqft
                sqft = nonres_sqft # add residential below
                if btype in [1,2,3,4,5,6]: # RESIDENTIAL
                    if btype in [1,2]: res_sqft = bform.sf_builtarea()
                    else: res_sqft = bform.mf_builtarea()
                    sqft += res_sqft
                    res_units = sum(bform.num_units)
                else:
                    res_sqft = 0
                    res_units = 0
                stories = sqft / bform.buildable_area
                tenure = 0
                if btype in [3,4]: tenure = 1
                year_built = current_year
                building = (pid, btype, stories, sqft, res_sqft, nonres_sqft, tenure, year_built, res_units)
                maxbuilding = building

        return maxbuilding 

if __name__ == "__main__":
    DeveloperModel().run()
