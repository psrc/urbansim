#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

import os

from numpy import array

from opus_core.configuration import Configuration

class OldStyleConfiguration(Configuration):
    """test configuration using old-style dictionaries"""
    def __init__(self):
        config_changes = {'models': ['a', 'b', 'c'], 'years': (2000, 2010)}
        self.merge(config_changes)
