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



# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *

from opus_gui.results.opus_result_generator import OpusResultGenerator
from inprocess.travis.opus_core.indicator_framework.representations.visualization import Visualization


class OpusXMLAction_Results(object):
    def __init__(self, parent):
        self.parent = parent
        self.xmlTreeObject = parent.xmlTreeObject
        
        self.currentColumn = None
        self.currentIndex = None
        
        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")

        #create new indicator action (only for my_indicators)
        self.actAddNewIndicator = QAction(self.acceptIcon, 
                                          "Add new indicator",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actAddNewIndicator, SIGNAL("triggered()"), self.addNewIndicator)

        #create new result template...
        self.actAddNewResultTemplate = QAction(self.acceptIcon, 
                                          "Add new result template...",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actAddNewResultTemplate, SIGNAL("triggered()"), self.addNewResultTemplate)          
        
        #generate results will enter a dialogue to pair indicators with 
        #result templates and datasets and then run them to produce results
        self.actGenerateResults = QAction(self.acceptIcon, 
                                          "Generate results with...",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actGenerateResults, SIGNAL("triggered()"), self.generateResults)

        #examine results via some visualization...
        self.actViewResultAsMatplotlibMap = QAction(self.acceptIcon, 
                                          "Map (Matplotlib)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsMatplotlibMap, SIGNAL("triggered()"), self.viewResultsMatplotlibMap)                
        self.actViewResultAsMatplotlibChart = QAction(self.acceptIcon, 
                                          "Chart (Matplotlib)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsMatplotlibChart, SIGNAL("triggered()"), self.viewResultsMatplotlibChart) 
        self.actViewResultAsTablePerYear = QAction(self.acceptIcon, 
                                          "Table (one per year over selected indicators)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsTablePerYear, SIGNAL("triggered()"), self.viewResultsTablePerYear) 
        self.actViewResultAsTablePerAttribute = QAction(self.acceptIcon, 
                                          "Table (one per selected indicator)",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsTablePerAttribute, SIGNAL("triggered()"), self.viewResultsTablePerAttribute) 
        
        #launch advanced view results window...
        self.actViewResultAsAdvanced = QAction(self.acceptIcon, 
                                          "[Advanced configuration]",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actViewResultAsAdvanced, SIGNAL("triggered()"), self.viewResultsAdvanced) 
        
                
        self.actPlaceHolder = QAction(self.applicationIcon, "Placeholder", self.xmlTreeObject.parent)
        QObject.connect(self.actPlaceHolder, SIGNAL("triggered()"), self.placeHolderAction)

    def placeHolderAction(self):
        print "placeHolderAction pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())

    def addNewIndicator(self):
        print "addNewIndicator pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
    
    def addNewResultTemplate(self):
        print "addNewResultTemplate pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
              
    def generateResults(self):
        print "generateResults pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        # If the XML is not dirty we can go ahead and run... else prompt for saving
        if not self.xmlTreeObject.model.dirty:
            # Add the model to the run Q
            new_result_run = OpusResultGenerator(self.xmlTreeObject,self.xmlTreeObject.parentTool.xml_file)
            self.xmlTreeObject.parent.resultManagerStuff.addGenerateIndicatorForm(new_result_run)
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.parent,
                                "Warning",
                                "Please save changes to project before generating results")
    
    def viewResults(self):
        print "viewResults pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())

    def viewResultsMatplotlibMap(self):
        print "viewResultsMatplotlibMap pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
        
        from opus_core.misc import directory_path_from_opus_path

        visualization = Visualization(indicators = None,
                                      visualization_type = None,
                                      name = None,
                                      years = None,
                                      table_name = 'alldata|chart|1980|alldata_home_based_jobs',
                                      storage_location = directory_path_from_opus_path('opus_gui.main.sample_images'),
                                      file_extension = 'png')
        self.xmlTreeObject.parent.resultManagerStuff.addViewImageIndicator(visualization = visualization)
        
        
    def viewResultsMatplotlibChart(self):
        print "viewResultsMatplotlibChart pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
              
    def viewResultsTablePerAttribute(self):
        print "viewResultsTablePerAttribute pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
              
    def viewResultsTablePerYear(self):
        print "viewResultsTablePerYear pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())

    def viewResultsAdvanced(self):
        print "viewResultsAdvanced pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())                  
        
    def processCustomMenu(self, position):
        if self.xmlTreeObject.view.indexAt(position).isValid() and \
               self.xmlTreeObject.view.indexAt(position).column() == 0:
            self.currentColumn = self.xmlTreeObject.view.indexAt(position).column()
            self.currentIndex = self.xmlTreeObject.view.indexAt(position)
            item = self.currentIndex.internalPointer()
            domNode = item.node()
            if domNode.isNull():
                return
            # Handle ElementNodes
            if domNode.isElement():
                domElement = domNode.toElement()
                if domElement.isNull():
                    return
                if domElement.attribute(QString("type")) == QString("indicator_library") and \
                   domElement.attribute(QString("append_to")) == QString("True"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actAddNewIndicator)
                    self.menu.exec_(QCursor.pos())
                    
                elif domElement.attribute(QString("type")) == QString("source_data"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actGenerateResults)
                    self.menu.exec_(QCursor.pos())

                elif domElement.attribute(QString("type")) == QString("all_source_data"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actAddNewResultTemplate)
                    self.menu.exec_(QCursor.pos())
                                                 
                elif domElement.attribute(QString("type")) == QString("indicator"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actGenerateResults)
                    self.menu.exec_(QCursor.pos())
                    
                elif domElement.attribute(QString("type")) == QString("indicator_result"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    visualization_menu = QMenu(self.xmlTreeObject.parent)
                    visualization_menu.setTitle(QString("View result as..."))
                    
                    visualization_menu.addAction(self.actViewResultAsMatplotlibMap)
                    visualization_menu.addAction(self.actViewResultAsMatplotlibChart)
                    visualization_menu.addAction(self.actViewResultAsTablePerYear)
                    visualization_menu.addAction(self.actViewResultAsTablePerAttribute)
                    visualization_menu.addAction(self.actViewResultAsAdvanced)
                    
                    self.menu.addMenu(visualization_menu)
                    self.menu.exec_(QCursor.pos())
                                   
                else:
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actPlaceHolder)
                    self.menu.exec_(QCursor.pos())
        return


