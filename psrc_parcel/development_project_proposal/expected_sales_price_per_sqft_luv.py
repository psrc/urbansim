# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import where, logical_not, logical_or, logical_and, zeros
from opus_core.variables.variable import Variable
from opus_core.variables.functions import expfin
from opus_core.logger import logger
from ctypes.test import is_resource_enabled


class expected_sales_price_per_sqft_luv(Variable):
    """
    """
    _return_type="float32"
        
    zone_dict = {
            "res-increase": {
                    "zone_id": [2151, 2286, 2293, 2481, 2475, 2657, 2116, 2598],
                    "faz_id": [705]
                   },
            "res-decrease": {
                    "zone_id": [2214],
                    "faz_id": []
                   },
            "nonres-increase": {
                    "zone_id": [2309, 2172, 2255, 2127, 2624, 2147, 2284, 2570, 2520, 2145, 2487, 2554, 2249, 2169, 2403],
                    "faz_id": [505, 705, 5925, 6216]
                   },
            "nonres-decrease": {
                    "zone_id": [2311, 2310, 2312, 2121, 2282, 2257, 2252, 2118, 2251, 2409, 2171, 2597, 2564],
                    "faz_id": [5825, 6125, 6115, 6114, 5915]
                   }
    }
    
    def dependencies(self):
        return ["development_project_proposal.expected_sales_price_per_sqft", 
                "urbansim_parcel.development_project_proposal.zone_id",
                "urbansim_parcel.development_project_proposal.faz_id",
                "is_res = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.is_residential) > 0"
                ]
    
    def compute(self,  dataset_pool):
        dpp = self.get_dataset()
        price = 0.09 * dpp["expected_sales_price_per_sqft"]
        is_res = dpp['is_res']
        is_non_res = logical_not(is_res)
        idx = self._get_indicator("res-increase", is_res)
        price[idx] = 2*price[idx]
        idx = self._get_indicator("res-decrease", is_res)
        price[idx] = 0.5*price[idx]
        idx = self._get_indicator("nonres-increase", is_non_res)
        price[idx] = 2*price[idx]
        idx = self._get_indicator("nonres-decrease", is_non_res)
        price[idx] = 0.5*price[idx]
        return expfin(price)
    
    def _get_indicator(self, what, res_ind):
        ds = self.get_dataset()
        indicator = zeros(ds.size(), dtype='bool8')
        for geoid in self.zone_dict[what].keys():            
            for zone in self.zone_dict[what][geoid]:
                indicator = logical_or(indicator,ds[geoid] == zone)
        return where(logical_and(res_ind, indicator))