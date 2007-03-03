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

# Standard library imports
import re

# Enthought library imports
from enthought.traits.api import Str
from enthought.envisage.action.action_plugin_definition import Action


class DefaultAction(Action):
    """ Action with 'standard' settings for class_name, id, and image based on
        the actions class_name.

        For an action called FooBarAction, the action will have the following
        settings:

            class_name = (root_path).action.foo_bar_action.FooBarAction
            id = FooBar
            image = foo_bar
    """

    # The path to the package that the action implementation will be found
    # within.
    root_path = Str


    def __init__(self, *args, **kw):

        super(Action, self).__init__(*args, **kw)

        # If no root path was specified, then assume we want the same package
        # that contained the module this class was declared within.
        if self.root_path == '':
            module = self.__class__.__module__
            package = re.sub('\.\w+$', '', module)
            self.root_path = package

        # If names aren't specified for some of the attributes, we create
        # default ones.
        camel_class_name = self.__class__.__name__
        underscore_class_name = camel_case_to_lowercase_underscore(
                                                               camel_class_name)


        if self.class_name == '':
            self.class_name = '%s.actions.%s.%s' % (self.root_path,
                                                   underscore_class_name,
                                                   camel_class_name)

        # The id and image strings don't use the 'Action' part of the
        # class name in their string.
        id_name = camel_class_name.replace('Action', '')
        image_name = camel_case_to_lowercase_underscore(id_name)

        if self.id == '':
            self.id = id_name

        if self.image == '':
            self.image = image_name


def camel_case_to_lowercase_underscore(s):
    """ Convert a CamelCase name to lower cased underscore format.

        ie. CamelCase->camel_case

        This is useful for translating class names to module names.
    """
    # Replace a upper case letters with an _ and their same character.
    # ie. CamelCase -> _Camel_Case
    s = re.sub('([A-Z])', '_\\1', s)

    # Remove the leading underscore if it exists.
    # ie. _Camel_Case -> Camel_Case
    s = re.sub('^_', '', s)

    # Finally lower case it.
    # ie. Camel_Case -> camel_case
    result = s.lower()

    return result
