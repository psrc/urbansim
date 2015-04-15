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
    """
    _return_type="float32"
        
    zone_dict = {
        "15": { # 15% revenue
                "residential": {
                    "zone_id": [2598, 2657],
                    "faz_id": []
                                },
                 "nonresidential": {
                    "zone_id": [2145, 2309, ],
                    "faz_id": []
                            }
                },        
        "18": { # double increase
                "residential": {
                    "zone_id": [2151, 2286, 2293, 2481, 2475,  2116, 6316],
                    "faz_id": [705]
                                },
                 "nonresidential": {
                    "zone_id": [2172, 2127, 2284, 2570, 2520, 2487, 2554, 2249, 2169],
                    "faz_id": [505, 705, 6216]
                             }
                },
        "27": { # 3x increase
                "residential": {
                    "zone_id": [],
                    "faz_id": []
                                },
                 "nonresidential": {
                    "zone_id": [2147,],
                    "faz_id": []
                            }
                }, 
        "36": { # 4x increase
                "residential": {
                    "zone_id": [ ],
                    "faz_id": []
                                },
                 "nonresidential": {
                    "zone_id": [2145, 2309, ],
                    "faz_id": [5925]
                            }
                }, 
        "4.5": { # half decrease
                "residential": {
                    "zone_id": [],
                    "faz_id": []
                                },
                 "nonresidential": {
                    "zone_id": [2311, 2310, 2312, 2121, 2282, 2257, 2409, 2171, 2597],
                    "faz_id": []                            }
                }, 
        "1": { #only 1% revenue 
                "residential": {
                    "zone_id": [2214],
                    "faz_id": []
                                },
                 "nonresidential": {
                    "zone_id": [2118, 2252, 2251, 2564],
                    "faz_id": [5825, 5915, 6114, 6115, 6125]
                            }
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
        is_res = dpp['is_res']
        is_non_res = logical_not(is_res)
        multipl = 9*ones(dpp.size(), dtype="float32")
        for m, set in self.zone_dict.iteritems():
            idx = self._get_indicator("residential", set, is_res)
            multipl[idx] = float(m)
            idx = self._get_indicator("nonresidential", set, is_non_res)
            multipl[idx] = float(m)
            
        price = multipl/100. * dpp["expected_sales_price_per_sqft"]
        return expfin(price)
    
    def _get_indicator(self, what, set, res_ind):
        ds = self.get_dataset()
        indicator = zeros(ds.size(), dtype='bool8')
        for geoid in set[what].keys():            
            for zone in set[what][geoid]:
                indicator = logical_or(indicator,ds[geoid] == zone)
        return where(logical_and(res_ind, indicator))