from numpy import array
from bayarea.accessibility.pyaccess import PyAccess

def compute_devmdl_accvars(node_set,node_ids):

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
