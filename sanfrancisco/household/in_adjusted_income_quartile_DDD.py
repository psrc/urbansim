# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import where,logical_and

class in_adjusted_income_quartile_DDD(Variable):
    """1 if a household in in the given income quartile, 0 otherwise.  
       Quartile should be 1,2,3, or 4.
       
       These are not true quartiles, but they're defined by the quartiles used by ABAG, which is
       * incomes less than $25k,
       * incomes between $25k and $45k
       * incomes between $45k and $75k
       * incomes greater than $75k
       All in 1989 constant dollars.
    """

    def __init__(self, quartile):
        self.quartile = quartile
        Variable.__init__(self)
    
        self.scale = 0.7328  # 1999 dollars to 1989 dollars

        
    def dependencies(self):
        return ["income_adjusted = sanfrancisco.household.income_adjusted"]
            
    def compute(self,  dataset_pool):
        income_adj = self.get_dataset().get_attribute("income_adjusted")
        if self.quartile==1:
            return where(income_adj< (25/self.scale),1,0)
        elif self.quartile==2:
            return where(logical_and(income_adj>= (25/self.scale), income_adj< (45/self.scale)),1,0)
        elif self.quartile==3:       
            return where(logical_and(income_adj> (45/self.scale), income_adj< (75/self.scale)),1,0)
        else:
            return where(income_adj>= (75/self.scale),1,0)

