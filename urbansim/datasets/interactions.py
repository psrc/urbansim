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

from opus_core.datasets.interaction_dataset import InteractionDataset as CoreInteractionDataset
from opus_core.misc import DebugPrinter
from opus_core.resources import Resources

class InteractionDataset(CoreInteractionDataset):
    def __init__(self, resources=None, dataset1=None, dataset2=None, index1 = None, index2 = None, 
                debuglevel=0):
        debug = DebugPrinter(debuglevel)
        debug.print_debug("Creating object %s.%s" % (self.__class__.__module__, self.__class__.__name__), 2)
        
        local_resources = Resources(resources)
        local_resources.merge_if_not_None({"dataset1":dataset1, 
            "dataset2":dataset2, "debug":debug, 
            "index1":index1, "index2":index2})
        CoreInteractionDataset.__init__(self, resources = local_resources)
        
        