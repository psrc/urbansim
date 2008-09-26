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

class AbstractManagerBase(object):
    #mainwindow is an OpusGui object
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.tabWidget = mainwindow.tabWidget
        self.gui = mainwindow
        self.guiElements = []
        
    def removeGuiElement(self,guiElement):
        self.tabWidget.removeTab(self.tabWidget.indexOf(guiElement))
        self.guiElements.remove(guiElement)
        guiElement.hide()
        guiElement.ingui = False
        self.updateGuiElements()
    
    def updateGuiElements(self):
        for guiElement in self.guiElements:
            if not guiElement.inGui:
                self.tabWidget.insertTab(0,guiElement,guiElement.tabIcon,guiElement.tabLabel)
                self.tabWidget.setCurrentIndex(0)
                guiElement.inGui = True
    
    def setGui(self, gui):
        self.gui = gui
        
    def addNewGuiElement(self, element):
        self.guiElements.append(element)
        self.updateGuiElements()
        element.show()
        #self.emit(SIGNAL("newModelAddedToManager()"))

    def removeAllElements(self):
        for i in sorted(range(len(self.guiElements)), reverse = True):
            element = self.guiElements[i]
            success = element.removeElement()            
            if success:
                self.removeGuiElement(guiElement = element)
