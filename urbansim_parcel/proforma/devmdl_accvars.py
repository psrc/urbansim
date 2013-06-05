# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import array
import numpy
from bayarea.accessibility.pyaccess import PyAccess

def compute_devmdl_accvars_nodal(node_set):
    node_ids = array(node_set.node_ids, dtype="int32")

    node_sum_unit_sqft_sf = node_set.compute_variables('node.aggregate((drcog.building.building_sqft - building.non_residential_sqft)*(building.residential_units>0)*(building.building_type_id==20),intermediates=[parcel])')
    node_sum_unit_sqft_sf = array(node_sum_unit_sqft_sf, dtype="float32")

    node_sum_unit_sqft_mf = node_set.compute_variables('node.aggregate((drcog.building.building_sqft - building.non_residential_sqft)*(building.residential_units>0)*(numpy.in1d(building.building_type_id,[2,3,24])),intermediates=[parcel])')
    node_sum_unit_sqft_mf = array(node_sum_unit_sqft_mf, dtype="float32")

    node_sum_sf_parcel_area = node_set.compute_variables('node.aggregate((building.disaggregate(parcel.parcel_sqft))*(building.residential_units==1)*(building.building_type_id==20),intermediates=[parcel])')
    node_sum_sf_parcel_area = array(node_sum_sf_parcel_area, dtype="float32")

    node_sum_sf_price = node_set.compute_variables('node.aggregate((residential_unit.sale_price/1000)*(residential_unit.sale_price>0)*(residential_unit.disaggregate(building.building_type_id==20)),intermediates=[building,parcel])')
    #node_sum_sf_price_sqft = node_set.compute_variables('node.aggregate((residential_unit.unit_sqft)*(residential_unit.sale_price>0)*(residential_unit.disaggregate(building.building_type_id<2)),intermediates=[building,parcel])')
    node_sum_sf_price_sqft = node_set.compute_variables('node.aggregate((1)*(residential_unit.sale_price>0)*(residential_unit.disaggregate(building.building_type_id==20)),intermediates=[building,parcel])')
    node_sum_sf_price = array(node_sum_sf_price, dtype="float32")
    node_sum_sf_price_sqft = array(node_sum_sf_price_sqft, dtype="float32")
    
    node_sum_mf_price = node_set.compute_variables('node.aggregate((residential_unit.sale_price/1000)*(residential_unit.sale_price>0)*(residential_unit.disaggregate(numpy.in1d(building.building_type_id,[2,3,24]))),intermediates=[building,parcel])')
    #node_sum_mf_price_sqft = node_set.compute_variables('node.aggregate((residential_unit.unit_sqft)*(residential_unit.sale_price>0)*(residential_unit.disaggregate(building.building_type_id==3)),intermediates=[building,parcel])')
    node_sum_mf_price_sqft = node_set.compute_variables('node.aggregate((1)*(residential_unit.sale_price>0)*(residential_unit.disaggregate(numpy.in1d(building.building_type_id,[2,3,24]))),intermediates=[building,parcel])')
    node_sum_mf_price = array(node_sum_mf_price, dtype="float32")
    node_sum_mf_price_sqft = array(node_sum_mf_price_sqft, dtype="float32")
    #for i in range(node_sum_mf_price.size):
    #    print node_sum_mf_price[i], node_sum_mf_price_sqft[i], node_sum_mf_price[i]/node_sum_mf_price_sqft[i]

    node_sum_sf_rent = node_set.compute_variables('node.aggregate((residential_unit.rent)*(residential_unit.rent>0)*(residential_unit.disaggregate(building.building_type_id==20)),intermediates=[building,parcel])')
    #node_sum_sf_rent_sqft = node_set.compute_variables('node.aggregate((residential_unit.rent)*(residential_unit.rent>0)*(residential_unit.disaggregate(building.building_type_id<2)),intermediates=[building,parcel])')
    node_sum_sf_rent_sqft = node_set.compute_variables('node.aggregate((1)*(residential_unit.rent>0)*(residential_unit.disaggregate(building.building_type_id==20)),intermediates=[building,parcel])')
    node_sum_sf_rent = array(node_sum_sf_rent, dtype="float32")
    node_sum_sf_rent_sqft = array(node_sum_sf_rent_sqft, dtype="float32")

    node_sum_mf_rent = node_set.compute_variables('node.aggregate((residential_unit.rent)*(residential_unit.rent>0)*(residential_unit.disaggregate(numpy.in1d(building.building_type_id,[2,3,24]))),intermediates=[building,parcel])')
    #node_sum_mf_rent_sqft = node_set.compute_variables('node.aggregate((residential_unit.unit_sqft)*(residential_unit.rent>0)*(residential_unit.disaggregate(building.building_type_id==3)),intermediates=[building,parcel])')
    node_sum_mf_rent_sqft = node_set.compute_variables('node.aggregate((1)*(residential_unit.rent>0)*(residential_unit.disaggregate(numpy.in1d(building.building_type_id,[2,3,24]))),intermediates=[building,parcel])')
    node_sum_mf_rent = array(node_sum_mf_rent, dtype="float32")
    node_sum_mf_rent_sqft = array(node_sum_mf_rent_sqft, dtype="float32")
    
    ##node_sum_of_rent = node_set.compute_variables('node.aggregate((building.non_residential_rent)*(building.non_residential_rent>0)*(building.building_type_id==4),intermediates=[parcel])')  
    node_sum_of_rent = node_set.compute_variables('node.aggregate((building.non_residential_rent)*(building.non_residential_rent>0)*(building.building_type_id==5),intermediates=[parcel])')
    ##node_sum_of_rent_sqft = node_set.compute_variables('node.aggregate((1)*(building.non_residential_rent>0)*(building.building_type_id==4),intermediates=[parcel])')
    node_sum_of_rent_sqft = node_set.compute_variables('node.aggregate((1)*(building.non_residential_rent>0)*(building.building_type_id==5),intermediates=[parcel])')  ##This varname is sum of nonres sqft, but what the variable is actually coded as is rent per building....  which one is desired?
    node_sum_of_rent = array(node_sum_of_rent, dtype="float32")
    node_sum_of_rent_sqft = array(node_sum_of_rent_sqft, dtype="float32")
    
    node_sum_ret_rent = node_set.compute_variables('node.aggregate((building.non_residential_rent)*(building.non_residential_rent>0)*(building.building_type_id==18),intermediates=[parcel])')
    node_sum_ret_rent_sqft = node_set.compute_variables('node.aggregate((1)*(building.non_residential_rent>0)*(building.building_type_id==18),intermediates=[parcel])')
    node_sum_ret_rent = array(node_sum_ret_rent, dtype="float32")
    node_sum_ret_rent_sqft = array(node_sum_ret_rent_sqft, dtype="float32")
    
    node_sum_ind_rent = node_set.compute_variables('node.aggregate((building.non_residential_rent)*(building.non_residential_rent>0)*(building.building_type_id==9),intermediates=[parcel])')
    node_sum_ind_rent_sqft = node_set.compute_variables('node.aggregate((1)*(building.non_residential_rent>0)*(building.building_type_id==9),intermediates=[parcel])')
    node_sum_ind_rent = array(node_sum_ind_rent, dtype="float32")
    node_sum_ind_rent_sqft = array(node_sum_ind_rent_sqft, dtype="float32")
    ####When predicting building-level non-residential rents, focus on these core non-res types above that are best represented in the model
    node_number_of_sf_resunits = node_set.compute_variables('node.aggregate((building.residential_units)*(building.residential_units>0)*(building.building_type_id==20),intermediates=[parcel])')
    node_number_of_sf_resunits = array(node_number_of_sf_resunits, dtype="float32")

    node_number_of_mf_resunits = node_set.compute_variables('node.aggregate((building.residential_units)*(building.residential_units>0)*(numpy.in1d(building.building_type_id,[2,3,24])),intermediates=[parcel])')
    node_number_of_mf_resunits = array(node_number_of_mf_resunits, dtype="float32")

    node_number_of_sfdetach_resunits = node_set.compute_variables('node.aggregate((building.residential_units)*(building.residential_units>0)*(building.building_type_id==20),intermediates=[parcel])')
    node_number_of_sfdetach_resunits = array(node_number_of_sfdetach_resunits, dtype="float32")
    
    node_set.pya.initializeAccVars(20)
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
    node_set.pya.initializeAccVar(10,node_ids,node_sum_sf_price_sqft)
    node_set.pya.initializeAccVar(11,node_ids,node_sum_mf_price_sqft)
    node_set.pya.initializeAccVar(12,node_ids,node_sum_sf_rent_sqft)
    node_set.pya.initializeAccVar(13,node_ids,node_sum_mf_rent_sqft)
    node_set.pya.initializeAccVar(14,node_ids,node_sum_of_rent)
    node_set.pya.initializeAccVar(15,node_ids,node_sum_of_rent_sqft)
    node_set.pya.initializeAccVar(16,node_ids,node_sum_ret_rent)
    node_set.pya.initializeAccVar(17,node_ids,node_sum_ret_rent_sqft)
    node_set.pya.initializeAccVar(18,node_ids,node_sum_ind_rent)
    node_set.pya.initializeAccVar(19,node_ids,node_sum_ind_rent_sqft)

    sf_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,0,0,2,0)
    sf_units=node_set.pya.getAllAggregateAccessibilityVariables(3000,1,0,2,0)
    #sf_sqft=sf_sqft.astype(numpy.int32)
    #sf_units=sf_units.astype(numpy.int32)
    result=numpy.divide(sf_sqft,sf_units)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_sf_unit_size', data=result)

    mf_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,2,0,2,0)
    mf_units=node_set.pya.getAllAggregateAccessibilityVariables(3000,3,0,2,0)
    #mf_sqft=mf_sqft.astype(numpy.int32)
    #mf_units=mf_units.astype(numpy.int32)
    result=numpy.divide(mf_sqft,mf_units)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_mf_unit_size', data=result)

    parcel_area=(node_set.pya.getAllAggregateAccessibilityVariables(3000,4,0,2,0))  #####*10.7639 No need, denver parcel area is already in terms of sqft
    sfdetach_resunits=node_set.pya.getAllAggregateAccessibilityVariables(3000,5,0,2,0)
    #parcel_area=parcel_area.astype(numpy.int32)
    #sfdetach_resunits=sfdetach_resunits.astype(numpy.int32)
    result=numpy.divide(parcel_area,sfdetach_resunits)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_sf_lot_size', data=result)

    sf_price=node_set.pya.getAllAggregateAccessibilityVariables(3000,6,0,2,0)
    sf_price_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,10,0,2,0)
    #sf_price=sf_price.astype(numpy.int32)
    result=numpy.divide(sf_price,sf_price_sqft)
    result = numpy.nan_to_num(result)*1000
    node_set.add_primary_attribute(name='avg_sf_unit_price', data=result)
    #for i in range(result.size):
    #    print sf_price[i], sf_price_sqft[i], result[i]

    mf_price=node_set.pya.getAllAggregateAccessibilityVariables(3000,7,0,2,0)
    mf_price_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,11,0,2,0)
    #mf_price=mf_price.astype(numpy.int32)
    result=numpy.divide(mf_price,mf_price_sqft)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_mf_unit_price', data=(result*1000))

    sf_rent=node_set.pya.getAllAggregateAccessibilityVariables(3000,8,0,2,0)
    sf_rent_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,12,0,2,0)
    #sf_rent=sf_rent.astype(numpy.int32)
    result=numpy.divide(sf_rent,sf_rent_sqft)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_sf_unit_rent', data=result)

    mf_rent=node_set.pya.getAllAggregateAccessibilityVariables(3000,9,0,2,0)
    mf_rent_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,13,0,2,0)
    #mf_rent=mf_rent.astype(numpy.int32)
    result=numpy.divide(mf_rent,mf_rent_sqft)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_mf_unit_rent', data=result)
    
    of_rent=node_set.pya.getAllAggregateAccessibilityVariables(3000,14,0,2,0)
    of_rent_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,15,0,2,0)
    result=numpy.divide(of_rent,of_rent_sqft)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_of_sqft_rent', data=result)
    #for i in range(result.size):
    #    print of_rent[i], of_rent_sqft[i], result[i]
    
    ret_rent=node_set.pya.getAllAggregateAccessibilityVariables(3000,16,0,2,0)
    ret_rent_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,17,0,2,0)
    result=numpy.divide(ret_rent,ret_rent_sqft)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_ret_sqft_rent', data=result)
    
    ind_rent=node_set.pya.getAllAggregateAccessibilityVariables(3000,18,0,2,0)
    ind_rent_sqft=node_set.pya.getAllAggregateAccessibilityVariables(3000,19,0,2,0)
    result=numpy.divide(ind_rent,ind_rent_sqft)
    result = numpy.nan_to_num(result)
    node_set.add_primary_attribute(name='avg_ind_sqft_rent', data=result)

def compute_devmdl_accvars_zonal(zone_set):
    print "Need to flesh this section out with zonal variables"