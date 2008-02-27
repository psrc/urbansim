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

from PyQt4.QtCore import QObject, SIGNAL


from opus_gui.results.forms.advanced_visualization_form import AdvancedVisualizationForm
from opus_gui.results.forms.generate_results_form import GenerateResultsForm
from opus_gui.results.forms.view_documentation_form import ViewDocumentationForm
from opus_gui.results.forms.view_image_form import ViewImageForm
from opus_gui.results.forms.view_table_form import ViewTableForm
from opus_gui.results.opus_result_generator import OpusGuiThread, OpusResultVisualizer


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

    def addAdvancedVisualizationForm(self):
        new_form = AdvancedVisualizationForm(parent = self.parent,
                                       result_manager = self)
        
        self.guiElements.insert(0, new_form)
        self.updateGuiElements() 
        
    def addGenerateIndicatorForm(self):

        new_form = GenerateResultsForm(parent = self.parent,
                                       result_manager = self)
        
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

    def addIndicatorForm(self, indicator_type, clicked_node, kwargs):
        #build visualizations
        domDocument = self.parent.toolboxStuff.doc
        self.indicator_type = indicator_type
        self.visualizer = OpusResultVisualizer(
                                xml_path = self.parent.toolboxStuff.xml_file,
                                domDocument = domDocument,
                                indicator_type = indicator_type,
                                clicked_node = clicked_node,
                                kwargs = kwargs)
        
        self.visualization_thread = OpusGuiThread(
                                  parentThread = self.parent,
                                  parent = self,
                                  thread_object = self.visualizer)
        self.visualization_thread.start()

        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.visualization_thread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.visualizationsCreated)
        
    def visualizationsCreated(self, success):

        form_generator = None
        visualizations = self.visualizer.get_visualizations()
        if self.indicator_type == 'matplotlib_map' or \
           self.indicator_type == 'matplotlib_chart':
            form_generator = self.addViewImageIndicator
        elif self.indicator_type == 'table_per_year' or \
             self.indicator_type == 'table_per_attribute':
            form_generator = self.addViewTableIndicator            
        
        if form_generator is not None:    
            for visualization in visualizations:
                form_generator(visualization = visualization)
        
        self.visualization_thread.wait()
        self.visualization_thread = None
        self.visualizer = None

    def addViewImageIndicator(self, visualization):
        new_form = ViewImageForm(parent = self.parent,
                                 visualization = visualization)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()

    def addViewTableIndicator(self, visualization):
        new_form = ViewTableForm(parent = self.parent,
                                 visualization = visualization)
        if self.indicator_type != 'arcgis_map':
            self.guiElements.insert(0, new_form)
            self.updateGuiElements()
        else:
            del new_form
            
    def addViewDocumentationForm(self, indicator_node):
        new_form = ViewDocumentationForm(parent = self.parent,
                                         indicator_node = indicator_node)
        self.guiElements.insert(0, new_form)
        self.updateGuiElements()
        
