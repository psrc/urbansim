# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys, pickle, traceback, time, string, io, math, copy
import numpy
from numpy import array, zeros, repeat, arange, round, logical_not, concatenate, where, logical_and

from opus_core.logger import logger
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.join_attribute_modification_model import JoinAttributeModificationModel
from opus_core.model import Model
from opus_core import paths
from opus_core.sampling_toolbox import sample_noreplace

from .devmdl_zoning import *
from . import devmdl_optimize
from .isr import ISR
from .parcelfees import ParcelFees
from .shifters import price_shifters
from .bform import BForm
from .devmdl_accvars import compute_devmdl_accvars_nodal, compute_devmdl_accvars_zonal
from .constants import *
from . import submarkets

from IPython import embed

DEBUG = 0
MP = 0
HOTSHOT = 0
NODES = 1
URBANVISION = 1

class DeveloperModel(Model):
  model_name = "Developer Model"

  def __init__(my,scenario='Base Scenario'):
    my.scenario = scenario

  def post_run(self):
    dataset_pool = SessionConfiguration().get_dataset_pool()
    dataset_pool._remove_dataset('price_shifter')
    dataset_pool._remove_dataset('cost_shifter')

  def run(my, cache_dir=None, year=None):
    global parcel_set, z, node_set, zone_set, submarket, esubmarket, isr, parcelfees, costdiscount, building_sqft, building_price
        
    dataset_pool = SessionConfiguration().get_dataset_pool()
    current_year = SimulationState().get_current_time()
    cache_dir = SimulationState().get_cache_directory()

    parcel_set = dataset_pool.get_dataset('parcel')
    building_set = dataset_pool.get_dataset('building')
    household_set = dataset_pool.get_dataset('household')
    unit_set = dataset_pool.get_dataset('residential_unit')
    submarket = dataset_pool.get_dataset('submarket')
    esubmarket = dataset_pool.get_dataset('employment_submarket')
    
    capped_rents = building_set.compute_variables('_adj_rent = building.non_residential_rent*(building.non_residential_rent<120) + 120*(building.non_residential_rent>=120)')
    
    building_set.modify_attribute('non_residential_rent', capped_rents)
    
    if NODES:
        node_set = dataset_pool.get_dataset('node')
        compute_devmdl_accvars_nodal(node_set)
    else:
        zone_set = dataset_pool.get_dataset('zone')
        compute_devmdl_accvars_zonal(zone_set)

    z = Zoning(my.scenario,current_year)
    costdiscount = 0.0
    SAMPLE_RATE = 0.05
    isr = None
    parcelfees = None
    
    empty_parcels = parcel_set.compute_variables("(parcel.number_of_agents(building)==0)*(parcel.parcel_sqft>800)")
    res_parcels = parcel_set.compute_variables("(parcel.number_of_agents(building)>0)*(parcel.parcel_sqft>800)")
    sampled_res_parcels_index = sample_noreplace(where(res_parcels)[0], int(SAMPLE_RATE * parcel_set.size()))
    test_parcels1 = concatenate((where(empty_parcels==1)[0], sampled_res_parcels_index))
    test_parcels = sample_noreplace(test_parcels1, int(.05 * test_parcels1.size))
    
    numpy.random.shuffle(test_parcels)
 
    building_sqft = parcel_set.compute_variables('parcel.aggregate(building.non_residential_sqft + building.residential_units*building.sqft_per_unit)')
    building_price_owner_residential=parcel_set.compute_variables('building_price_owner_res=parcel.aggregate((residential_unit.sale_price)*(residential_unit.sale_price>0),intermediates=[building])')
    building_price_rental_residential=parcel_set.compute_variables('building_price_rental_res=parcel.aggregate((residential_unit.rent*12*17.9)*(residential_unit.rent>0),intermediates=[building])') ##change 17.9
    building_price_nonresidential = parcel_set.compute_variables('building_price_nonres = parcel.aggregate((building.non_residential_rent*7*building.non_residential_sqft))') ##change 7
    sum_building_p = parcel_set.compute_variables('sum_building_price = parcel.building_price_owner_res + parcel.building_price_rental_res + building_price_nonres')
    
    vacant_parcel = parcel_set.compute_variables('parcel.sum_building_price == 0')
    price_per_sqft_land = parcel_set.compute_variables('safe_array_divide(parcel.land_value,parcel.parcel_sqft)')
    parcel_land_area = parcel_set.compute_variables('parcel.parcel_sqft')
    vacant_land_price = vacant_parcel*price_per_sqft_land*parcel_land_area
    building_price = sum_building_p + vacant_land_price #rename property price

    #info used to match from proposal_component to submarket
    parcel_set.compute_variables(["drcog.parcel.within_half_mile_transit", 
                                  "drcog.parcel.zone",
                                 ])
                                 
    logger.log_status("%s parcels to test" % (test_parcels.size))

    
    if MP:
        from multiprocessing import Pool, Queue
        pool = Pool(processes=4)

    if HOTSHOT:
        import hotshot, hotshot.stats
        prof = hotshot.Profile('devmdl.prof')
        prof.start()

    outf = open(os.path.join(cache_dir,'buildings-%d.csv' % current_year),'w')
    outf.write('pid,county,dev_btype,stories,sqft,res_sqft,nonres_sqft,tenure,year_built,res_units,npv,actualfee,btype\n')
    debugf = open(os.path.join(cache_dir,'proforma-debug-%d.csv' % current_year),'w')
    bformdbg = 'county_id,far,height,max_dua,bform.sf_builtarea(),bform.sfunitsizes,bform.mf_builtarea(),bform.mfunitsizes,bform.num_units,bform.nonres_sqft,bform.buildable_area'
    otherdbg = 'isr,parcelfees,existing_sqft,existing_price,lotsize,unitsize,unitsize2,bform.sales_absorption,bform.rent_absorption,bform.leases_absorption,bform.sales_vacancy_rates,bform.vacancy_rates'
    debugf.write('pid,btype,npv,actualfee,pricesf,pricemf,rentsf,rentmf,rentof,rentret,rentind,%s,%s\n' % (bformdbg,otherdbg))
    t1 = time.time()
    aggd = {}

    def chunks(l, n):
        for i in range(0, len(l), n):
           yield l[i:i+n]

    for test_chunk in chunks(test_parcels,1000):

        print("Executing CHUNK")

        sales_absorption = submarket.compute_variables('drcog.submarket.sales_absorption') ######################!!
        rent_absorption = submarket.compute_variables('drcog.submarket.rent_absorption')
        vacancy_rates = submarket.compute_variables('drcog.submarket.vacancy_rates')
        leases_absorption = esubmarket.compute_variables('drcog.employment_submarket.leases_absorption')
        nr_vacancy_rates = esubmarket.compute_variables('drcog.employment_submarket.vacancy_rates')

        if HOTSHOT:
            results = []
            for p in test_chunk: 
                r = process_parcel(p)
                if r != None and r != -1: results.append(list(r))
        else:
            if MP:
                results = pool.map(process_parcel,test_chunk)
            else:
                results = [process_parcel(p) for p in test_chunk]
            results_bldg = [list(x[0]) for x in results if x != None and x[0] != -1]
            #each row of units represents number of units of [1, 2, 3, 4] bedrooms
            units = array([x[1][0] for x in results if x != None and x[0] != -1])
            sqft_per_unit = array([x[1][1] for x in results if x != None and x[0] != -1])
            for x in results:
                if x != None: 
                    debugf.write(x[2])

            results = results_bldg
        for result in results:
            #print result
            out_btype = int(result[2])
            outf.write(string.join([str(x) for x in result]+[str(out_btype)],sep=',')+'\n')

        ##TODO: id of buildings to be demolished
    
        buildings_to_demolish = []
        idx_buildings_to_demolish = building_set.get_id_index(buildings_to_demolish)
        
        JAMM = JoinAttributeModificationModel()
        JAMM.run(household_set, building_set, index=idx_buildings_to_demolish, value=-1)

        building_set.remove_elements(idx_buildings_to_demolish)
        column_names = ["parcel_id","county","building_type_id","stories",
                    "building_sqft","residential_sqft","non_residential_sqft",
                    "tenure","year_built","residential_units"]
        buildings_data = copy.deepcopy(results)

        #for i in range(len(buildings_data)):
            #buildings_data[i][2] = devmdltypes[int(buildings_data[i][2])-1]
        buildings_data = array(buildings_data)
        new_buildings = {}
        available_bldg_id = building_set['building_id'].max() + 1
        new_bldg_ids = arange(available_bldg_id, available_bldg_id+buildings_data.shape[0],
                              dtype=building_set['building_id'].dtype)
        if buildings_data.size > 0:
            for icol, col_name in enumerate(column_names):
                if col_name in building_set.get_known_attribute_names():
                    ddtype = building_set[col_name].dtype
                    new_buildings[col_name] = (buildings_data[:, icol]).astype(ddtype)
                else:
                    #if the col_name is not in dataset, it will be discarded anyway
                    pass

            new_buildings['building_id'] = new_bldg_ids
            # recode tenure: 1 - rent, 2 - own from 0 - own, 1 - rent
            new_buildings['tenure'][new_buildings['tenure']==0] = 1
            ## pid is the index to parcel_set; convert them to actual parcel_id
            #new_buildings['parcel_id'] = parcel_set['parcel_id'][new_buildings['parcel_id']]
            building_set.add_elements(new_buildings, require_all_attributes=False,
                                      change_ids_if_not_unique=True)
            building_set.flush_dataset()

            assert new_bldg_ids.size == units.shape[0] == sqft_per_unit.shape[0]
            units_bldg_ids = repeat(new_bldg_ids, 4)
            bedrooms = array([1, 2, 3, 4] * units.size)
            units = round(units.ravel())
            sqft_per_unit = sqft_per_unit.ravel()
            new_units = {'building_id': array([], dtype='i4'),
                         'bedrooms': array([], dtype='i4'),
                         'unit_sqft': array([], dtype='i4')
                        }
            
            for i_unit, unit in enumerate(units):
                if unit <= 0:
                  continue
                new_units['building_id'] = concatenate((new_units['building_id'],
                                                        repeat(units_bldg_ids[i_unit], unit))
                                                       )
                new_units['bedrooms'] = concatenate((new_units['bedrooms'],
                                                     repeat(bedrooms[i_unit], unit))
                                                    )
                new_units['unit_sqft'] = concatenate((new_units['unit_sqft'],
                                                          repeat(sqft_per_unit[i_unit], unit))
                                                         )

            ##force dtype conversion to the same dtype as unit_set
            for col_name in ['building_id', 'bedrooms', 'unit_sqft']:
                if col_name in unit_set.get_known_attribute_names():
                    new_units[col_name] = new_units[col_name].astype(unit_set[col_name].dtype)

            unit_set.add_elements(new_units, require_all_attributes=False,
                                  change_ids_if_not_unique=True)
            unit_set.flush_dataset()

        for result in results:
            units = result[-1]
            nonres_sqft = 1 #result[6]/1000.0
            county = result[1]
            btype = result[2]
            key = (county,btype)
            aggd.setdefault(key,0)
            if btype < 7: aggd[key] += units
            else: aggd[key] += nonres_sqft
            aggd.setdefault(county,0)
            aggd[county] += units
    
    ######################These hard-coded counties are problematic!!!
    # aggf = open('county_aggregations-%d.csv' % current_year,'w')
    # county_names = {49:'son',41:'smt',1:'ala',43:'scl',28:'nap',38:'sfr',7:'cnc',48:'sol',21:'mar',0:'n/a'}
    # btype_names = {1:'SF',2:'SFBUILD',3:'MF',4:'MXMF',5:'CONDO',6:'MXC',7:'OF',8:'MXO',9:'CHOOD',10:'CAUTO',11:'CBOX',12:'MANU',13:'WHE'}
    # aggf.write('county,total,'+string.join(btype_names.values(),sep=',')+'\n')
    # for county in [38,41,43,1,7,48,28,49,21]:
        # aggf.write(county_names[county]+','+str(aggd.get(county,0)))
        # for btype in btype_names.keys():
            # key = (county,btype)
            # val = aggd.get(key,0) 
            # aggf.write(','+str(val))
        # aggf.write('\n')

    t2 = time.time()

    print("Finished in %f seconds" % (t2-t1))
    print("Ran optimization %d times" % devmdl_optimize.OBJCNT)
    global NOZONINGCNT, NOBUILDTYPES
    print("Did not find zoning for parcel %d times" % NOZONINGCNT)
    print("Did not find building types for parcel %d times" % NOBUILDTYPES)
    print("DONE")

    my.post_run() #remove price_shifter & cost_shifter to avoid them being cached

    if HOTSHOT:
        prof.stop()
        prof.close()
        stats = hotshot.stats.load('devmdl.prof')
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(20)

NOZONINGCNT = 0
NOBUILDTYPES = 0

def process_parcel(parcel):

        global parcel_set, z, node_set, zone_set, submarket, esubmarket, isr, parcelfees, costdiscount, i
        global NOZONINGCNT, NOBUILDTYPES
        global building_sqft

        debugoutput = ''
        current_year = SimulationState().get_current_time()
        pid = parcel_set['parcel_id'][parcel]
        county_id = parcel_set['county_id'][parcel]
        taz = parcel_set['zone_id'][parcel]
        if NODES:
            node_id = parcel_set['node_id'][parcel]
        
        zoning_id = parcel_set['zoning_id'][parcel]
        
        existing_sqft = building_sqft[parcel]

        existing_price = building_price[parcel]
        if existing_sqft < 0: existing_sqft = 0
        if existing_price < 0: existing_price = 0
        if DEBUG: print("parcel_id is %d" % pid)
        shape_area = parcel_set['parcel_sqft'][parcel]
        v = float(shape_area) #*10.7639
        
        if URBANVISION:
            #try: zoning = z.get_zoning(pid)
            try: zoning = zoning_id
            except: 
                return
            if zoning < 1:
                return
            btypes = z.get_building_types(zoning)

            if not zoning:
                NOZONINGCNT += 1
                return
            if not btypes:
                NOBUILDTYPES += 1
                return
            if v < 800:
                return
            if DEBUG > 0: print("Parcel size is %f" % v)
            ####################### Not having max far , max height, max dua
            far = z.get_far(pid)
            # height = int(z.get_attr(zoning,'max_height', 1000))
            # max_dua = int(z.get_attr(zoning,'max_dua', 100))
            # max_dua = min(max_dua,50)
            
            #far = 2
            height = 400
            max_dua = 100
            if DEBUG: print(far, height, max_dua)
            if far == 100 and height == 1000: far,height = .75,10
            bform = BForm(pid,v,far,height,max_dua,county_id,taz,isr,parcelfees,existing_sqft,existing_price)
        else:
            print("Need to flesh out the case where zoning data is entirely in cache")
            #bform = BForm(pid,v,far,height,max_dua,county_id,taz,isr,parcelfees,existing_sqft,existing_price)

        
        ################################################!!!!!!!!! Need to clarify the developer model's building typology
        if DEBUG > 0: print("ZONING BTYPES:", btypes)

        devmdl_btypes = []
        if 20 in btypes: devmdl_btypes+=[1,2] ##sf detached
        if 24 in btypes or 3 in btypes or 2 in btypes: ##sf attached and multifamily
            devmdl_btypes+=[3,5] # MF to MF-rental and MF-condo
        if 5 in btypes: devmdl_btypes.append(7) # office to office
        if 22 in btypes: # warehouse to warehouse
            devmdl_btypes.append(13)
        if 9 in btypes: devmdl_btypes.append(12) #industrial to manufacturing
        if 18 in btypes: devmdl_btypes+=[10,11,9] #retail to retail
        if 11 in btypes: devmdl_btypes+=[4,6] # mixed to MXD-MF and MXD-condo

        btypes = devmdl_btypes
        #print btypes
        if NODES:
            idx_node_parcel = numpy.where(node_set['node_id']==node_id)[0]
        else:
            idx_zone_parcel = numpy.where(zone_set['zone_id']==taz)[0]

        if DEBUG > 0: print("DEVMDL BTYPES:", btypes)
        
        npv = 0
        maxnpv, maxbuilding = 0, -1
        ## number of units and sqft_per_unit by number of bedrooms (1, 2, 3, 4)
        units = zeros(4, dtype='i4')
        sqft_per_unit = zeros(4, dtype='i4')

        for btype in btypes:
            
            if DEBUG > 0: print("building type = %s" % btype)
            
            if 1: #btype in [1,2,3,4,5,6]: # RESIDENTIAL
                if NODES:
                    zone_id = parcel_set['zone_id'][parcel]
                    lotsize = node_set['avg_sf_lot_size'][idx_node_parcel][0]
                    unitsize = node_set['avg_sf_unit_size'][idx_node_parcel][0]
                    unitsize2 = node_set['avg_mf_unit_size'][idx_node_parcel][0]
                    unitprice = node_set['avg_sf_unit_price'][idx_node_parcel][0]
                    unitprice2 = node_set['avg_mf_unit_price'][idx_node_parcel][0]
                    unitrent = node_set['avg_sf_unit_rent'][idx_node_parcel][0]
                    unitrent2 = node_set['avg_mf_unit_rent'][idx_node_parcel][0]
                    of_rent_sqft = node_set['avg_of_sqft_rent'][idx_node_parcel][0]
                    ret_rent_sqft = node_set['avg_ret_sqft_rent'][idx_node_parcel][0]
                    ind_rent_sqft = node_set['avg_ind_sqft_rent'][idx_node_parcel][0]
                else:
                    print("Need to flesh this section out with zonal variables")
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
            if numpy.isinf(price_per_sqft_sf): price_per_sqft_sf = 0
            if numpy.isinf(price_per_sqft_mf): price_per_sqft_mf = 0
            if numpy.isinf(rent_per_sqft_sf): rent_per_sqft_sf = 0
            if numpy.isinf(rent_per_sqft_mf): rent_per_sqft_mf = 0
            if numpy.isinf(of_rent_sqft): of_rent_sqft = 0
            if numpy.isinf(ret_rent_sqft): ret_rent_sqft = 0
            if numpy.isinf(ind_rent_sqft): ind_rent_sqft = 0
            if of_rent_sqft < 7: of_rent_sqft = 7
            if ret_rent_sqft < 7: ret_rent_sqft = 7
            if ind_rent_sqft < 7: ind_rent_sqft = 7
            #if price_per_sqft_mf > 700: price_per_sqft_mf = 700
            #price_per_sqft_mf *= .35
            price_per_sqft_mf *= price_shifters['price_per_sqft_mf']
            #if price_per_sqft_mf > 1.5 * price_per_sqft_sf:
            #    price_per_sqft_mf = 1.5 * price_per_sqft_sf
            #price_per_sqft_mf = price_per_sqft_sf*.5
            if DEBUG > 0: print("price_per_sqft_sf:", price_per_sqft_sf, "price_per_sqft_mf:", price_per_sqft_mf, "rent_per_sqft_sf:", rent_per_sqft_sf, "rent_per_sqft_mf:", rent_per_sqft_mf)
            if DEBUG > 0: print("of_rent_sqft:", of_rent_sqft, "ret_rent_sqft:", ret_rent_sqft, "ind_rent_sqft:", ind_rent_sqft)
            #prices = (price_per_sqft_sf*1.2,price_per_sqft_mf,rent_per_sqft_sf,rent_per_sqft_mf*2,of_rent_sqft*1.85,ret_rent_sqft*1.85,ind_rent_sqft*2.5)
            prices = (price_per_sqft_sf*1.0*price_shifters['price_per_sqft_sf'],
                      price_per_sqft_mf*1.0,
                      rent_per_sqft_sf*1.0*price_shifters['rent_per_sqft_sf'],
                      rent_per_sqft_mf*1.0*price_shifters['rent_per_sqft_mf'],
                      of_rent_sqft*price_shifters['of_rent_sqft'],
                      ret_rent_sqft*price_shifters['ret_rent_sqft'],
                      ind_rent_sqft*price_shifters['ind_rent_sqft'])
            if not lotsize: lotsize = 11111    
            if lotsize <1000:  lotsize = 11111   
            if lotsize>20000: lotsize=20000
            if DEBUG > 0: print("zone:", zone_id, "lotsize:", lotsize, "HS size:", unitsize, "MF size:", unitsize2)
            bform.set_unit_sizes(lotsize,unitsize,unitsize2)

            bform.set_btype(btype)

            #parking = z.get_parking_requirements(pid, btype)
            parking = None

            bform.set_parking(parking)  ############add parking info for DRCOG!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            #if 1: print btype
            #pjurisdiction = parcel_set['jurisdiction_id'][parcel]
            #pschooldistrict = parcel_set['schooldistrict'][parcel]
            pzone = parcel_set['zone_id'][parcel]
            ptransit = parcel_set['within_half_mile_transit'][parcel]

            sub_idx = where(logical_and(submarket['zone_id'] == taz,
                                       submarket['within_half_mile_transit'] == ptransit)
                           )[0]
            submarket_info = {}
            for attr in submarket.get_known_attribute_names():
                submarket_info[attr] = submarket[attr][sub_idx]
            esub_idx = where(logical_and(esubmarket['zone_id'] == taz,
                                        esubmarket['within_half_mile_transit'] == ptransit)
                           )[0]
            esubmarket_info = {}
            for attr in esubmarket.get_known_attribute_names():
                esubmarket_info[attr] = esubmarket[attr][esub_idx]
            
            submarket_pool = submarkets.setup_dataset_pool(opus=False,btype=btype,submarket_info=submarket_info,esubmarket_info=esubmarket_info)  ###Look into this
            
            X, npv = devmdl_optimize.optimize(bform,prices,costdiscount,
                                              submarket_pool)
            if DEBUG: print(X, npv)
            bformdbg = (county_id,far,height,max_dua,bform.sf_builtarea(),bform.sfunitsizes,bform.mf_builtarea(),bform.mfunitsizes,bform.num_units,bform.nonres_sqft,bform.buildable_area)
            pfeesstr = ''
            if parcelfees: pfeesstr = parcelfees.get(pid)

            otherdbg = (isr,pfeesstr,existing_sqft,existing_price,lotsize,unitsize,unitsize2,string.join([str(x) for x in bform.sales_absorption],'|'),string.join([str(x) for x in bform.rent_absorption],'|'),string.join([str(x) for x in bform.leases_absorption],'|'),string.join([str(x) for x in bform.sales_vacancy_rates],'|'),string.join([str(x) for x in bform.vacancy_rates],'|'))
            debugoutput += string.join([str(x) for x in [pid,btype,npv,bform.actualfees]+list(prices)+list(bformdbg)+list(otherdbg)]
,sep=',')+'\n'
            #if npv == -1: return # error code
            if npv > maxnpv:
                maxnpv = npv
                nonres_sqft = bform.nonres_sqft
                sqft = nonres_sqft # add residential below
                if btype in [1,2,3,4,5,6]: # RESIDENTIAL 
                    if btype in [1,2]: 
                        res_sqft = bform.sf_builtarea()
                        sqft_per_unit = bform.sfunitsizes
                    else: 
                        res_sqft = bform.mf_builtarea()
                        sqft_per_unit = bform.mfunitsizes
                    sqft += res_sqft
                    res_units = sum(bform.num_units)
                else:
                    res_sqft = 0
                    res_units = 0
                stories = sqft / bform.buildable_area

                #this is to be recoded tenure: 1 - rent, 2 - own from 0 - own, 1 - rent
                tenure = 0
                if btype in [3,4]: tenure = 2
                year_built = current_year
                stories = math.ceil(stories)
                sqft = math.floor(sqft)
                res_sqft = math.floor(res_sqft)
                nonres_sqft = math.floor(nonres_sqft)
                res_units = math.ceil(res_units) # these are partial units, but usually very close to one
                # it's not mixed if the nonres gets optimized out
                #if btype in [4,6] and nonres_sqft == 0: btype = 3
                if btype in [1,2]: btype = 20
                if btype in [3,4]: btype = 2
                if btype in [5,6]: btype = 3
                if btype in [7,8]: btype = 5
                if btype in [9,10,11]: btype = 18
                if btype == 12: btype = 9
                if btype == 13: btype = 22
                if btype == 14: btype = 23
                building = (pid, county_id, btype, stories, sqft, res_sqft, nonres_sqft, tenure, year_built, res_units, npv, bform.actualfees)
                maxbuilding = building
                units = bform.num_units
                
        return maxbuilding, (units, sqft_per_unit), debugoutput
