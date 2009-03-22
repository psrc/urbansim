# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

# exception for XML schema version problems

class XMLVersionException(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return self.value