#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

class CoefficientEstimate(object):
    """A coefficient estimated by biogeme"""
    
    def __init__(self, name, value, stderr, t_test):
        """Defines the estimate with the fields outputted by biogeme"""
        self.name = name
        self.value = float(value)
        self.stderr = float(stderr)
        self.t_test = float(t_test)