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

class AttributeType(object):
    PRIMARY = 1
    COMPUTED = 2
    LAG = 3
    EXOGENOUS = 4
    
class InteractionAttributeType(object):
    OWNER_AGENT = 1
    OWNER_CHOICE = 2
    OWNER_INTERACTION = 3
    