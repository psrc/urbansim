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

from opus_gui.model.project import Project
from opus_gui.plugin.project_context_adapter import ProjectContextAdapter

from enthought.envisage.resource import ResourceContextAdapterFactory
from enthought.envisage.single_project.api import ProjectResourceType as EnvisageProjectResourceType


class ProjectResourceType(EnvisageProjectResourceType):
    def _context_adapter_factory_default(self):
        return ResourceContextAdapterFactory(
            adaptee_class = Project,
            adapter_class = ProjectContextAdapter,
            resource_type = self,
            )