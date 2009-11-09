# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import where, zeros
from urbansim.functions import attribute_label

# Functions
def my_attribute_label(attribute_name):
    """Return a triple (package, dataset_name, attribute_name).
    """
    return attribute_label("fazdistrict", attribute_name)
    
