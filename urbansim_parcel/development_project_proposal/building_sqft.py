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

from opus_core.variables.variable import Variable

class building_sqft(Variable):
    """ 
    sums building_sqft over proposal components
    """

    def dependencies(self):
        return ["_building_sqft = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.building_sqft)",
                 ]

    def compute(self, dataset_pool):
        return self.get_dataset().get_attribute("_building_sqft")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
