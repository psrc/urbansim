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

import os
from inprocess.configurations.xml_configuration import XMLConfiguration

inprocessdir = __import__('inprocess').__path__[0]
baseconfig_path = os.path.join(inprocessdir, 'urbansim_xml_configurations', 'base_urbansim.xml')
c = XMLConfiguration(baseconfig_path)
print c
