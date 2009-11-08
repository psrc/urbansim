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

from enthought.traits import HasTraits, Instance, Str, List
from enthought.traits.ui import View, Item, Group

from opus_gui.model.model_specification import ModelSpecification


class ModelSpecificationList(HasTraits):
    name = Str
    list = List(Instance(ModelSpecification))
    
    my_view = View(
        Item('name', width=300),
        Item('model_specification_list', width=300, height=300),
        )
    