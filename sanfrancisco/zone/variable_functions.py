# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.functions import attribute_label
  
def my_attribute_label(attribute_name):
    """Return a triple (package, dataset_name, attribute_name).
    """
    return "sanfrancisco.zone." + attribute_name
    
