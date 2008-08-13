#
# Opus software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.model_component_creator import ModelComponentCreator

class SamplerFactory(ModelComponentCreator):

    def get_sampler(self, method, debuglevel=0):
        """'method determines the name of sampling subclass in forma package.subdir.name 
        (e.g. opus_core.samplers.weighted_sampler, ...). There has to be a module in the subdir directory
        of that name that contains a class of the same name. 
        """
        return self.get_model_component(method, debuglevel=debuglevel)
