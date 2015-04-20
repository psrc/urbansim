# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import where, logical_not, logical_or, logical_and, zeros, ones
from opus_core.variables.variable import Variable
from opus_core.variables.functions import expfin
from opus_core.logger import logger
from ctypes.test import is_resource_enabled


class expected_sales_price_per_sqft_luv(Variable):
    """
    Exponentiated proposals' expected revenue per sqft used for LUV. 
    The base is 9% of the expected sales price per sqft. For fine-tuning we give some zones (TAZ or FAZ)
    an advantage or disadvantage. The numbers below determine the percentage. If it's above 9 it means
    all proposals in those zones will have higher revenue than others. Below 9 means the opposite.
    """
    _return_type="float32"
        
    weight_factor = {}
    # The order of the geographies below should correspond to the order in which they should be processed.
    # The number gives the maximum id number for that geography that can be find in the parcel dataset
    geo_settings = (('growth_center_id', 535), ('faz_id', 9916), ('zone_id', 3700))
    for id, max_value in geo_settings:
        weight_factor[id] = -1*ones((max_value+1,2), dtype='float32')
    res = 0
    nonres = 1
    weight_factor['growth_center_id'][[506, 511, 520], res] = 18
    weight_factor['growth_center_id'][[520], nonres] = 18
    weight_factor['zone_id'][[2598, 2657], res] = 15
    weight_factor['zone_id'][[2598, 2657], res] = 15
    weight_factor['zone_id'][[2151, 2286, 2293, 2481, 2475,  2116], res] = 18 # double increase
    weight_factor['zone_id'][[2172, 2127, 2284, 2570, 2520, 2487, 2554, 2249, 2169], nonres] = 18
    weight_factor['zone_id'][2147, nonres] = 27 # 3x increase
    weight_factor['zone_id'][[2145, 2309], nonres] = 36 # 4x increase
    weight_factor['zone_id'][[2311, 2310, 2312, 2121, 2282, 2257, 2409, 2171, 2597], nonres] = 4.5 # half decrease
    weight_factor['zone_id'][2214, res] = 1 # only 1% revenue 
    weight_factor['zone_id'][[2118, 2252, 2251, 2564], nonres] = 1    
    weight_factor['faz_id'][705, res] = 18
    weight_factor['faz_id'][[505, 705, 6216], nonres] = 18
    weight_factor['faz_id'][5925, nonres] = 36
    weight_factor['faz_id'][[5825, 5915, 6114, 6115, 6125], nonres] = 1
    
        
    def dependencies(self):
        return ["development_project_proposal.expected_sales_price_per_sqft", 
                "urbansim_parcel.development_project_proposal.zone_id",
                "urbansim_parcel.development_project_proposal.faz_id",
                "growth_center_id = development_project_proposal.disaggregate(parcel.growth_center_id)",
                "is_res = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential) > 0"
                ]
    
    def compute(self,  dataset_pool):
        dpp = self.get_dataset()
        is_res = dpp['is_res']
        is_non_res = logical_not(is_res)
        wis_res = where(is_res)
        wis_non_res = where(is_non_res)
        rev = 9*ones(dpp.size(), dtype="float32")
        # largest geography
        geo = self.geo_settings[0][0]
        rev[wis_res] = self.weight_factor[geo][dpp[geo][wis_res], self.res]
        rev[wis_non_res] = self.weight_factor[geo][dpp[geo][wis_non_res], self.nonres]
        # iterate over smaller geography
        for geoitem in self.geo_settings[1:len(self.geo_settings)]:
            geo = geoitem[0]
            # residential
            zone_rev = self.weight_factor[geo][dpp[geo][wis_res], self.res]
            where_weight = where(zone_rev >= 0)
            rev[wis_res[0][where_weight]] = zone_rev[where_weight]
            # non-residential
            zone_rev = self.weight_factor[geo][dpp[geo][wis_non_res], self.nonres]
            where_weight = where(zone_rev >= 0)
            rev[wis_non_res[0][where_weight]] = zone_rev[where_weight]
        # set remaining elements to default
        rev[where(rev < 0)] = 9    
        price = rev/100. * dpp["expected_sales_price_per_sqft"]
        return expfin(price)
