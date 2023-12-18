# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from .variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from math import pow
from opus_core.simulation_state import SimulationState

class income_adjusted(Variable):
    """
    Adjusts income up slightly, based on ABAG adjustments (assuming this is based on
    inflation, cost of living adjustments, etc.)
    
    Not doing this on any global level because we're not adjusting up land values and other stuff;
    the purpose of this is to export more reasonable incomes to SF-CHAMP.
    """

    def __init__(self):
        
        # This is mysterious and terrible.  But the avg weighted income is just too low!
        self.initial_factor = 1.0
        
        self.year_over_year_factor = 1.01

        Variable.__init__(self)
        
    def compute(self,  dataset_pool):
        income = self.get_dataset().get_attribute("income")
        
        current_year = SimulationState().get_current_time()
        if current_year < 2009: return income
        
        return income*self.initial_factor*pow(self.year_over_year_factor,current_year-2009)
    
