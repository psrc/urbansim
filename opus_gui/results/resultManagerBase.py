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


from opus_gui.results.forms.generate_results_form import GenerateResultsForm
from opus_gui.results.forms.view_documentation_form import ViewDocumentationForm
from opus_gui.results.forms.view_image_form import ViewImageForm
from opus_gui.results.forms.view_table_form import ViewTableForm

# General system includes
import os, sys, tempfile, shutil


class AbstractManagerBase(object):
    #parent is an OpusGui object
    def __init__(self, parent):
        self.parent = parent
        self.tabWidget = parent.tabWidget
        self.gui = parent
        self.guiElements = []
    
    def removeTab(self,guiElement):
        self.tabWidget.removeTab(self.tabWidget.indexOf(guiElement))
        self.guiElements.remove(guiElement)
        guiElement.hide()
    
    def updateGuiElements(self):
        for guiElement in self.guiElements:
            if guiElement.inGui == False:
                self.tabWidget.insertTab(0,guiElement,guiElement.tabIcon,guiElement.tabLabel)
                self.tabWidget.setCurrentIndex(0)
                guiElement.inGui = True
    
    def setGui(self, gui):
        self.gui = gui
    
# Main Run manager class
class ResultManagerBase(AbstractManagerBase):        

    def addGenerateIndicatorForm(self):
                    
        new_form = GenerateResultsForm(parent = self.parent,
                                       result_manager = self)
        
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

    def addIndicatorForm(self, indicator_type):
        #build visualizations
        #use indicator_framework_interface
        pass
        
    def addViewImageIndicator(self, visualization):
        new_form = ViewImageForm(parent = self.parent,
                                 visualization = visualization)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

    def addViewTableIndicator(self, visualization):
        new_form = ViewTableForm(parent = self.parent,
                                 visualization = visualization)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()
        
    def addViewDocumentationForm(self, indicator_node):
        new_form = ViewDocumentationForm(parent = self.parent,
                                         indicator_node = indicator_node)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()
        
