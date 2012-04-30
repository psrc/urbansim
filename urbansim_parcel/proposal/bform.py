import numpy
from math import ceil
from numpy import array
import devmdl_optimize

FLOORHEIGHT = 12
LOTRATIOS = array([.71,.79,.93,1.16]) # ratio of 1BR, 2BR, etc to average
UNITRATIOS = array([.835,1.15,1.5,1.72]) # ratio of 1BR, 2BR, etc to average
RENTFACTOR = .9 # ratio of rent to ave
CONDOFACTOR = 1.1 # ratio of own to ave

class BForm:

    def __init__(my,parcel_size,FAR,height,max_dua,county,taz,isr,existing_sqft,existing_price):
        my.height = height
        my.FAR = FAR
        my.max_dua = max_dua
        my.existing_sqft = existing_sqft
        my.existing_price = existing_price
        my.parcel_size = parcel_size
        my.buildable_area = parcel_size*.8
        
        far_area = FAR*parcel_size
        height_area = height/FLOORHEIGHT*my.buildable_area
        my.max_floor_area = min(far_area,height_area)
        my.num_units = array([0, 0, 0, 0])
        my.nonres_sqft = 0
        if county not in LOCALCOST_D: localcost = 100.0 # happens in a few cases
        else: localcost = LOCALCOST_D[county]
        my.F = COSTFACTOR * localcost/100.0
        my.isr = isr
        my.taz = taz

    def set_btype(my,btype):
        my.btype = btype

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
        cons = my.max_floor_area - X[0]*devmdl_optimize.SQFTFACTOR
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
        cost += numpy.sum(my.num_units)*my.isr.res_isr_fee(my.taz)
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
        F = my.F
        cost = 0
        if btype == 7 or btype == 8:
            if height < 25: cost += sqft*OFFICELOWRISE*F
            elif height < 45: cost += sqft*OFFICEMIDRISE*F
            elif height < 85: cost += sqft*OFFICEMID2RISE*F
            elif height < 120: cost += sqft*OFFICEHIGHRISE*F
        elif btype == 9: cost += sqft*NEIGHBORHOODRETAIL*F
        elif btype == 10: cost += sqft*AUTORETAIL*F
        elif btype == 11: cost += sqft*BIGBOXRETAIL*F
        elif btype == 12: cost += sqft*INDUSTRIAL*F
        elif btype == 13: cost += sqft*WAREHOUSE*F
        elif btype == 14: cost += sqft*LODGING*F
        else: assert 0

        cost += my.isr.nonres_isr_fee(my.taz)*sqft
        #print cost
        return cost

    def mf_cost(my,mf='apt'):
        F = my.F
        cost = 0
        height = my.get_height()
        #assert height >= 0 and height < 250
        if mf == 'apt': sqft = numpy.dot(my.mfunitsizes,my.num_units)
        elif mf == 'condo': sqft = numpy.dot(my.condounitsizes,my.num_units)
        if height < 25: cost += sqft*MFLOWRISE*F
        elif height < 45: cost += sqft*MFMIDRISE*F
        elif height < 85: cost += sqft*MFMID2RISE*F
        elif height < 120: cost += sqft*MFHIGHRISE*F
        else: cost += sqft*MFSKYSCRAPER*F
        cost += numpy.sum(my.num_units)*IMPACTFEE
        cost += numpy.sum(my.num_units)*my.isr.res_isr_fee(my.taz)
        cost += my.nonres_sqft*GROUNDFLOORRETAIL*F
        return cost

DEMOCOST = 5.0
COSTFACTOR = 1.5
SFCOST = 140.0
SFBUILDEREFFICIENCY = .9
MFBUILDEREFFICIENCY = .8
MFLOWRISE = 140.0
MFMIDRISE = 140.0*1.2
MFMID2RISE = 168.00*1.2
MFHIGHRISE = 168.00*1.3
MFSKYSCRAPER = 200.0
IMPACTFEE = 8000.0
GROUNDFLOORRETAIL = 120.0
NEIGHBORHOODRETAIL = 100.0
AUTORETAIL = 100.0
BIGBOXRETAIL = 100.0
INDUSTRIAL = 50.0
WAREHOUSE = 50.0
LODGING = 200.0
OFFICELOWRISE = 100.00
OFFICEMIDRISE = 110.00
OFFICEMID2RISE = 120.00
OFFICEHIGHRISE = 130.00
OFFICESKYSCRAPER = 140.00
SFPARKING = array([18000.0,30000.0,30000.0,36000.0])
LOCALCOST_D = {
49:115.58, # sonoma
41:114.6, # san mateo
1:116.2, # alameda
43:117.1, # santa clara
28:115.58, # napa
38:123.8, # san fran
7:112.9, # contra costa
48:110.5, # solano
21:115.58 # marin 
}
