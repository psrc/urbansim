# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

class CoefficientEstimate(object):
    """A coefficient estimated by biogeme"""
    
    def __init__(self, name, value, stderr, t_test):
        """Defines the estimate with the fields outputted by biogeme"""
        self.name = name
        self.value = float(value)
        self.stderr = float(stderr)
        self.t_test = float(t_test)