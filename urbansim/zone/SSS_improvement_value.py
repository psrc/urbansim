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

from abstract_sum_from_gridcells import abstract_sum_from_gridcells

class SSS_improvement_value(abstract_sum_from_gridcells):

    def __init__(self, sss):
        abstract_sum_from_gridcells.__init__(self)
        self.gc_variable = "%s_improvement_value" % sss
