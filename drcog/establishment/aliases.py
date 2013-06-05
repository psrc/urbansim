# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
    "employment_submarket_id = establishment.disaggregate(drcog.building.employment_submarket_id)",
    "is_office_id = establishment.disaggregate(drcog.building.is_office_id)",
    "sector_id_six = 1*(establishment.sector_id==61) + 2*(establishment.sector_id==71) + 3*numpy.in1d(establishment.sector_id,[11,21,22,23,31,32,33,42,48,49]) + 4*numpy.in1d(establishment.sector_id,[7221,7222,7224]) + 5*numpy.in1d(establishment.sector_id,[44,45,7211,7212,7213,7223]) + 6*numpy.in1d(establishment.sector_id,[51,52,53,54,55,56,62,81,92])",
    "sector_id_retail_agg = establishment.sector_id*numpy.logical_not(numpy.in1d(establishment.sector_id,[7211,7212,7213])) + 7211*numpy.in1d(establishment.sector_id,[7211,7212,7213])"
           ]
