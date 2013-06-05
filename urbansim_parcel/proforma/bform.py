# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import numpy
from math import ceil
from numpy import array
import devmdl_optimize
from shifters import RESLOCALCOST_D, NONRESLOCALCOST_D, MAXNONRESSIZE_D

FLOORHEIGHT = 12
LOTRATIOS = array([.71,.79,.93,1.16]) # ratio of 1BR, 2BR, etc to average
UNITRATIOS = array([.835,1.15,1.5,1.72]) # ratio of 1BR, 2BR, etc to average
RENTFACTOR = .9 # ratio of rent to ave
CONDOFACTOR = 1.1 # ratio of own to ave

MAXNONRESSIZE = 800000.0
DEMOCOST = 5.0
NONRESCOSTFACTOR = 1.0
RESCOSTFACTOR = 0.125
SFCOST = 105.0

SFBUILDEREFFICIENCY = 1.0
MFBUILDEREFFICIENCY = .9
MFLOWRISE = 140.0
MFMIDRISE = 172.0 #*1.2
MFMID2RISE = 176.00 #*1.2
MFHIGHRISE = 230.00 #*1.3
MFSKYSCRAPER = 230.0
IMPACTFEE = 8000.0
GROUNDFLOORRETAIL = 140.0
NEIGHBORHOODRETAIL = 122.0
AUTORETAIL = 106.0
BIGBOXRETAIL = 114.0
INDUSTRIAL = 130.0
WAREHOUSE = 96.0
LODGING = 181.0
OFFICELOWRISE = 178.00
OFFICEMIDRISE = 185.00
OFFICEMID2RISE = 176.00
OFFICEHIGHRISE = 173.00
OFFICESKYSCRAPER = 173.00
PARKINGCOSTPERSPOT = 18000.0
SFPARKING = array([18000.0,30000.0,30000.0,36000.0])

class BForm:

    def __init__(my,parcel_id,parcel_size,FAR,height,max_dua,county,taz,isr,parcelfees,existing_sqft,existing_price):
        my.height = height
        my.FAR = FAR
        my.max_dua = max_dua
        my.existing_sqft = existing_sqft
        my.existing_price = existing_price
        my.parcel_size = parcel_size
        my.buildable_area = parcel_size*.8 #####
        my.btype = None
        my.parking = None
    
        my.sales_absorption = []
        my.rent_absorption = []
        my.leases_absorption = []
        my.sales_vacancy_rates = []
        my.vacancy_rates = []
        
        far_area = FAR*parcel_size
        height_area = height/FLOORHEIGHT*my.buildable_area
        my.max_floor_area = min(far_area,height_area)
        my.num_units = array([0, 0, 0, 0])
        my.nonres_sqft = 0
        if county not in RESLOCALCOST_D: 
            localcost = 100.0 # happens in a few cases
            localcost2 = 100.0 # happens in a few cases
        else: 
            localcost = RESLOCALCOST_D[county]
            localcost2 = NONRESLOCALCOST_D[county]
        my.F = RESCOSTFACTOR * localcost/100.0
        my.F2 = NONRESCOSTFACTOR * localcost2/100.0
        if county in MAXNONRESSIZE_D:
            my.maxnonressize = MAXNONRESSIZE_D[county]
        else:
            my.maxnonressize = MAXNONRESSIZE
        my.isr = isr
        my.parcelfees = parcelfees
        my.actualfees = 0
        my.taz = taz
        my.parcel_id = parcel_id

    def set_btype(my,btype):
        my.btype = btype

    def set_parking(my,parking):
        my.parking = parking

    def set_unit_sizes(my,lotsize,sfunitsize,mfunitsize):
        #print lotsize, sfunitsize, mfunitsize
        my.lotsize = lotsize*LOTRATIOS
        my.sfunitsizes = sfunitsize*LOTRATIOS
        my.mfunitsizes = mfunitsize*RENTFACTOR*UNITRATIOS
        my.condounitsizes = mfunitsize*CONDOFACTOR*UNITRATIOS

    def set_num_units(my,num_units):
        my.num_units = num_units

    def set_nonres_sqft(my,nonres_sqft):
        my.nonres_sqft = nonres_sqft

    def sfoneoff_bounds(my,X,*args):
        # there's a bug here - need to make sure a single family house actually
        # fits on this lot - I suppose by respecting height / FAR limits
        return numpy.append(X,1 - numpy.sum(X))

    def sfbuilder_bounds(my,X,*args):
        Y = numpy.append(X,my.parcel_size/43560.0*my.max_dua - numpy.sum(X))
        Y = numpy.append(Y,my.parcel_size*SFBUILDEREFFICIENCY - numpy.dot(my.lotsize,X))
        return Y

    def sf_builtarea(my):
        return numpy.dot(my.sfunitsizes,my.num_units)

    def mf_builtarea(my,X=None):
        if X == None: 
            sqft = numpy.dot(my.mfunitsizes,my.num_units) + my.nonres_sqft
            return sqft / MFBUILDEREFFICIENCY

        sqft = numpy.dot(my.mfunitsizes,X[:4])
        # ground floor retail
        if len(X) == 5: sqft += X[4]*devmdl_optimize.SQFTFACTOR 
        return sqft / MFBUILDEREFFICIENCY

    def mf_bounds(my,X,*args):
        Y = numpy.append(X,my.parcel_size/43560.0*my.max_dua - numpy.sum(X))
        Y = numpy.append(Y,my.max_floor_area - my.mf_builtarea(X))
        #print my.max_floor_area, my.mf_builtarea(X), X
        #print my.parcel_size/43560.0*my.max_dua, numpy.sum(X)
        return Y

    def commercial_bounds(my,X,*args):
        cons = min(my.max_floor_area,my.maxnonressize) - X[0]*devmdl_optimize.SQFTFACTOR
        #print "cons", cons
        #print "FA", my.max_floor_area
        return array([X[0],cons])

    def procurement_cost(my):
        cost = 0
        cost += my.existing_sqft*DEMOCOST
        cost += my.existing_price
        return cost

    def sf_cost(my):
        F = my.F
        cost = numpy.dot(my.sfunitsizes,my.num_units)*SFCOST*F
        cost += numpy.sum(my.num_units)*IMPACTFEE
        if my.parking: cost += numpy.sum(my.num_units)*PARKINGCOSTPERSPOT
        if my.isr: cost += numpy.sum(my.num_units)*my.isr.res_isr_fee(my.taz)
        if my.parcelfees: 
            my.actualfees = numpy.sum(my.num_units)*\
                                my.parcelfees.resother_parcel_fee(my.parcel_id)
            cost += my.actualfees
        cost += numpy.dot(SFPARKING,my.num_units)*F
        return cost

    def get_height(my):
        builtarea = my.mf_builtarea()
        footprint = min(my.buildable_area,my.max_floor_area)
        if footprint == 0: return 0
        return ceil(builtarea/footprint)*FLOORHEIGHT

    def commercial_cost(my,btype):
        sqft = my.nonres_sqft
        height = my.get_height()
        F2 = my.F2
        cost = 0
        MULT = 1.0
        if btype in [9,10,11,12,13] and height > 14: MULT = 2.5 ### Add parking costs here
        if btype == 7 or btype == 8:
            if height < 25: cost += sqft*OFFICELOWRISE*F2
            elif height < 45: cost += sqft*OFFICEMIDRISE*F2
            elif height < 85: cost += sqft*OFFICEMID2RISE*F2
            elif height < 120: cost += sqft*OFFICEHIGHRISE*F2
        elif btype == 9: cost += sqft*NEIGHBORHOODRETAIL*F2*MULT ####
        elif btype == 10: cost += sqft*AUTORETAIL*F2*MULT
        elif btype == 11: cost += sqft*BIGBOXRETAIL*F2*MULT
        elif btype == 12: cost += sqft*INDUSTRIAL*F2*MULT
        elif btype == 13: cost += sqft*WAREHOUSE*F2*MULT
        elif btype == 14: cost += sqft*LODGING*F2
        else: assert 0
        
        if my.isr: cost += my.isr.nonres_isr_fee(my.taz)*sqft
        if my.parcelfees: 
            my.actualfees = sqft*my.parcelfees.nonres_parcel_fee(my.parcel_id)
            cost += my.actualfees
        #print cost
        return cost

    def mf_cost(my,mf='apt'):
        F = my.F
        F2 = my.F2
        cost = 0
        height = my.get_height()
        #assert height >= 0 and height < 250
        sqft = numpy.dot(my.mfunitsizes,my.num_units)
        #if mf == 'apt': sqft = numpy.dot(my.mfunitsizes,my.num_units)
        #elif mf == 'condo': sqft = numpy.dot(my.condounitsizes,my.num_units)
        if height < 25: cost += sqft*MFLOWRISE*F
        elif height < 45: cost += sqft*MFMIDRISE*F
        elif height < 85: cost += sqft*MFMID2RISE*F
        elif height < 120: cost += sqft*MFHIGHRISE*F
        else: cost += sqft*MFSKYSCRAPER*F
        cost += numpy.sum(my.num_units)*IMPACTFEE
        if my.parking: cost += numpy.sum(my.num_units)*PARKINGCOSTPERSPOT
        if my.isr: cost += numpy.sum(my.num_units)*my.isr.res_isr_fee(my.taz)
        if my.parcelfees: 
            my.actualfees = numpy.sum(my.num_units)*\
                                my.parcelfees.resmf_parcel_fee(my.parcel_id)
            cost += my.actualfees
        cost += my.nonres_sqft*GROUNDFLOORRETAIL*F2
        return cost
