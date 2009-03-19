# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

class OpusError(Exception):
    """Base class for errors in the OPUS package."""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        