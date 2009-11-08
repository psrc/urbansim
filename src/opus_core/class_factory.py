#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.misc import DebugPrinter
from opus_core.composed_name import ComposedName

class ClassFactory(object):
    """ Class for creating other classes. 
    """        
    def get_class(self, module_composed_name, class_name=None, arguments={}, debug=0):
        """
        'module_composed_name' is either a string or an instance of 
        class ComposedName that represent the full name of the module in which the class 
        given by 'class_name' is implemented. If  'class_name' is None, it is considered to have
        te same name as the module.
        'arguments' is a dictionary with names and values of arguments of the class constructor.
        It returns an object of the given class.
        """
        if module_composed_name == None: return None
        if isinstance(module_composed_name, str):
            module_c_name = ComposedName(module_composed_name)
        else:
            module_c_name = module_composed_name

        if class_name == None:
            class_name = module_c_name.get_short_name()
            
        if not isinstance(debug, DebugPrinter):
            debug = DebugPrinter(debug)
             
        ev = "from " + module_c_name.get_full_name() + " import " + class_name
        try:
            exec(ev)
        except ImportError:
            raise ImportError("Module named '%s' does not exist or could not "
                "import class '%s' from it." 
                    % (module_c_name.get_full_name(), class_name))
        return eval(class_name + "(**arguments)")
                    