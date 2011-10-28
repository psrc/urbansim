#gives back the value of the current year of simulation, e.g.to calculcate building age

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
	
class current_year():
	from opus_core.simulation_state import SimulationState
    time = SimulationState().get_current_time() 
    return time