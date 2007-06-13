#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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


# all_traits_features.py --- Shows primary features of the Traits

from enthought.traits import Delegate, HasTraits, Int, Str, Instance 
from enthought.traits.ui import View, Item

class Parent(HasTraits):
    first_name = Str('')         # INITIALIZATION:
    last_name = Str('')          # 'first_name' and
                                 # 'last_name' are
                                 # initialized to ''
class Child(HasTraits):
    age = Int

    father = Instance(Parent)      # VALIDATION: 'father' must
                                   # be a Parent instance

    first_name = Str('')

    last_name = Delegate('father') # DELEGATION:
                                   # 'last_name' is
                                   # delegated to
                                   # father's 'last_name'

    def _age_changed(self, old, new):  # NOTIFICATION:
                                       # This method is
                                       # called when 'age'
                                       # changes
        print 'Age changed from %s to %s ' % (old, new)


  
#    traits_view = View(Item(name='first_name'),   # TRAITS UI: Define
#                       Item(name='last_name',     # the default window
#                            style='readonly'),    # layout
#                       Item(name='age'),
#                       Item(name='father'))


####################################################
# Make and manipulate objects from the classes above
####################################################

joe = Parent()
joe.last_name = 'Johnson'

# DELEGATION in action
moe = Child()
moe.father = joe
print "Moe's last name is %s" % (moe.last_name)

# NOTIFICATION in action
moe.age = 10

#VISUALIZATION: Display the UI
moe.configure_traits()
