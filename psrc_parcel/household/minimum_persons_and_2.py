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

from numpy import minimum
from opus_core.variables.variable import Variable

class minimum_persons_and_2(Variable):
    """minimum of persons and 2"""

    _return_type="int32"
    
    def dependencies(self):
        return ["household.persons"]

    def compute(self,  dataset_pool):
        return minimum(self.get_dataset().get_attribute("persons"), 2)