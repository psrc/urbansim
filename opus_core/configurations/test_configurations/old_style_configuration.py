# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from numpy import array

from opus_core.configuration import Configuration

class OldStyleConfiguration(Configuration):
    """test configuration using old-style dictionaries"""
    def __init__(self):
        config_changes = {'models': ['a', 'b', 'c'], 'years': (2000, 2010)}
        self.merge(config_changes)
