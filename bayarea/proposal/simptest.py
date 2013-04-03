# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from bform import BForm
import submarkets
import devmdl_optimize

pid = -1 # only used for parecl fees
parcel_size = 2000.0
far = 2
height = 20
max_dua = 3
county_id = 39 # for use with cost shifters
taz = -1 # as long as isr below is off this won't be used 
isr = None
parcelfees = None
existing_sqft = 0 # for demolition cost
existing_price = 0 # for procurement cost

bform = BForm(pid,parcel_size,far,height,max_dua,county_id,taz,isr,parcelfees,existing_sqft,existing_price)

lotsize = 4000 # average lot size in the area
unitsize = 1500 # average sf unit size in the area
unitsize2 = 1200 # average mf unit size in the area
bform.set_unit_sizes(lotsize,unitsize,unitsize2)

btype = 1 # single family
bform.set_btype(btype)
  
sfprice = 400
mfprice = 150
sfrent = 2
mfrent = 1.5
ofrent = 2.25
retrent = 3
indrent = 1
prices = (sfprice,mfprice,sfrent,mfrent,ofrent,retrent,indrent)
  
costdiscount = 0.0

submarket_pool = submarkets.setup_dataset_pool(opus=False,btype=btype, \
                                   submarket_info=None,esubmarket_info=None)
prop_comp = submarket_pool['proposal_component']

prop_comp['sales_absorption'] = [.05]*5
prop_comp['rent_absorption'] = [4]*5
prop_comp['leases_absorption'] = [4]*5
prop_comp['sales_vacancy_rates'] = [.005]*5
prop_comp['vacancy_rates'] = [.005]*5

X, npv = devmdl_optimize.optimize(bform,prices,costdiscount,submarket_pool)

print X, npv
