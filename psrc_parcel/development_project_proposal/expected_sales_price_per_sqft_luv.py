# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import where, logical_not, logical_and, zeros, ones, percentile, concatenate, array, unique, isclose, newaxis, arange
from scipy import ndimage as nd
from opus_core.variables.variable import Variable
from opus_core.variables.functions import expfin
from opus_core.logger import logger
from ctypes.test import is_resource_enabled


class expected_sales_price_per_sqft_luv(Variable):
    """
    Exponentiated proposals' expected revenue per sqft used for LUV. 
    The base is 9% of the expected sales price per sqft. For fine-tuning we give some zones (TAZ or FAZ)
    an advantage or disadvantage. The numbers below determine the percentile of the city distribution. 
    If it's above 50 (median) it means all proposals in those zones will get a shift up. Below 50 means a shift down.
    """
    _return_type="float32"
        
    status_id = 4
    weight_factor = {}
    # The order of the geographies below should correspond to the order in which they should be processed.
    # The number gives the maximum id number for that geography that can be find in the parcel dataset
    geo_settings = (('growth_center_id', 535), ('faz_id', 9916), ('zone_id', 3700))
    for id, max_value in geo_settings:
        weight_factor[id] = -1*ones((max_value+1,2), dtype='float32')
    res = 0
    nonres = 1
#     weight_factor['growth_center_id'][[506, 511, 520], res] = 18
#     weight_factor['growth_center_id'][[520], nonres] = 18
#     weight_factor['zone_id'][[2598, 2657], res] = 15
#     weight_factor['zone_id'][[2598, 2657], res] = 15
#     weight_factor['zone_id'][[2151, 2286, 2293, 2481, 2475,  2116], res] = 18 # double increase
#     weight_factor['zone_id'][[2172, 2127, 2284, 2570, 2520, 2487, 2554, 2249, 2169], nonres] = 18
#     weight_factor['zone_id'][2147, nonres] = 27 # 3x increase
#     weight_factor['zone_id'][[2145, 2309], nonres] = 36 # 4x increase
#     weight_factor['zone_id'][[2311, 2310, 2312, 2121, 2282, 2257, 2409, 2171, 2597], nonres] = 4.5 # half decrease
#     weight_factor['zone_id'][2214, res] = 1 # only 1% revenue 
#     weight_factor['zone_id'][[2118, 2252, 2251, 2564], nonres] = 1    
#     weight_factor['faz_id'][705, res] = 18
#     weight_factor['faz_id'][[505, 705, 6216], nonres] = 18
#     weight_factor['faz_id'][5925, nonres] = 36
#     weight_factor['faz_id'][[5825, 5915, 6114, 6115, 6125], nonres] = 1

    weight_factor['growth_center_id'][[506, 511, 520], res] = 90
    weight_factor['growth_center_id'][[520], nonres] = 90
    weight_factor['zone_id'][[2598, 2657], res] = 90
    weight_factor['zone_id'][[2151, 2286, 2293, 2481, 2475,  2116], res] = 90
    weight_factor['zone_id'][[2172, 2127, 2284, 2570, 2520, 2487, 2554, 2249, 2169], nonres] = 90
    weight_factor['zone_id'][2147, nonres] = 90 
    weight_factor['zone_id'][[2145, 2309], nonres] = 90
    weight_factor['zone_id'][[2311, 2310, 2312, 2121, 2282, 2257, 2409, 2171, 2597], nonres] = 10 
    weight_factor['zone_id'][2214, res] = 10 
    weight_factor['zone_id'][[2118, 2252, 2251, 2564], nonres] = 10
    weight_factor['faz_id'][705, res] = 90
    weight_factor['faz_id'][[505, 705, 6216], nonres] = 90
    weight_factor['faz_id'][5925, nonres] = 90
    weight_factor['faz_id'][[5825, 5915, 6114, 6115, 6125], nonres] = 10
        
    def dependencies(self):
        return ["development_project_proposal.expected_sales_price_per_sqft", 
                "urbansim_parcel.development_project_proposal.zone_id",
                "urbansim_parcel.development_project_proposal.faz_id",
                "growth_center_id = development_project_proposal.disaggregate(parcel.growth_center_id)",
                "city_id = development_project_proposal.disaggregate(parcel.city_id)",
                "is_res = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential) > 0",
                "is_nonres = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential==0) > 0",
                "development_project_proposal.status_id"
                ]
    
    def compute(self,  dataset_pool):
        dpp = self.get_dataset()
        if self.status_id is not None:
            filter = dpp['status_id'] == self.status_id
        else:
            filter = ones(dpp.size(), dtype="bool8")
        is_res = logical_and(dpp['is_res'], filter)
        is_non_res = logical_and(dpp['is_nonres'], filter)
        wis_res = where(is_res)[0]
        wis_non_res = where(is_non_res)[0]
        price = 9./100. * dpp["expected_sales_price_per_sqft"]
        percentiles = []
        for geo, p in  self.weight_factor.iteritems():
            percentiles = percentiles + list(unique(p))
        percentiles = unique(array(percentiles))
        percentiles = percentiles[percentiles > 0]
        allperc = concatenate((percentiles, array([-1])))
        # convert percentiles into indices for faster lookup
        # these indices are relative to allperc
        weight_factor_idx = {}
        #is_increase = {}
        for geoitem in self.geo_settings:
            geo = geoitem[0]
            weight_factor_idx[geo] = 999*ones(self.weight_factor[geo].shape, dtype='int32')
            for pidx in range(allperc.size):
                weight_factor_idx[geo][where(isclose(self.weight_factor[geo],allperc[pidx]))] = pidx
            #is_increase[geo] = self.weight_factor[geo] > 50
                
        cities = unique(dpp['city_id'])
        # last column is for "no change", i.e. when weight_factor is -1.
        quant_matrix_res = -1*ones((cities.max()+1, percentiles.size+1), dtype='float32')
        quant_matrix_nonres = -1*ones((cities.max()+1, percentiles.size+1), dtype='float32')
        values_res = price[wis_res]
        values_nonres = price[wis_non_res]
        for city in cities:
            idx = where(dpp["city_id"][wis_res]==city)[0]
            if idx.size > 0:
                quant_matrix_res[city,0:-1] = percentile(values_res[idx], percentiles)  
            idx = where(dpp["city_id"][wis_non_res]==city)[0]
            if idx.size > 0:            
                quant_matrix_nonres[city,0:-1] = percentile(values_nonres[idx], percentiles)
        
        #quant_matrix_res[:, -1] = quant_matrix_res[:, -2]
        #quant_matrix_nonres[:, -1] = quant_matrix_nonres[:, -2]
        for geoitem in self.geo_settings:
            geo = geoitem[0]
            # residential
            if self.weight_factor[geo][dpp[geo][wis_res], self.res].size > 0:
                index2d = concatenate((dpp["city_id"][wis_res][newaxis], weight_factor_idx[geo][dpp[geo][wis_res], self.res][newaxis]), axis=0)                
                city_perc = quant_matrix_res[(index2d[0,:], index2d[1,:])]
                zone_mean = nd.mean(price[wis_res], labels=dpp[geo][wis_res], index=arange(geoitem[1]+1))                
                where_weight = where(city_perc >= 0)[0]
                price[wis_res[where_weight]] = price[wis_res[where_weight]] + city_perc[where_weight] - zone_mean[dpp[geo][wis_res[where_weight]]]
            # non-residential
            if self.weight_factor[geo][dpp[geo][wis_non_res], self.nonres].size > 0:
                index2d = concatenate((dpp["city_id"][wis_non_res][newaxis], weight_factor_idx[geo][dpp[geo][wis_non_res], self.nonres][newaxis]), axis=0) 
                city_perc = quant_matrix_nonres[(index2d[0,:], index2d[1,:])]
                zone_mean = nd.mean(price[wis_non_res], labels=dpp[geo][wis_non_res], index=arange(geoitem[1]+1))
                #zone_median = quant_matrix_nonres[dpp["city_id"][wis_non_res],-2]
                where_weight = where(city_perc >= 0)[0]
                price[wis_non_res[where_weight]] = price[wis_non_res[where_weight]] + city_perc[where_weight] - zone_mean[dpp[geo][wis_non_res[where_weight]]]                                      
            
#         rev = 9*ones(dpp.size(), dtype="float32")        
#         # largest geography
#         geo = self.geo_settings[0][0]
#         rev[wis_res] = self.weight_factor[geo][dpp[geo][wis_res], self.res]
#         rev[wis_non_res] = self.weight_factor[geo][dpp[geo][wis_non_res], self.nonres]
#         # iterate over smaller geography
#         for geoitem in self.geo_settings[1:len(self.geo_settings)]:
#             geo = geoitem[0]
#             # residential
#             zone_rev = self.weight_factor[geo][dpp[geo][wis_res], self.res]
#             where_weight = where(zone_rev >= 0)
#             rev[wis_res[0][where_weight]] = zone_rev[where_weight]
#             # non-residential
#             zone_rev = self.weight_factor[geo][dpp[geo][wis_non_res], self.nonres]
#             where_weight = where(zone_rev >= 0)
#             rev[wis_non_res[0][where_weight]] = zone_rev[where_weight]
#         # set remaining elements to default
#         rev[where(rev < 0)] = 9    
#         price = rev/100. * dpp["expected_sales_price_per_sqft"]
        return expfin(price)
