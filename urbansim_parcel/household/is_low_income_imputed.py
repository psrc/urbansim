# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.household.is_low_income import is_low_income

class is_low_income_imputed(is_low_income):
    """Is income_imputed < mid_income_level.
    income_imputed is the income attribute where missing values are imputed by zonal averages.
    """
    income = "income_imputed"
    
    def dependencies(self):
        return ["urbansim_parcel.household.income_imputed"]