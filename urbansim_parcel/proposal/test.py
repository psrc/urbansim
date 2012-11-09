from bform import BForm
import submarkets
import devmdl_optimize
import csv, string

TESTFILE = 'proforma-debug-2011.csv'
f = csv.DictReader(open(TESTFILE))
c = 0
for r in f:
  #print r
  try:
    pid = int(r['pid'])
  except:
    continue # some bad logging info
  parcel_size = float(r['bform.buildable_area'])/.8
  far = float(r['far'])
  height = float(r['height'])
  max_dua = float(r['max_dua'])
  county_id = int(r['county_id'])
  taz = -1 # as long as isr below is off this won't be used 
  isr = None
  parcelfees = None
  existing_sqft = float(r['existing_sqft'])
  existing_price =  float(r['existing_price'])

  bform = BForm(pid,parcel_size,far,height,max_dua,county_id,taz,isr,parcelfees,existing_sqft,existing_price)
  lotsize = float(r['lotsize'])
  unitsize = float(r['unitsize'])
  unitsize2 = float(r['unitsize2'])
  bform.set_unit_sizes(lotsize,unitsize,unitsize2)
  btype = int(r['btype'])
  bform.set_btype(btype)
  
  prices = (r['pricesf'],r['pricemf'],r['rentsf'],r['rentmf'],r['rentof'],r['rentret'],r['rentind'])
  prices = tuple([float(x) for x in prices])
  prices
  costdiscount = 0.0

  submarket_pool = submarkets.setup_dataset_pool(opus=False,btype=btype, \
                                   submarket_info=None,esubmarket_info=None)

  prop_comp = submarket_pool['proposal_component']

  if r['bform.sales_absorption']:
    prop_comp['sales_absorption'] = [float(x) for x in string.split(r['bform.sales_absorption'],'|')]
  if r['bform.rent_absorption']:
    prop_comp['rent_absorption'] = [float(x) for x in string.split(r['bform.rent_absorption'],'|')]
  if r['bform.leases_absorption']:
    prop_comp['leases_absorption'] = [float(x) for x in string.split(r['bform.leases_absorption'],'|')]
  if r['bform.sales_vacancy_rates']:
    prop_comp['sales_vacancy_rates'] = [float(x) for x in string.split(r['bform.sales_vacancy_rates'],'|')]
  if r['bform.vacancy_rates']:
    prop_comp['vacancy_rates'] = [float(x) for x in string.split(r['bform.vacancy_rates'],'|')]

  X, npv = devmdl_optimize.optimize(bform,prices,costdiscount,submarket_pool)

  print X, npv
  print bform.actualfees

  c += 1
  if c == 10: break
