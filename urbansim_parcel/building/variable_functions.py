# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from numpy import where, zeros
from urbansim.functions import attribute_label
  
def my_attribute_label(attribute_name):
    """Return a triple (package, dataset_name, attribute_name).
    """
    return "urbansim_parcel.building." + attribute_name
    
