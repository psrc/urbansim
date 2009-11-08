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

from enthought.envisage.single_project.api import ProjectFactory as EnvisageProjectFactory

from opus_gui.model.project import Project


class ProjectFactory(EnvisageProjectFactory):
    ##########################################################################
    # Attributes
    ##########################################################################

    #### public 'ProjectFactory' interface ###################################

    # The class of the project created by this factory.
    #
    # This is provided so that the single_project services can call class
    # methods.
    #
    # This value is meant to be constant for the lifetime of this class!
    PROJECT_CLASS = Project


    ##########################################################################
    # 'ProjectFactory' interface.
    ##########################################################################

    #### public method #######################################################

    def create(self):
        """
        Create a new project from scratch.

        This must return an instance of a Project or 'None'.  A return
        value of 'None' indicates that no project could be created.  The
        plugin will display the default traits view to the user so that
        they can configure this new project.

        Override to provide a derived class for new projects!

        """

        return Project()


    def open(self, location):
        """
        Open a project from the specified location.

        This must return an instance of a Project or 'None'.  A return
        value of 'None' indicates that no project could be opened from
        the specified location.

        """

        try:
            project = Project.load(location)
        except:
            logger.exception('Unable to load Project from location %s',
                location)
            project = None

        return project


#### EOF #####################################################################